#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=01:00:00
#SBATCH --partition=rome
#SBATCH --output=pipeline.%j.out
#SBATCH --error=pipeline.%j.err

module load 2025
module load Python/3.13.1-GCCcore-14.2.0


echo START,$( date +%s )

# TIMES_FILE picks the sleep times (default times.txt); the block size is the number of tasks
# Slurm gave the job (16 with the #SBATCH line above), so the comparison with QCG stays fair
times=${TIMES_FILE:-times.txt}
block=${SLURM_NTASKS:-16}
[ -r "$times" ] || { echo "Cannot open $times" >&2; exit 1; }
mapfile -t nums < "$times"

# send the sleeps in blocks of $block, and wait for each block to finish
for ((i=0; i<${#nums[@]}; i+=block)); do
    for num in "${nums[@]:i:block}"; do
        python sleep.py "$num" &
    done
    wait
done

echo END,$( date +%s )
