#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p rome
#SBATCH -t 10
#SBATCH --array 0-999%10

module load 2024
module load Python/3.12.3-GCCcore-13.3.0

# copy input data and scripts to working directory
cp -r $SLURM_SUBMIT_DIR/input_mod $TMPDIR/
cp -r $SLURM_SUBMIT_DIR/average.py $TMPDIR/
cd $TMPDIR
echo "TMPDIR = $TMPDIR"

# average data
input_file_path=input_mod/${SLURM_ARRAY_TASK_ID}_*
echo "Analyzing file: $input_file_path"
python3 average.py $input_file_path
