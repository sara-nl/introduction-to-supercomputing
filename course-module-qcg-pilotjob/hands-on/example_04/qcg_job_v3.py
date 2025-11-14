from glob import glob
import os
from qcg.pilotjob.api.job import Jobs
from qcg.pilotjob.api.manager import LocalManager

job_names = []

# scan input directory for CVS files
for filename in glob(os.path.join("input/*.csv"), recursive = False):
    # determine the job name and append it to the list
    job_names.append(os.path.basename(filename))

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
             modules=["2024", "Python/3.12.3-GCCcore-13.3.0"],
             iteration=1
            )

print("-- submit computational jobs")
job_ids = manager.submit(jobs)
print("-- wait for all computational jobs")
manager.wait4all()

# set up a job for the aggregation of the results
jobs.clear()
jobs.add(name="aggregate",
         script='cat average_*.csv | sort',
         stdout='result.csv',
         stderr='aggregate.err',
         after=job_names
        )

print("-- submit the post-processing job")
job_ids = manager.submit(jobs)
print("-- wait for the post-processing job")
manager.wait4(job_ids)

manager.finish()
print("-- finished")
