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
