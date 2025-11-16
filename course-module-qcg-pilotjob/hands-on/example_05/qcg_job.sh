#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:40:00
#SBATCH --partition=rome
#SBATCH --output=qcg.%j.out
#SBATCH --error=qcg.%j.err

module load 2024
module load QCG-PilotJob/0.14.1-gfbf-2024a

START=$( date +%s )
python qcg_job.py
END=$( date +%s )

# concatenate all output files
echo START $START
cat $TMPDIR/qcg_*.out
echo END $END
