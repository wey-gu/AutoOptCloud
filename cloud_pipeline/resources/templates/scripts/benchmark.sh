#!/usr/bin/env bash
set -uex

source /var/lib/cloud_pipeline_functions.sh

benchmark_run()
{
    local benchmark_type="${1}"
    local iperf_server_host=$iperf_server_host$

    start_benchmark

    case $benchmark_type in
        rabbitmq)
            benchmark_rabbitmq ;;
        mysql)
            benchmark_mysql ;;
        fileio)
            benchmark_fileio ;;
        cpu)
            benchmark_cpu ;;
        iperf_s)
            load_iperf server dummy_arg dummy_arg
            update_state succeeded ;;
        iperf_c)
            benchmark_iperf $iperf_server_host ;;
    esac
}

main()
{
    # Fetch Heat arguments
    #local messagequeue_benchmark_enabled=$messagequeue_benchmark_enabled$
    #local db_benchmark_enabled=$db_benchmark_enabled$
    #local fileio_benchmark_enabled=$fileio_benchmark_enabled$
    #local cpu_benchmark_enabled=$cpu_benchmark_enabled$
    #local iperf_server_enabled=$iperf_server_enabled$
    #local iperf_benchmark_enabled=$iperf_benchmark_enabled$

    local benchmark_type=$benchmark_type$
    local counter=$benchmark_retry$

    # preparation
    create_state_file
    append_etc_hosts

    # benchmark

    while [[ $(check_state succeeded | grep -w CHECK_STATE_NOK) && ${counter} != 0 ]]; do
        benchmark_run $benchmark_type
        counter=$((${counter}-1))
        sleep 1;
    done

    if [[ $(check_state succeeded | grep -w CHECK_STATE_NOK) ]]; then
        exit 1
    fi

}

main "$*"
