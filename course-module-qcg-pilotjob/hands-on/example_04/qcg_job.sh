#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:20:00
#SBATCH --partition=rome

module load 2024
module load QCG-PilotJob/0.14.1-gfbf-2024a

echo $TMPDIR

# copy input data and scripts to working directory
cp -r $SLURM_SUBMIT_DIR/. $TMPDIR/
cd $TMPDIR

# execute jobs
# python3 qcg_job_v0.py
python3 qcg_job_v1.py
# python3 qcg_job_v2.py
# python3 qcg_job_v3.py
# python3 qcg_job_v4.py

# copy result back to submission directory
mkdir -p $SLURM_SUBMIT_DIR/results
cp result.csv  $SLURM_SUBMIT_DIR/results/

# archive the logdata for the reference
tar -c --exclude="input" --exclude="result" . > $SLURM_SUBMIT_DIR/results/log.${SLURM_JOB_ID}.tar
gzip $SLURM_SUBMIT_DIR/results/log.${SLURM_JOB_ID}.tar



