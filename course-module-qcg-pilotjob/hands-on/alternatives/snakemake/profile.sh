#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:40:00
#SBATCH --partition=rome
#SBATCH --output=snakemake.%j.out
#SBATCH --error=snakemake.%j.err
set -euo pipefail
module load 2025
# SRC course cluster: module. Snellius has no snakemake module: use the venv from the README.
module load snakemake/9.22.0-foss-2025b 2>/dev/null || { module load Python/3.13.1-GCCcore-14.2.0; source "$HOME/venvs/snakemake/bin/activate"; }

rm -rf profile
echo START,$(date +%s)
snakemake --snakefile Snakefile.profile --cores "$SLURM_NTASKS" >&2
echo END,$(date +%s)
cat profile/*.out
