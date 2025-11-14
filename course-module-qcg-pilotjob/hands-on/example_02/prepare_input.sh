#!/bin/bash

tar -xf input.tar.gz 

input_dir="input"
input_dir_mod="input_mod"

mkdir -p $input_dir_mod

counter=0
for file in $input_dir/*; do
    echo "$counter $(basename $file)"
    base_name=$(basename $file)
    #echo $base_name
    new_name="${counter}_${base_name}"
    #echo $new_name
    cp $file $input_dir_mod/${counter}_$(basename $file) 
    counter=$(( counter + 1 ))
done
