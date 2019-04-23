#!/usr/bin/env bash
# LOAD env variables
LOAD_IPERF_TIMER_S=86400
# Benchmark variables
FILEIO_SIZE=32G
CPU_MAX_PRIME=2000
RABBIT_SCALE=100
MYSQL_TIME=60
IPERF_TIME=60

append_etc_hosts()
{
    cat /tmp/etc_hosts >> /etc/hosts
    echo >> /etc/hosts
}

create_state_file()
{
    mkdir -p /var/lib/cloud_pipeline/results/
    touch /var/lib/cloud_pipeline/state
}

load_cpu()
{
    local cpu_percentage="${1}"
    cat <<EOF > /tmp/cpu_load.sh
while true ; do
    /usr/bin/stress-ng -c 0 -t 2y -p ${cpu_percentage}
done 
EOF
    /usr/bin/screen -dmS cpu_load /bin/bash /tmp/cpu_load.sh
}


load_fileio()
{
    local fileio_thread="${1}"
    /usr/bin/sysbench fileio --file-total-size=${FILEIO_SIZE} prepare
    cat <<EOF > /tmp/disk_load.sh
while true ; do
    /usr/bin/sysbench fileio --file-total-size=${FILEIO_SIZE} \
      --file-test-mode=rndrw --time=${LOAD_IPERF_TIMER_S} \
      --max-requests=0 --threads=${fileio_thread} \
      run
done 
EOF
    /usr/bin/screen -dmS disk_load /bin/bash /tmp/disk_load.sh
}


load_iperf()
{
    local iperf_role="${1}"
    local iperf_server_host="${2}"
    local iperf_parallel="${3}"

    cat <<EOF > /tmp/iperf_server.sh
while true ; do
    /usr/bin/iperf3 -s
done 
EOF

    cat <<EOF > /tmp/iperf_client.sh
while true ; do
    /usr/bin/iperf3 -c ${iperf_server_host} -t ${LOAD_IPERF_TIMER_S} -P ${iperf_parallel}
done 
EOF

    if [[ "${iperf_role}" = "server" ]]; then
        /usr/bin/screen -dmS iperf_s /bin/bash /tmp/iperf_server.sh
    fi

    if [[ "${iperf_role}" = "client" ]]; then
        /usr/bin/screen -dmS iperf_c /bin/bash /tmp/iperf_client.sh
    fi
}

update_state()
{
    echo "${1}" >> /var/lib/cloud_pipeline/state
}

check_state()
{
    # how to use: 
    # if [[ $(check_state success) == CHECK_STATE_OK]]
    #    foo bar
    # fi
    local return_value=0
    tail -n1 /var/lib/cloud_pipeline/state | grep -w "${1}" || return_value=$?
    if [[ ${return_value} != 0 ]]; then
        echo CHECK_STATE_NOK
        return
    fi
    echo CHECK_STATE_OK
}

start_benchmark()
{
    update_state started
}

run_benchmark_rabbitmq()
{
    ulimit -n 65536; \
        perf-test_linux_x86_64 --queue-pattern 'perf-test-%d' \
        --queue-pattern-from 1 --queue-pattern-to ${RABBIT_SCALE} \
        --producers ${RABBIT_SCALE} --consumers ${RABBIT_SCALE} \
        --heartbeat-sender-threads 10 \
        --publishing-interval 5 -z 30 
}

load_benchmark_rabbitmq()
{
    cat <<EOF > /tmp/load_benchmark_rabbitmq.sh
set -uex
source /var/lib/cloud_pipeline_functions.sh
while true ; do
    run_benchmark_rabbitmq
done 
EOF
    /usr/bin/screen -dmS run_benchmark_rabbitmq /bin/bash /tmp/load_benchmark_rabbitmq.sh
}

benchmark_rabbitmq()
{   
    local return_value=0
    run_benchmark_rabbitmq >> /var/lib/cloud_pipeline/results/rabbitmq.log || return_value=$?
    if [[ ${return_value} != 0 ]]; then
        update_state failed
        return
    fi
    echo BENCHMARK_OK
    update_state succeeded

    load_benchmark_rabbitmq
}

run_sysbench_mysql()
{
    /usr/bin/sysbench oltp_read_write \
    --mysql-user=root \
    --mysql-socket='/var/run/mysqld/mysqld.sock' \
    --tables=20 \
    --table_size=100000 \
    --threads=10 \
    --time=${MYSQL_TIME} \
    run
}

load_sysbench_mysql()
{
    cat <<EOF > /tmp/load_sysbench_mysql.sh
set -uex
source /var/lib/cloud_pipeline_functions.sh
while true ; do
    run_sysbench_mysql
done 
EOF
    /usr/bin/screen -dmS load_sysbench_mysql /bin/bash /tmp/load_sysbench_mysql.sh
}


benchmark_mysql()
{
    local return_value=0
    # preparation
    mysql -e "CREATE DATABASE sbtest;" || true
    mysql -e "CREATE USER sbtest@localhost;" || true
    mysql -e "GRANT ALL PRIVILEGES ON sbtest.* TO sbtest@localhost;" || true

    /usr/bin/sysbench oltp_read_write \
        --mysql-user=root \
        --mysql-socket='/var/run/mysqld/mysqld.sock' \
        --tables=20 \
        --table_size=100000 \
        --threads=10 \
        --time=120 \
        prepare || true

    run_sysbench_mysql >> /var/lib/cloud_pipeline/results/mysql.log || return_value=$?

    if [[ ${return_value} != 0 ]]; then
        update_state failed
        return
    fi
    echo BENCHMARK_OK
    update_state succeeded

    load_sysbench_mysql
}

load_sysbench_cpu()
{
    cat <<EOF > /tmp/load_sysbench_cpu.sh
while true ; do
    /usr/bin/sysbench cpu --cpu-max-prime=${CPU_MAX_PRIME}
done 
EOF
    /usr/bin/screen -dmS load_sysbench_cpu /bin/bash /tmp/load_sysbench_cpu.sh
}

benchmark_cpu()
{
    local return_value=0
    /usr/bin/sysbench cpu --cpu-max-prime=${CPU_MAX_PRIME} run >> /var/lib/cloud_pipeline/results/cpu.log || return_value=$?
    if [[ ${return_value} != 0 ]]; then
        update_state failed
        return
    fi
    echo BENCHMARK_OK
    update_state succeeded

    load_sysbench_cpu
}


benchmark_iperf()
{
    local return_value=0
    local iperf_server_host="${1}"
    /usr/bin/iperf3 -c ${iperf_server_host} -t ${IPERF_TIME} -P 16 >> /var/lib/cloud_pipeline/results/iperf3_c.log || return_value=$?
    if [[ ${return_value} != 0 ]]; then
        update_state failed
        return
    fi
    echo BENCHMARK_OK
    update_state succeeded

    load_iperf client "${iperf_server_host}" 16
}


benchmark_fileio()
{
    local return_value=0
    /usr/bin/sysbench fileio --file-total-size=${FILEIO_SIZE} prepare
    /usr/bin/sysbench fileio --file-total-size=${FILEIO_SIZE} \
        --file-test-mode=rndrw --time=60 \
        --max-requests=0 --threads=12 \
        run  >> /var/lib/cloud_pipeline/results/fileio.log || return_value=$?
    if [[ ${return_value} != 0 ]]; then
        update_state failed
        return
    fi
    echo BENCHMARK_OK
    update_state succeeded

    load_fileio 12
}