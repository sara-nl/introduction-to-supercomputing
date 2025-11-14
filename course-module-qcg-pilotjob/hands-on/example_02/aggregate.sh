#!/bin/bash

job_id=$1

if [ -z "$job_id" ]
then
  echo "Error: you need to specify the job ID"
  exit 1
fi

echo "Job ID $job_id"

result_file_name="result.csv"
echo "" > $result_file_name

for slurm_file in slurm-$job_id_*.out
do
  # echo $slurm_file
  csv_file_name=$(cat $slurm_file | grep "Analyzing file" | sed 's/Analyzing file: //g')
  csv_file_name=$(echo $csv_file_name | sed 's/input_mod\///g' | sed 's/.csv//g')
  echo $csv_file_name
  
  cat $slurm_file | grep "$csv_file_name," >> $result_file_name
done	

sort -o ${result_file_name}{,}
