#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:02:00
#SBATCH --partition=rome
set -euo pipefail
module load 2025
module load Python/3.13.1-GCCcore-14.2.0
srun python3 -c 'import platform; print("Python on", platform.node()); print("sum:", sum(range(1000000)))'
