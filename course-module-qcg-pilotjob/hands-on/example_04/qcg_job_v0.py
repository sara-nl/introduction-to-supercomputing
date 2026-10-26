from glob import glob
import os
from qcg.pilotjob.api.job import Jobs
from qcg.pilotjob.api.manager import LocalManager

job_names = []

# scan input directory for CVS files
for filename in glob(os.path.join("input/*.csv"), recursive = False):
    # determine the job name and append it to the list
    job_names.append(os.path.basename(filename))

# QCG_MAX_INPUTS limits the run to that many input files, e.g. on a small cluster
max_inputs = int(os.environ.get("QCG_MAX_INPUTS", "0"))
if max_inputs:
    job_names = sorted(job_names)[:max_inputs]

# create the QCG manager and the Jobs object
manager = LocalManager()
jobs = Jobs()

# loop over all files and populate the list of jobs
for jname in job_names:
    print("submit {}".format(jname))
    jobs.add(name=jname,
             exec='python3',
             args=["average.py", os.path.join("input", jname)],
             stdout='average_{}'.format(jname),
             stderr='job.{}.err'.format(jname),
             iteration=1
            )

# add a job for the aggregation of the results
jobs.add(name="aggregate",
         script='cat average_*.csv | sort',
         stdout='result.csv',
         stderr='aggregate.err',
        )

print("-- submit jobs")
manager.submit(jobs)
print("-- wait for all jobs --")
manager.wait4all()
manager.finish()
print("-- finished")
