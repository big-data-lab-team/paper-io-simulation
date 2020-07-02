#! /bin/bash

rm -f /disk0/dzung/data/file*

max_pipe=32
size=3000 # File size, in MB
data_dir="/disk0/dzung/data/"

for i in $(seq 1 ${max_pipe})
do
    dd if=/dev/urandom of=${data_dir}file${i} bs=1MB count=${size}
done