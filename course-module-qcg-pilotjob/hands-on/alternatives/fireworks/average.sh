#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --partition=rome
#SBATCH --output=fw-average.%j.out
# Example 4 with FireWorks: the workflow goes into a LaunchPad, then one worker runs whatever
# is ready until nothing is left. The LaunchPad is a file, which only one process may write:
# several rlaunch workers on it lose Firework states. Parallel workers need a MongoDB server.
# One worker takes about 9 s for 100 files and 212 s for 1000 on Snellius, so 100 files by
# default; QCG_MAX_INPUTS=0 runs all of them.
set -euo pipefail
module load 2025
# SRC course cluster: module. Snellius has no FireWorks module: use the venv from the README.
module load FireWorks/2.1.4-gfbf-2025a 2>/dev/null || { module load Python/3.13.1-GCCcore-14.2.0; source "$HOME/venvs/fireworks/bin/activate"; }

run_dir=$(mktemp -d "$TMPDIR/fw-average.XXXXXXXX")
export MONGOMOCK_SERVERSTORE_FILE=$run_dir/launchpad.json
echo "{}" > "$MONGOMOCK_SERVERSTORE_FILE"   # an empty LaunchPad, as in the FireWorks quickstart
tar -xf ../../example_04/input.tar.gz
QCG_MAX_INPUTS=${QCG_MAX_INPUTS:-${MAX_INPUTS:-100}} python workflow.py average
cd "$TMPDIR"   # rlaunch makes a directory per Firework run
rlaunch rapidfire
lpad get_fws -d count -s COMPLETED
cd - >/dev/null
python workflow.py check
test -s result.csv
echo "result.csv: $(wc -l < result.csv) rows"
