A paper on I/O simulation in [SimGrid](http://simgrid.org).

### Generate the pdf from svg figures
Generate pdf files used in the paper from svg files. 
1. Install [inkscape](http://inkscape.org)
2. ./generate_figures.sh

### Generate the figures
If the svg files are not available to generate pdf files, you should re-generate the svg files 
from experiment results. 

The figures are generated from the log files exported in real execution and simulators.
Use the Jupyter notebook `generate_figures.ipynb` to generate svg (and also pdf) files.

Figures are generated and saved in:
- Single-threaded experiment: [result/single/figures/](result/single/figures/)
- Multi-threaded experiment: [result/multi/figures/](result/multi/figures/)

### Get the log files
If the log files are missing, or if you would like to run the experiments with your own configurations,
you should run the real pipeline/simulators to generate these logs.

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
To run the WRENCH simulator, use this source code [example](https://github.com/wrench-project/wrench/tree/master/examples/basic-examples/io-pagecache/) and follow the instructions in README file.

3. Multi-threaded simulation log

- The log files of the WRENCH simulator should be place in [result/multi/local/wrench/original/](result/multi/local/wrench/original/) for original WRENCH 
and in [result/multi/local/wrench/pagecache/](result/multi/local/wrench/pagecache/) for WRENCH with page cache.

- To run the WRENCH simulators, use the source code [example](https://github.com/wrench-project/wrench/tree/master/examples/basic-examples/io-pagecache/) and follow the instructions in README file.

4. NFS simulation log

- The log files of the WRENCH simulator should be place in [result/multi/nfs/wrench/original/](result/multi/nfs/wrench/original/) for original WRENCH 
and in [result/multi/nfs/wrench/pagecache/](result/multi/nfs/wrench/pagecache/) for WRENCH with page cache.

- To run the WRENCH simulators, use the source code [example](https://github.com/wrench-project/wrench/tree/master/examples/basic-examples/io-pagecache/) and follow the instructions in README file.
