# Average algorithm

Compute the average of one column in several CSV files. Aggregate the results in one output CSV file `results.csv`.

## Usage
1. Prepare input data from the tarball
```shell
./prepare_input.sh
```

2. Submit the array job
```shell
sbatch array_job.sh
```

3. Observe the results in the submittion folder

4. Aggregate all results in one file by running
```shell
./aggregate.sh
```

5. How much time did it take to finish the job? How many SBUs were spent?

## Data source
https://www.ncdc.noaa.gov/ghcnd-data-access
