#!/bin/sh
watch_file=$1
watch_action=$2

while true ; do
    while inotifywait -e modify $watch_file ; do
        $2
    done
done
