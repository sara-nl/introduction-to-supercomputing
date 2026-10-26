#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:40:00
#SBATCH --partition=rome
#SBATCH --output=hq.%j.out
#SBATCH --error=hq.%j.err
# Example 5 with HyperQueue: the same sleeping tasks, scheduled as soon as a core is free.
# TIMES_FILE picks the task lengths (default: example 5's times.txt).
set -euo pipefail
module load 2025
# HyperQueue/0.24.0 exists on the SRC course cluster and on Snellius (2025)
module load Python/3.13.1-GCCcore-14.2.0 2>/dev/null || true
module load HyperQueue/0.24.0

export HQ_SERVER_DIR=$(mktemp -d "$TMPDIR/hq-profile.XXXXXXXX")
hq server start >&2 &
server_pid=$!
worker_pid=
trap 'rc=$?; trap - EXIT; hq server stop >/dev/null 2>&1 || true; kill "$server_pid" ${worker_pid:+"$worker_pid"} 2>/dev/null || true; wait || true; exit "$rc"' EXIT
for attempt in {1..60}; do
    hq server info >/dev/null 2>&1 && break
    kill -0 "$server_pid"
    sleep 1
done
hq server info >/dev/null
hq worker start --cpus="$SLURM_NTASKS" >&2 &
worker_pid=$!
hq worker wait 1 >&2

times=$(realpath "${TIMES_FILE:-../../example_05/times.txt}")
tasks=$(mktemp -d "$TMPDIR/hq-tasks.XXXXXXXX")
echo START,$(date +%s)
hq submit --each-line "$times" --cpus=1 --wait --stdout "$tasks/%{TASK_ID}.out" --stderr none \
    -- bash -c 'cd "$1" && python3 sleep.py "$HQ_ENTRY"' _ "$PWD/../../example_05" >&2
echo END,$(date +%s)
cat "$tasks"/*.out
hq server stop >&2
