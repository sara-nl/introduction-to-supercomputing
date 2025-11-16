# Profiling embarrassingly parallel workflows

In this example you'll determine the profile and efficiency of two
embarrassingly parallel workflows.

## Usage

### Helper script

The helper script sleeps for n seconds and reports the assigned CPU and the 
time interval (start and end time) of the process.
```
module load 2024
module load Python/3.12.3-GCCcore-13.3.0
python sleep.py 7
TASK,54,1763290002.014343,1763290009.014470
```

### Submit bash pipelines

```
sbatch pipeline.sh
```

### Submit QCG pilot job

```
sbatch qcg_job.sh
```

### Visualize profile
Wait for until the jobs are finished and check the content of the generated output files:
`pipeline.<<<SLURM_JOB_ID>>>.out` and `qcg.<<<SLURM_JOB_ID>>>.out`

The profile plots can be generated as follows:
```
module load 2024
module load SciPy-bundle/2024.05-gfbf-2024a 
module load matplotlib/3.9.2-gfbf-2024a

python plot_profile.py pipeline.<<<SLURM_JOB_ID>>>.out 
python plot_profile.py qcg.<<<SLURM_JOB_ID>>>.out 
```

Open the generated png files. You may use the OpenOnDemand file browser or copy the file to your local 
device.

What do you observe?


### Efficiency analysis

Based on the profile data in the output file, estimate 

- the required SBUs for both pipelines
- the percentage of idle time
