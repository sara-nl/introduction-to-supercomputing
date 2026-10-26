#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --time=00:05:00
#SBATCH --partition=rome

# QCG-PilotJob is installed in the 2024 stack only (toolchain gfbf-2024a)
module load 2024
module load QCG-PilotJob/0.14.1-gfbf-2024a

python3 qcg_job.py

