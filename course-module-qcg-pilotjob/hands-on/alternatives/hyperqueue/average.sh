#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:20:00
#SBATCH --partition=rome
#SBATCH --output=hq-average.%j.out
# Example 4 with HyperQueue: the averages of the CSV files, then one result.csv.
# QCG_MAX_INPUTS (or MAX_INPUTS) selects 100 files by default; 0 selects all.
set -euo pipefail
module load 2025
# HyperQueue/0.24.0 exists on the SRC course cluster and on Snellius (2025)
module load Python/3.13.1-GCCcore-14.2.0 2>/dev/null || true
module load HyperQueue/0.24.0

# The server and a worker run inside this allocation, as QCG-PilotJob's manager does
export HQ_SERVER_DIR=$(mktemp -d "$TMPDIR/hq-average.XXXXXXXX")
hq server start &
server_pid=$!
worker_pid=
trap 'rc=$?; trap - EXIT; hq server stop >/dev/null 2>&1 || true; kill "$server_pid" ${worker_pid:+"$worker_pid"} 2>/dev/null || true; wait || true; exit "$rc"' EXIT
for attempt in {1..60}; do
    hq server info >/dev/null 2>&1 && break
    kill -0 "$server_pid"
    sleep 1
done
hq server info >/dev/null
hq worker start --cpus="$SLURM_NTASKS" &
worker_pid=$!
hq worker wait 1

tar -xf ../../example_04/input.tar.gz
python3 - <<'PY' > files.txt
import glob, os
limit = int(os.environ.get("QCG_MAX_INPUTS") or os.environ.get("MAX_INPUTS", "100"))
if limit < 0:
    raise ValueError("QCG_MAX_INPUTS must be nonnegative; 0 selects all files")
names = sorted(glob.glob("input/*.csv"))
names = names[:limit] if limit else names
if not names:
    raise ValueError("No input CSV files found")
print("\n".join(names))
PY
averages=$(mktemp -d "$TMPDIR/hq-averages.XXXXXXXX")

# One task per line of files.txt; HQ_ENTRY holds that line. --wait returns when every task is done,
# so the aggregation below cannot start early (compare qcg_job_v0.py).
hq submit --each-line files.txt --cpus=1 --wait \
    --stdout "$averages/%{TASK_ID}.csv" --stderr "$averages/%{TASK_ID}.err" \
    -- bash -c 'python3 ../../example_04/average.py "$HQ_ENTRY"'
hq job list --all

python3 ../aggregate.py "$averages"/*.csv > result.csv
test "$(wc -l < result.csv)" -eq "$(wc -l < files.txt)"
echo "result.csv: $(wc -l < result.csv) rows from $(wc -l < files.txt) files"
hq server stop
