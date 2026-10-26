#!/bin/bash
# Measure the workflow alternatives on the course cluster, as a learner, from the hands-on tree:
# example 5's 32 tasks (times_short.txt) with 2 slots on a two-core node for the bash pipeline,
# QCG-PilotJob, HyperQueue and Snakemake, FireWorks with its one worker; and the averages of 100
# files (example 4) with each tool. Outputs and a summary land in measurements/.
set -u
R=$PWD; OUT=$R/measurements; mkdir -p "$OUT"
TIMES=$R/example_05/times_short.txt
common="--parsable --nodes=1 --exclude=coursenode4 --time=01:00:00"
cd "$R/example_05"
j_pipe=$(sbatch $common --ntasks=2 --export=ALL,TIMES_FILE=times_short.txt pipeline.sh)
j_qcg=$(sbatch $common --ntasks=2 --export=ALL,TIMES_FILE=times_short.txt qcg_job.sh)
cd "$R/alternatives/hyperqueue"
j_hq=$(sbatch $common --ntasks=2 --export=ALL,TIMES_FILE=$TIMES profile.sh)
j_hqa=$(sbatch $common --ntasks=2 average.sh)
cd "$R/alternatives/snakemake"
j_sm=$(sbatch $common --ntasks=2 --export=ALL,TIMES_FILE=$TIMES profile.sh)
j_sma=$(sbatch $common --ntasks=2 average.sh)
cd "$R/alternatives/fireworks"
j_fw=$(sbatch $common --ntasks=1 --export=ALL,TIMES_FILE=$TIMES profile.sh)
j_fwa=$(sbatch $common --ntasks=1 average.sh)
cd "$R/example_04"
tar -xf input.tar.gz
sed -i 's/^python3 qcg_job_v1.py/# python3 qcg_job_v1.py/; s/^# python3 qcg_job_v4.py/python3 qcg_job_v4.py/' qcg_job.sh
j_q4=$(sbatch $common --ntasks=2 --export=ALL,QCG_MAX_INPUTS=100 qcg_job.sh)
ids="$j_pipe,$j_qcg,$j_hq,$j_hqa,$j_sm,$j_sma,$j_fw,$j_fwa,$j_q4"
echo "jobs: pipeline=$j_pipe qcg=$j_qcg hq=$j_hq hq-avg=$j_hqa snakemake=$j_sm snakemake-avg=$j_sma fireworks=$j_fw fireworks-avg=$j_fwa qcg-v4-avg=$j_q4"
for t in $(seq 1 240); do [ "$(squeue -h -j "$ids" 2>/dev/null | wc -l)" = 0 ] && break; sleep 15; done
echo "== states"; sacct -X -n -j "$ids" -o JobID,JobName%20,NodeList,AllocCPUS,Elapsed,State,ExitCode
cp "$R/example_05"/pipeline.$j_pipe.out "$R/example_05"/qcg.$j_qcg.out "$R/alternatives/hyperqueue"/hq.$j_hq.out \
   "$R/alternatives/snakemake"/snakemake.$j_sm.out "$R/alternatives/fireworks"/fw.$j_fw.out "$OUT"/ 2>&1
cp "$R/alternatives/hyperqueue"/hq-average.$j_hqa.out "$R/alternatives/snakemake"/*average*.$j_sma.out "$R/alternatives/fireworks"/*average*.$j_fwa.out "$R/example_04"/slurm-$j_q4.out "$OUT"/ 2>&1
sacct -X -n -j "$ids" -o JobID,JobName%20,NodeList,AllocCPUS,Elapsed,State,ExitCode > "$OUT/sacct.txt"
python3 - "$OUT" "$j_pipe:pipeline:2" "$j_qcg:qcg:2" "$j_hq:hq:2" "$j_sm:snakemake:2" "$j_fw:fw:1" <<'PY'
import sys, glob, os
out = sys.argv[1]
print("== idle time (span from START/END lines, busy from TASK lines, slots as given)")
for spec in sys.argv[2:]:
    jid, name, slots = spec.split(":"); slots = int(slots)
    files = glob.glob(f"{out}/{name}.{jid}.out")
    if not files: print(name, jid, "no output"); continue
    start = end = None; busy = 0.0; n = 0
    for line in open(files[0]):
        p = line.strip().split(",")
        if p[0] == "START": start = float(p[1])
        elif p[0] == "END": end = float(p[1])
        elif p[0] == "TASK" and len(p) >= 4: busy += float(p[3]) - float(p[2]); n += 1
    if start is None or end is None: print(name, jid, "no START/END"); continue
    span = end - start
    print(f"{name}: span {span:.0f} s, {n} tasks, busy {busy:.0f} task-s, idle {100*(1-busy/(slots*span)):.0f}% of {slots} slots")
PY
echo "== averages of 100 files (elapsed):"; sacct -X -n -j "$j_hqa,$j_sma,$j_fwa,$j_q4" -o JobID,JobName%20,Elapsed,State
echo MEASURE-DONE
