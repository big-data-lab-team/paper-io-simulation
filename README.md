# paper-io-simulation

A paper on I/O simulation in [SimGrid](http://simgrid.org).

## Before generating figures
The figures are generated from the log files exported in real execution and simulators. 
You can use the existing simulation log files in this repository or run the real pipeline/simulators to generate these logs.

1. Real execution
- Single-threaded experiment: The log files of real execution should be placed in [result/single/real/](result/single/real/).
- Multi-threaded experiment: The log files of real execution should be placed in [result/multi/real/](result/multi/real/).

If the log files are not available, or you want to generate your log files from your own experiment, 
run pipeline on a real system using the source code in [exp/real/](exp/real/)

2. Single-threaded simulation log

- **Python simulator**: The log files of the Python simulator should be placed [result/single/pysim/](result/single/pysim/). 
To run the Python simulator, use the source code in [/exp/pysim/](/exp/pysim/)  and follow the instructions in README file.

- **WRENCH simulator**: The log files of the WRENCH simulator shoule be place in [result/single/wrench/original/](result/single/wrench/original/) 
for original WRENCH and [result/single/wrench/pagecache/](result/single/wrench/pagecache/) for WRENCH with page cache.
To run the WRENCH simulator, use this source code [example](https://github.com/dohoangdzung/wrench/tree/io_chunk_test/examples/basic-examples/bare-metal-chain) and follow the instructions in README file.

3. Multi-threaded simulation log

- The log files of the WRENCH simulator shoule be place in [result/single/wrench/original/](result/single/wrench/original/) for original WRENCH 
and in [result/single/wrench/pagecache/](result/single/wrench/pagecache/) for WRENCH with page cache.

- To run the WRENCH simulators, use the source code [example](https://github.com/dohoangdzung/wrench/tree/io_chunk_test) and follow the instructions in README file.

## To generate the figures

Follow the instruction in README file as well as Jupyter notebook available in result directories.

- Single-threaded experiment: [result/single/](result/single/)

- Multi-threaded experiment: [result/multi/](result/multi/)

## Before generate paper: generate the pdf from svg figures

1. Install [inkscape](http://inkscape.org)
2. ./generate_figures.sh