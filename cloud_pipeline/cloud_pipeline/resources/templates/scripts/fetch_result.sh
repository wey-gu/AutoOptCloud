#!/usr/bin/env bash
set -uex

source /var/lib/cloud_pipeline_functions.sh


main()
{

    local benchmark_type=$benchmark_type$
    write_to_console $benchmark_type

}

main "$*"
