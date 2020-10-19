This is the directory to place and analyze the results of the single-threaded experiment.

- The output log files from the real pipeline should be placed in `real/<size_in_gb>gb/` directory.
There are 3 required log files: `atop` logfile (named as `atop_mem.log`), `collectl` logfile 
(named as `collectl.dsk`), and `timestamps.csv`.

- The output log files from the python simulator should be place in `pysim/` directory.
There are 2 logfiles for each input file size: `<file_size_gb>gb_sim_mem.csv` 
and `<file_size_gb>gb_sim_time.csv`

- The output log files from the orignal WRENCH simulator should be place in `wrench/original/` directory.
There is only one log file for each input file size named `<file_size_gb>gb_sim_time.csv` 
(because memory profiling is not available in original WRENCH and SimGrid).

- The output log files from the extended WRENCH simulator should be place in `wrench/pagecache/` directory.
There are 2 logfiles for each input file size: `<file_size_gb>gb_sim_mem.csv` 
and `<file_size_gb>gb_sim_time.csv`

- There are 2 logfiles of each simulator for each input file size: `<file_size_gb>gb_sim_mem.csv` 
and `<file_size_gb>gb_sim_time.csv`

#### Before analyzing the results
Run the pipeline on a real system or run simulators, copy the log files and put in 
corresponding directories.

#### Results from the real pipeline
Open the jupyter notebook `plot_real_result.ipynb`

#### Errors comparison between python simulator and WRENCH simulator
Open the jupyter notebook `plot_error.ipynb` 