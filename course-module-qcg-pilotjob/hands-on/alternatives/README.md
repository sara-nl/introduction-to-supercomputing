# The same exercises with HyperQueue, Snakemake and FireWorks

In this hands-on you run the two exercises of the QCG-PilotJob module with three other tools and compare how each one expresses dependencies and fills the cores:

- **Example 4**: one average per CSV file, then an aggregation that must wait for every average.
- **Example 5**: a profile of sleeping tasks, to measure idle time.

Each tool has a directory with the job scripts `average.sh` and `profile.sh`. Run every command from inside the tool directory. The scripts extract `../../example_04/input.tar.gz` and call the helper scripts of examples 4 and 5, so keep the directory layout as it is.

> [!NOTE]
> The scripts ask for 16 cores. On SRC workspaces with 2 cores, scale the runs down:
> ```
> QCG_MAX_INPUTS=100 sbatch --ntasks=2 average.sh
> TIMES_FILE=../../example_05/times_short.txt sbatch --ntasks=2 profile.sh
> ```
> `times_short.txt` keeps the original task lengths of the first 32 of the 160 tasks. SRC does not bill in system billing units: `sacct` reports `CPUTimeRAW` in core-seconds, so count core-hours instead.

## HyperQueue

```
cd hyperqueue
```

Module: `HyperQueue/0.24.0`, with `module load 2025` and `Python/3.13.1-GCCcore-14.2.0`; the scripts load them. The same module name exists on Snellius (2025 stack, which also lists 0.19.0 and 0.20.0). On the SRC course cluster it is a site installation on top of EESSI, not part of EESSI.

The script starts a HyperQueue server and one worker inside the Slurm allocation. It lists the CSV files in `files.txt` and submits one task per line with `hq submit --each-line`. The `--wait` flag blocks until every task has finished, and only then does the script build `result.csv`.

```
sbatch average.sh
sbatch profile.sh
```

The dependency sits in `hq submit --wait`: the aggregation is the line after it.

## Snakemake

```
cd snakemake
```

Module: `snakemake/9.22.0-foss-2025b`, from EESSI on the SRC course cluster. Snellius has no Snakemake module (`module spider snakemake` finds nothing in the 2025 stack). Install it once in a virtual environment; the scripts activate `$HOME/venvs/snakemake` when the module is missing:

```
module load 2025 Python/3.13.1-GCCcore-14.2.0
python -m venv $HOME/venvs/snakemake
source $HOME/venvs/snakemake/bin/activate
pip install snakemake
```

The `Snakefile` defines a rule `average` that turns `input/{name}.csv` into `averages/{name}.csv`, and a rule `aggregate` that builds `result.csv`. `snakemake --cores $SLURM_NTASKS` works out which files are missing and runs the rules on the cores of the allocation. `Snakefile.profile` has one rule instance per task length.

```
sbatch average.sh
sbatch profile.sh
```

The dependency sits in the `input` of the `aggregate` rule: it lists every file in `averages/`.

## FireWorks

```
cd fireworks
```

Module: `FireWorks/2.1.4-gfbf-2025a`, a site installation on top of EESSI on the SRC course cluster only. Snellius has no FireWorks module (`module spider FireWorks` finds nothing in the 2025 stack). Install it once in a virtual environment; the scripts activate `$HOME/venvs/fireworks` when the module is missing:

```
module load 2025 Python/3.13.1-GCCcore-14.2.0
python -m venv $HOME/venvs/fireworks
source $HOME/venvs/fireworks/bin/activate
pip install "fireworks[mongomock]"
```

`workflow.py` writes one Firework per task into a LaunchPad, which here is a file under `$TMPDIR` (no MongoDB server needed). `rlaunch rapidfire` then starts one worker, which runs whichever Firework is ready until none are left. Only one worker may use a file-backed LaunchPad: with several (`rlaunch multi`), Firework states get lost and the aggregation never runs. Parallel workers need a MongoDB server.

```
sbatch average.sh
sbatch profile.sh
```

The dependency sits in `parents=averages` on the `aggregate` Firework in `workflow.py`.

`average.sh` uses 100 of the 1000 files unless `QCG_MAX_INPUTS` says otherwise. On Snellius the one worker took 9 s for 100 files and 212 s for all 1000; Snakemake took 15 s for 1000 files on 16 cores. Do not use FireWorks for many small tasks: without a MongoDB server it runs them one at a time.

## Plot the profiles

The profile job scripts print `START`, `END` and one `TASK` line per task, in the same format as example 5. Plot each output file:

```
module load 2025 SciPy-bundle/2025.06-gfbf-2025a matplotlib/3.10.3-gfbf-2025a
python ../../example_05/plot_profile.py hq.<<<SLURM_JOB_ID>>>.out
python ../../example_05/plot_profile.py snakemake.<<<SLURM_JOB_ID>>>.out
python ../../example_05/plot_profile.py fw.<<<SLURM_JOB_ID>>>.out
```

The lanes in the plot are the CPU number each task reported at its start. Tasks stay unpinned, so overlapping bars can leave white space in a lane that is not idle time. The idle figure below comes from the start and end times of the tasks.

## Measured results

Measured once on 2-core SRC nodes with 2 slots, with the 32 tasks of example 5 at their original lengths. These numbers describe that setup, not the tools in general; a 16-core Snellius allocation was not measured:

| Tool | Span | Idle |
|---|---|---|
| bash pipeline | 266 s | 36% |
| QCG-PilotJob | 221 s | 23% |
| HyperQueue | 172 s | 2% |
| Snakemake | 172 s | 2% |

FireWorks is left out of both tables: it was measured with two `rlaunch multi` workers, which the file-backed LaunchPad does not support.

Most of the QCG-PilotJob idle time came from the module load that each task did in that run. The QCG examples leave `modules=` out, so the tasks inherit the job's environment and a new run should show less idle time for QCG-PilotJob.

Averages of 100 files (example 4), on the same 2-core SRC nodes with 2 slots:

| Tool | Time |
|---|---|
| HyperQueue | 23 s |
| Snakemake | 46 s |
| QCG-PilotJob | 3 min 12 s per version |

## Questions

1. Which tool needed the least code to express that the aggregation waits for every average? Compare the lines in `average.sh`, the `Snakefile` and `workflow.py` with the dependency you found in `qcg_job_v0.py`.
2. Which run had the least idle time, and why? Look at where the idle time sits in each plot.
3. What does each run cost in core-hours? Use `sacct -X --format="JobID%24,Timelimit,AllocCPUS,CPUTime,CPUTimeRAW" -j <jobid>`, as in example 4, and divide `CPUTimeRAW` by 3600.
