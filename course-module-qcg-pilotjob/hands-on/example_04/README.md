# Average algorithm

Compute the average of one column in several CSV files. Aggregate the results in one output CSV file `results.csv`. This example is same as `example_02` from this hands-on.

## Usage
1. Extract input data from the tarball
```shell
tar -xvf input.tar.gz
```

2. Submit the job
```shell
sbatch qcg_job.sh
```

3. Observe the results in the `results` directory.

4. Take a look at the `qcg_job_v0.py` file. Can you spot a problem?

5. Compare `qcg_job_v0.py` to `qcg_job_v1.py`, `qcg_job_v2.py`, `qcg_job_v3.py` and `qcg_job_v4.py`.

6. Estimate the total execution time and SBUs spent on this task.

The required SBUs can be estimated with the `sacct` tool:
``` 
sacct -X --format="JobID%24,Timelimit,AllocCPUS,CPUTime,CPUTimeRAW" -j 16235860
                   JobID  Timelimit  AllocCPUS    CPUTime CPUTimeRAW 
------------------------ ---------- ---------- ---------- ---------- 
                16235860   00:20:00         16   02:00:32       7232 
```

The raw CPU time in this example is 7232 seconds. It can be converted to SBUs:

``` shell
1 SBU / CPU hour * 7232 CPU seconds / 3600 seconds per hour = 2.0
```

## Data source
https://www.ncdc.noaa.gov/ghcnd-data-access
