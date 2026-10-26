#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:40:00
#SBATCH --partition=rome
#SBATCH --output=fw.%j.out
#SBATCH --error=fw.%j.err
# One worker: the file-backed LaunchPad loses Firework states with several rlaunch workers,
# so the tasks run one after another. Parallel workers need a MongoDB server.
set -euo pipefail
module load 2025
# SRC course cluster: module. Snellius has no FireWorks module: use the venv from the README.
module load FireWorks/2.1.4-gfbf-2025a 2>/dev/null || { module load Python/3.13.1-GCCcore-14.2.0; source "$HOME/venvs/fireworks/bin/activate"; }

run_dir=$(mktemp -d "$TMPDIR/fw-profile.XXXXXXXX")
export MONGOMOCK_SERVERSTORE_FILE=$run_dir/launchpad.json TASK_DIR=$run_dir/tasks
echo "{}" > "$MONGOMOCK_SERVERSTORE_FILE"
python workflow.py profile >&2
echo START,$(date +%s)
(cd "$TMPDIR" && rlaunch rapidfire >&2)
python workflow.py check >&2
echo END,$(date +%s)
cat "$TASK_DIR"/*.out
