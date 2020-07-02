#! /bin/bash

rm -f export/*.*
rm -f /disk0/dzung/input/*.*
rm -f /disk0/dzung/output/*.*

input="data/file1"
logfile="export/timestamps_pipeline.csv"
size=20000 #File size is in MB
logperiod=500 #in seconds

dd if=/dev/urandom of=${input} bs=1MB count=${size}

echo 3 | sudo tee /proc/sys/vm/drop_caches

collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p &
sleep 1
atop -P MEM 1 ${logperiod} > export/atop.log &

./pipeline.sh "${input}" "${logfile}"
