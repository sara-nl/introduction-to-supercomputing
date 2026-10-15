import os
from qcg.pilotjob.api.job import Jobs
from qcg.pilotjob.api.manager import LocalManager

manager = LocalManager()
jobs = Jobs()

i = 0
tmpdir = os.environ.get('TMPDIR', '.')

with open(os.environ.get("TIMES_FILE", "times.txt"), "r") as f:
    for line in f:
        sleep_time = int(line.rstrip("\n"))
        jobs.add(name=f'job_{i}',
                 exec='python3',
                 args=["sleep.py", sleep_time],
                 stdout=f'{tmpdir}/qcg_{i}.out',
                 stderr=f'{tmpdir}/qcg_{i}.err',
                 iteration=1)
        i = i + 1

manager.submit(jobs)
manager.wait4all()
manager.finish()
