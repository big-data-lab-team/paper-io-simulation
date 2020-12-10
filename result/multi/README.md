This is the directory to place and analyze the results of the multi-threaded experiment. 
If the log files are not placed in appropriate locations, run the pipeline on a real system or run simulators, 
copy the log files and put in corresponding directories.

### Log files and locations
The output log files should be generated and placed in corresponding directories.

#### Local file system experiment

- Real execution: log files should be placed in `local/real/<i>/`, where `<i>` is the number 
of the repetition. 
The log file should be named as `time_pipeline_<no_pipeline>_<pipeline_idx>.csv`

- Original WRENCH: log files should be placed in `local/wrench/orginal/<i>/`. 
The log files (exported by WRENCH) should be named as `dump_<no_pipeline>.json`.

- WRENCH with page cache: log files should be placed in `local/wrench/pagecache/<i>/`. 
The log files (exported by WRENCH) should be named as `dump_<no_pipeline>.json`.

#### NFS experiment

Similar to above experiment but use the directory `nfs/` instead of `local/`.