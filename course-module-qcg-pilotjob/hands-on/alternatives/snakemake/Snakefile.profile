# Example 5 with Snakemake: one rule instance per task length.
# TIMES_FILE picks the task lengths (default: example 5's times.txt).
import os

TIMES_FILE = os.environ.get("TIMES_FILE", "../../example_05/times.txt")
TIMES = [line.strip() for line in open(TIMES_FILE) if line.strip()]
SLEEP = os.path.abspath("../../example_05/sleep.py")


rule all:
    input:
        expand("profile/{i}.out", i=range(len(TIMES))),


rule sleep:
    output:
        "profile/{i}.out",
    params:
        seconds=lambda wildcards: TIMES[int(wildcards.i)],
    shell:
        "python {SLEEP} {params.seconds} > {output}"
