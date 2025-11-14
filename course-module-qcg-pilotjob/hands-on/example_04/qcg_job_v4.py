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
jobs_1 = Jobs()

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
manager.wait4(job_ids)
job_status = manager.status(job_ids)
print("-- job status ")
all_comp_finished = (all([job_status.get('jobs').get(x).get('data').get('status')=='SUCCEED'
                          for x in job_ids]) and
                     any([job_status.get('jobs').get(x).get('data').get('status')=='SUCCEED'
                          for x in job_ids]))

print("-- all computations finished = ", all_comp_finished)

# execute the aggregate job if all computations finished successfully
if(all_comp_finished):
    # set up a job for the aggregation of the results
    jobs_1.add(name="aggregate",
               script='cat average_*.csv | sort',
               stdout='result.csv',
               stderr='aggregate.err',
               after=job_names
              )
    print("-- submit the post-processing job")
    manager.submit(jobs_1)
else:
    print("-- WARNING! Not all jobs have finished successfully. The aggregation step will be skipped.")

print("-- wait for the post-processing job")
manager.wait4all()
manager.finish()
print("-- finished")
