# Hands-on QCG-PilotJob
Guide for the hands-on exercises

## Structure of QCG-PilotJob on Snellius
QCG-PilotJob on Snellius requires 3 files:
1. **Slurm job script** - defines resources, loads the module environment and runs the QCG-PilotJob python script.

2. **QCG-PilotJob python script** - invokes the job manager that aggregates all jobs 
along with the resources and conditions defined by the user.

3. **Executable** - this is the main application or script that the user wants to invoke.

The flow of invoking: *Slurm job Script*&rarr;*QCG-PilotJob python script*&rarr;*Executable*

## Description
Below is the description of the order in which the main **Executable** ultimately gets invoked.

1. The Slurm job script defines the resources that the user wants to have for a job. In the same
Slurm script, the user lists the modules that are required for running the **Executable** file and
loads the QCG-PilotJob module. The job script also moves the necessary files needed for the execution
from the home space to the scratch space and once the calculations are complete, copies the relevant files back to the submittion directory. This is essential because the home space is only meant for storage of small files, e.g. source code, input files, pre- post-processing scripts, and should not be used for intense I/O operations. The I/O on the compute nodes needs to occur within the scratch space that uses GPFS (General Parallel File System).

*Please note that within Snellius the environment in the login nodes does not get transferred by default to the allocated compute nodes. Users must load the modules within the Slurm job script.*

2. QCG-PilotJob python script invokes a job manager within the Slurm allocation. This manager runs and 
manages multiple (small) jobs based on the resources provided to it. This script mainly executes different jobs along with different parameters that a user needs to provide for the embarrassingly parallel workflow. Parameters can, e.g., represent different input arguments for the executable. 
Each run will produce its own output and error file. It's also possible to specify loading of additional 
modules per run.

   The status of each job can be found in the file named *nl-agent-{hostname}.log*. For more detailed 
   diagnostics and explanation regarding each job and also the available logs please refer to the 
   [documentation](https://qcg-pilotjob.readthedocs.io/en/develop/logs.html).

> [!NOTE]
> EESSI 2025.06 does not include QCG-PilotJob, so the SRC course cluster carries a site installation on top of it. The job scripts run unchanged: the cluster answers their `module load 2024` and `module load QCG-PilotJob/0.14.1-gfbf-2024a` with that installation, and `module load 2025` followed by `module load QCG-PilotJob/0.14.1-GCCcore-14.2.0` is the same software under its own name. Lower `--ntasks-per-node` to the core count of a workspace (`sinfo -o '%n %c'`), or override it on the command line, for example `sbatch --nodes=3 --ntasks-per-node=2 qcg_job.sh`. SRC does not bill in system billing units: `sacct` reports `CPUTimeRAW` in core-seconds, so count core-hours instead.
> On Snellius, examples 4 and 5 ask for 16 cores (`--ntasks=16`), the 1/8-node minimum allocation on a 128-core rome node. On 2-core SRC workspaces, scale them down so a run takes minutes, not an hour:
> ```
> sbatch --array=0-99%10 array_job.sh                                # example 2: 100 of the 1000 files
> QCG_MAX_INPUTS=100 sbatch --ntasks=2 qcg_job.sh                    # example 4: 100 of the 1000 files, each version
> TIMES_FILE=times_short.txt sbatch --ntasks=2 pipeline.sh           # example 5: the first 32 of the 160 tasks
> TIMES_FILE=times_short.txt sbatch --ntasks=2 qcg_job.sh
> ```
> In example 5, `pipeline.sh` runs its tasks in blocks of the job's task count, so both runs use the same number of slots. `times_short.txt` keeps the original task lengths: shorter tasks would make QCG's start-up time per task count for more than the idle time it saves, and the comparison would turn around.
