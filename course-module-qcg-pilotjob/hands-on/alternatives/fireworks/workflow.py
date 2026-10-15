"""Build the example 4 and example 5 workflows on a FireWorks LaunchPad.

    python workflow.py average   # one Firework per CSV file, then one that aggregates them
    python workflow.py profile   # one Firework per task length of example 5

The LaunchPad is the file in MONGOMOCK_SERVERSTORE_FILE (no MongoDB server needed). QCG_MAX_INPUTS (or MAX_INPUTS) and
TIMES_FILE scale the runs down, as for the QCG examples.
"""
import glob
import os
import sys

from fireworks import Firework, LaunchPad, ScriptTask, Workflow

HERE = os.path.abspath(os.path.dirname(__file__))
EX4 = os.path.join(HERE, "..", "..", "example_04")
EX5 = os.path.join(HERE, "..", "..", "example_05")

lp = LaunchPad()
lp.reset("", require_password=False)  # a fresh LaunchPad for every run of the exercise

if sys.argv[1:] == ["average"]:
    names = sorted(glob.glob(os.path.join(HERE, "input", "*.csv")))
    limit = int(os.environ.get("QCG_MAX_INPUTS") or os.environ.get("MAX_INPUTS", "0"))
    names = names[:limit] if limit else names
    os.makedirs(os.path.join(HERE, "averages"), exist_ok=True)
    averages = []
    for path in names:
        out = os.path.join(HERE, "averages", os.path.basename(path))
        averages.append(Firework(ScriptTask.from_str(f"python3 {EX4}/average.py {path} > {out}"),
                                 name=os.path.basename(path)))
    # parents=averages is the dependency qcg_job_v0.py forgets: FireWorks will not run this
    # Firework before every average has finished
    aggregate = Firework(ScriptTask.from_str(f"cat {HERE}/averages/*.csv | sort > {HERE}/result.csv"),
                         name="aggregate", parents=averages)
    lp.add_wf(Workflow(averages + [aggregate], name="average"))
    print(f"added {len(averages)} averages and the aggregation")
elif sys.argv[1:] == ["profile"]:
    times = [t.strip() for t in open(os.environ.get("TIMES_FILE", os.path.join(EX5, "times.txt"))) if t.strip()]
    tasks = os.environ.get("TASK_DIR", os.path.join(HERE, "tasks"))
    os.makedirs(tasks, exist_ok=True)
    fws = [Firework(ScriptTask.from_str(f"python {EX5}/sleep.py {t} > {tasks}/{i}.out"), name=f"sleep_{i}")
           for i, t in enumerate(times)]
    lp.add_wf(Workflow(fws, name="profile"))
    print(f"added {len(fws)} sleeping tasks")
else:
    sys.exit(__doc__)
