#!/usr/bin/env bash
set -uex

source /var/lib/cloud_pipeline_functions.sh

main()
{
    # Fetch Heat arguments
    local cpu_load_enabled=$cpu_load_enabled$
    local cpu_percentage=$cpu_percentage$
    local fileio_enabled=$fileio_enabled$
    local fileio_thread=$fileio_thread$
    local iperf_enabled=$iperf_enabled$
    local iperf_server_host=$iperf_server_host$
    local iperf_role=$iperf_role$
    local iperf_parallel=$iperf_parallel$

    # append /etc/hosts

    append_etc_hosts

    # generating loads

    if [[ "${iperf_enabled}" = "True" ]]; then
        load_iperf "${iperf_role}" "${iperf_server_host}" "${iperf_parallel}"
    fi

    if [[ "${cpu_load_enabled}" = "True" ]]; then
        load_cpu "${cpu_percentage}"
    fi

    if [[ "${fileio_enabled}" = "True" ]]; then
        load_fileio "${fileio_thread}"
    fi

}

main "$*"
