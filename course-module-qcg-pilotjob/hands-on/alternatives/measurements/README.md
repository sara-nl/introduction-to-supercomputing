# One measured run, 25 October 2026

The numbers in the hands-on README and on the slides come from this run on the SURF Research Cloud course cluster: two-core workspaces `coursenode1` to `coursenode3`, EESSI 2025.06, QCG-PilotJob, HyperQueue, Snakemake and FireWorks from the cluster's modules, every job alone on its node with `--nodes=1 --ntasks=2` (FireWorks `--ntasks=1`, its one worker). `measure.sh` is the driver that submitted the nine jobs as a learner and computed the summary; `sacct.txt` lists the jobs.

Example 5 (the 32 tasks of `times_short.txt`, 338 task-seconds): `pipeline.<job>.out`, `qcg.<job>.out`, `hq.<job>.out`, `snakemake.<job>.out`, `fw.<job>.out`, each with `START`, `END` and one `TASK,id,start,end` line per task. Idle is `1 - busy / (slots * span)`, with busy the sum of the task durations and span `END - START`.

Example 4 (averages of 100 files): `hq-average.<job>.out`, `snakemake-average.<job>.out`, `fw-average.<job>.out`, `slurm-<job>.out` (QCG-PilotJob v4); their elapsed times are in `sacct.txt`.
