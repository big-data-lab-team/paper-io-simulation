# I/O experiments
Results of the experimental pipelines running the lab cluster.
There are results of 4 experiments stored in the [export/cluster](export/cluster/) directory.
    
## Requirement
1. *python3*
2. *numpy*
3. *pandas*
4. [*nighres*](https://nighres.readthedocs.io/en/latest/) (to run experiment 4)

# Experiment Details
## System specs
- CentOS Linux release 8.1
- 32 cores CPU
- 256 GB of RAM
- 6 x 450GB SSDs.
- Lustre: ...

## Run the experiments
- To the experiments, get `read_write.c` source file compiled: `gcc -Wall read_write.c -o read_write`
- The scripts to run the experiments are `run_exp1.sh`, `run_exp2.sh`, `run_exp3.sh` ,`run_exp4.sh`.

### I. Single threaded experiment (Exp1)
1. Update line 7, 8, 9, 10 in script `run_exp1.sh`.
2. Output files:
- `logfile` in the script.
- `atop.log`
- `collectl-*.dsk.gz`
3. Visualize the result: Run *plot_result.py* to show the result.

### II. Multi-threaded experiment (Exp2)
1. Generate input files: modify line 5, 6, 7 in `gen_data_ex2.sh` and run the script.
2. Run the pipelines: Modify line 9, 10, 11 in `run_exp2.sh` and run the script.
3. Output files are stored in `log_dir` defined in line 11.
4. Visualize the result: 
