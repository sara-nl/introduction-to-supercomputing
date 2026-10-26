#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:20:00
#SBATCH --partition=rome
#SBATCH --output=snakemake-average.%j.out
set -euo pipefail
module load 2025
# SRC course cluster: module. Snellius has no snakemake module: use the venv from the README.
module load snakemake/9.22.0-foss-2025b 2>/dev/null || { module load Python/3.13.1-GCCcore-14.2.0; source "$HOME/venvs/snakemake/bin/activate"; }

tar -xf ../../example_04/input.tar.gz
# Snakemake runs the rules inside this allocation, on as many cores as Slurm gave the job
snakemake --snakefile Snakefile --cores "$SLURM_NTASKS"
echo "result.csv: $(wc -l < result.csv) rows"
