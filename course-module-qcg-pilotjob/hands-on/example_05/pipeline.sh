#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=01:00:00
#SBATCH --partition=rome
#SBATCH --output=pipeline.%j.out
#SBATCH --error=pipeline.%j.err

module load 2024
module load Python/3.12.3-GCCcore-13.3.0


echo START $( date +%s )

# read all numbers in time 
exec {fd}< "times.txt" || { echo "Cannot open times.txt" >&2; exit 1; }

# iterate over all 10 blocks of 16 numbers
for ((i=0; i<10; i++)); do
    # send 16 jobs to the background
    for ((j=0; j<16; j++)); do
        if ! IFS= read -r -u "$fd" num; then
            echo "Unexpected end of file before 160 numbers" >&2
            exec {fd}<&-
            exit 1
        fi
        python sleep.py $num &
    done
    # wait for all 16 jobs
    wait
done

echo END $( date +%s )
