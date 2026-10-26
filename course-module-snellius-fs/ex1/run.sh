#!/bin/bash
#SBATCH -J ex1      # Job name
#SBATCH -p rome     # Specify your partition or queue name
#SBATCH -t 00:15:00 # Max runtime in format HH:MM:SS

set -euo pipefail

module load 2025
module load GCC/14.2.0

exec_name=print-n.out

gcc print-n.c -o ${exec_name}

# Array length <n> is calculated as 10**i
#  Use ibeg and iend to tune the range of i (the Snellius exercise: 10**6 to 10**9 values, up to 8 GB)
#  Use nmax to limit the size of the output vector (10**10 results in 80 GB)
#  Use wdir for the directory written to; wdir=TMPDIR means the job's own $TMPDIR
# Each one is taken from the environment when set, so `iend=8 wdir=TMPDIR sbatch run.sh`
# runs a small version on a small cluster without editing this file.
ibeg=${ibeg:-6}
iend=${iend:-10}
nmax=${nmax:-10000000000}

wdir=${wdir:-$HOME}
if [ "$wdir" = TMPDIR ]; then wdir=$TMPDIR; fi

for (( i = $ibeg; i < $iend; ++i ))
do
    n=$(( 10**$i ))

    if (( $n > $nmax )); then
        data=$(( $n*8/1000000000 ))
        echo "You are attempting to print too much data ($data GB)"
        exit 1
    fi

    srun "./${exec_name}" "$n" "$wdir/ex1.dat" ascii
    echo "Printing $n elements"
done
