A paper on I/O simulation in [SimGrid](http://simgrid.org).

### Generate the pdf from svg figures
Generate pdf files used in the paper from svg files. 
1. Install [inkscape](http://inkscape.org)
2. ./generate_figures.sh

### Generate the figures
If the svg files are not available to generate pdf files, you should re-generate the svg files 
from experiment results by running the python script `gen_fig.py`.

Experimental figures are generated and saved in:
- Single-threaded experiment: [result/single/figures/](result/single/figures/)
- Multi-threaded experiment: [result/multi/figures/](result/multi/figures/)

The other general figures can be found [here](https://drive.google.com/drive/folders/1ahnUdi9r9niyKgiBlmcODHrO5RUIroo8?usp=sharing) 

### Get the log files
If the log files are missing, or if you would like to run the experiments with your own configurations,
you should run the real pipeline/simulators to generate these logs.

#### 1. Real execution

##### 1.1 Single-threaded experiment.
- Log files location: [result/single/real/](result/single/real/).

##### 1.2 Multi-threaded experiment.
- Log files location: [result/multi/local/real/](result/multi/local/real/).

##### 1.3 NFS experiment.
- Log files location: [result/multi/nfs/real/](result/multi/nfs/real/).

If the log files are not available, or you want to generate your log files from your own experiment, 
run pipeline on a real system using the source code in [exp/real/](exp/real/)

#### 2. Single-threaded simulation

##### 2.1 **Python simulator**
- Log files location: [result/single/pysim/](result/single/pysim/). 
- How to run: use the source code in [/exp/pysim/](/exp/pysim/), follow the instructions in README.

##### 2.2 **Original WRENCH simulator**
- Log files location: 
    - Original WRENCH: [result/single/wrench/original/](result/single/wrench/original/) 
    - WRENCH-cache: [result/single/wrench/pagecache/](result/single/wrench/pagecache/)
- How to run: use this source code [example](https://github.com/wrench-project/wrench/tree/master/examples/basic-examples/io-pagecache/),
 follow the instructions in README.

#### 3. Multi-threaded simulation
- Log files location: 
    - Original WRENCH: [result/multi/local/wrench/original/](result/multi/local/wrench/original/) 
    - WRENCH-cache: [result/multi/local/wrench/pagecache/](result/multi/local/wrench/pagecache/)
- How to run: use the source code [example](https://github.com/wrench-project/wrench/tree/master/examples/basic-examples/io-pagecache/),
 follow the instructions in README.

#### 4. NFS simulation
- Log files location: 
    - Original WRENCH: [result/multi/nfs/wrench/original/](result/multi/nfs/wrench/original/)  
    - WRENCH-cache: [result/multi/nfs/wrench/pagecache/](result/multi/nfs/wrench/pagecache/)
- How to run: use the source code [example](https://github.com/wrench-project/wrench/tree/master/examples/basic-examples/io-pagecache/),
 follow the instructions in README.
