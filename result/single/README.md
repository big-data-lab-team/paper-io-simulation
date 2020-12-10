This is the directory to place and analyze the results of the single-threaded experiment.

### Log files and locations
- The output log files from the real execution of the application should be placed 
in `real/<size_in_gb>gb/` directory.
There are 3 required log files: `atop` logfile (named as `atop_mem.log`), `collectl` logfile 
(named as `collectl.dsk`), and `timestamps.csv`.

- Log files from the python simulator should be place in `pysim/` directory.
There are 2 log files for each input file size: `<file_size_gb>gb_sim_mem.csv` 
and `<file_size_gb>gb_sim_time.csv`

- Log files from the orignal WRENCH simulator should be place in `wrench/original/` directory.
There is only one log file for each input file size named `<file_size_gb>gb_sim_time.csv` 
(because memory profiling is not available in original WRENCH and SimGrid).

- Log files from the WRENCH-cache simulator should be place in `wrench/pagecache/` directory.
There are 2 log files for each input file size: `<file_size_gb>gb_sim_mem.csv` 
and `<file_size_gb>gb_sim_time.csv`
