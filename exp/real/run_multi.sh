#! /bin/bash

rm -f export/*.*

#collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p &
#sleep 1
#atop -P MEM 1 500 > export/pipeline_mem_c.log &

max_pipe=32
data_dir="/disk0/dzung/data/"
log_dir="export/"

for no_pipe in $(seq 1 ${max_pipe})
do
    rm /disk0/dzung/data/file*_*
    echo "No of concurrent pipelines: ${no_pipe}."
    echo "Wait for dirty data to be flushed..."
    sleep 300
    echo 3 | sudo tee /proc/sys/vm/drop_caches
    echo "Cache cleared..."
    for pipe_idx in $(seq 1 ${no_pipe})
    do
        echo "read_start,read_end,cpu_start,cpu_end,write_start,write_end" \
            > "export/time_pipeline_${no_pipe}_${pipe_idx}.csv"
        echo "Start pipeline #${pipe_idx} ..."
        ./pipeline.sh "${data_dir}file${pipe_idx}" "${log_dir}time_pipeline_${no_pipe}_${pipe_idx}.csv" &
    done
    wait
done

