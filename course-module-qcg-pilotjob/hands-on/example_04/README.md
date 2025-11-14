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

## Data source
https://www.ncdc.noaa.gov/ghcnd-data-access
