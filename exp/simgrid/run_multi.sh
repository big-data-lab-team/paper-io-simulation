#! /bin/bash

for i in $(seq 1 32)
do
    ./cmake-build-debug/my-executable data/platform-files/single_host.xml data/workflows/simple_wf.dax ${i}
done