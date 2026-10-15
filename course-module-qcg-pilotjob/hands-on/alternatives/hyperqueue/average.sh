#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:20:00
#SBATCH --partition=rome
#SBATCH --output=hq-average.%j.out
# Example 4 with HyperQueue: the averages of the CSV files, then one result.csv.
# QCG_MAX_INPUTS (or MAX_INPUTS) limits the number of files (all of them by default).
set -euo pipefail
module load 2025
# HyperQueue/0.24.0 exists on the SRC course cluster and on Snellius (2025)
module load Python/3.13.1-GCCcore-14.2.0 2>/dev/null || true
module load HyperQueue/0.24.0

# The server and a worker run inside this allocation, as QCG-PilotJob's manager does
export HQ_SERVER_DIR=$TMPDIR/hq-server
hq server start &
until hq server info >/dev/null 2>&1; do sleep 1; done
hq worker start --cpus="$SLURM_NTASKS" &
hq worker wait 1

tar -xf ../../example_04/input.tar.gz
ls input/*.csv | sort | head -n "${QCG_MAX_INPUTS:-${MAX_INPUTS:-1000000}}" > files.txt
mkdir -p averages

# One task per line of files.txt; HQ_ENTRY holds that line. --wait returns when every task is done,
# so the aggregation below cannot start early (compare qcg_job_v0.py).
hq submit --each-line files.txt --cpus=1 --wait \
    --stdout "$PWD/averages/%{TASK_ID}.csv" --stderr "$PWD/averages/%{TASK_ID}.err" \
    -- bash -c 'python3 ../../example_04/average.py "$HQ_ENTRY"'
hq job list --all

cat averages/*.csv | sort > result.csv
echo "result.csv: $(wc -l < result.csv) rows from $(wc -l < files.txt) files"
hq server stop
