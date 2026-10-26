# Batch examples used in the slides

Run these commands from this directory on Snellius. `python.sh` runs a small
Python calculation in a batch allocation; its sum is `499999500000`.

```bash
sbatch python.sh
bash compilepi
sbatch pi.sh
```

`compilepi` builds the OpenMP midpoint-integration example in `pi.c`.
`pi.sh` compares thread counts within its allocation. Each line should report
`pi = 3.141592654`; elapsed times depend on the machine. Compare speedup with
the one-thread time and discuss scheduling overhead for a short calculation.
On a two-core SRC node submit `sbatch --cpus-per-task=2 pi.sh`.

The scripts load their own software modules. `pi` is a compiled executable
created by `compilepi`; it is not supplied by a system module.
