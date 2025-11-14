import csv
import sys
import os
import statistics

# compute the average over the second column of a CSV file

input_file = sys.argv[1]

# extract the name of the data set from filename by stripping the extension
dataset_name = os.path.basename(input_file).removesuffix('.csv')

values = []
with open(input_file) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        values.append(float(row[1]))

mean_value = statistics.mean(values)

print("{},{}".format(dataset_name, mean_value))
