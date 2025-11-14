from qcg.pilotjob.api.job import Jobs
from qcg.pilotjob.api.manager import LocalManager

# create the QCG manager and the Jobs object
manager = LocalManager() 
jobs = Jobs()

# create 512 independent jobs
for job in range(512):
    # define a job
    jobs.add(name="job_{}".format(job),
             exec='hostname',
             stdout='output/job.{}.out'.format(job),
             stderr='output/job.{}.err'.format(job),
             model='default',
             numCores={ "exact" : 1},
             iteration=1)

print("-- submit jobs")
manager.submit(jobs)
print("-- wait for all jobs")
manager.wait4all()
manager.finish()
print("-- finished")
