This is the directory to place and analyze the results of the multi-threaded experiment. 

#### Before analyzing results
The output log files should be generated and placed in corresponding directories.

- Real pipelines: log files should be placed in `real/indv_logs/`. 
The log file should be named as `time_pipeline_<no_pipeline>_<pipeline_idx>.csv`

- Original WRENCH: log files should be placed in `wrench_org/`. 
The log files (exported by WRENCH) should be named as `dump_<no_pipeline>.json` 

- Extended WRENCH: log files should be placed in `wrench_ext/`. 
The log files (exported by WRENCH) should be named as `dump_<no_pipeline>.json` 

#### Analyzing the results
Open the jupyter notebook `result.ipynb`.