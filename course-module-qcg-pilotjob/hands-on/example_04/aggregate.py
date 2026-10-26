"""Validate and combine the outputs selected by the final QCG example."""

import csv
import json
import math
from pathlib import Path
import sys


def aggregate(directory):
    directory = Path(directory)
    names = json.loads((directory / 'selected.json').read_text(encoding='utf-8'))
    if not isinstance(names, list) or not names:
        raise ValueError('The selection must be a nonempty list of output filenames')
    if any(not isinstance(name, str) or Path(name).name != name
           or not name.endswith('.csv') for name in names):
        raise ValueError('Every selected output must be a CSV filename in the output directory')
    if len(set(names)) != len(names):
        raise ValueError('The selection contains duplicate output filenames')
    rows = []
    for name in names:
        with (directory / name).open(encoding='utf-8', newline='') as stream:
            records = list(csv.reader(stream))
        if len(records) != 1 or len(records[0]) != 2:
            raise ValueError(f'{name}: expected exactly one row with two columns')
        row = records[0]
        if row[0] != Path(name).stem or not math.isfinite(float(row[1])):
            raise ValueError(f'{name}: expected its dataset name and a finite mean')
        rows.append(row)
    return sorted(rows)


def main():
    rows = aggregate(sys.argv[1])
    csv.writer(sys.stdout, lineterminator='\n').writerows(rows)


if __name__ == '__main__':
    main()
