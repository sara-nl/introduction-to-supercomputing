"""Build the example 4 and example 5 workflows on a FireWorks LaunchPad.

    python workflow.py average   # one Firework per CSV file, then one that aggregates them
    python workflow.py profile   # one Firework per task length of example 5

The LaunchPad is the file in MONGOMOCK_SERVERSTORE_FILE (no MongoDB server needed). QCG_MAX_INPUTS (or MAX_INPUTS) and
TIMES_FILE scale the runs down, as for the QCG examples.
"""
import glob
import json
import os
import sys
import shlex
import tempfile

from fireworks import Firework, LaunchPad, ScriptTask, Workflow

HERE = os.path.abspath(os.path.dirname(__file__))
EX4 = os.path.join(HERE, "..", "..", "example_04")
EX5 = os.path.join(HERE, "..", "..", "example_05")

if not os.environ.get("MONGOMOCK_SERVERSTORE_FILE"):
    sys.exit("Set MONGOMOCK_SERVERSTORE_FILE to a private file for this exercise.")
lp = LaunchPad()

if sys.argv[1:] == ["check"]:
    ids = lp.get_fw_ids()
    incomplete = lp.get_fw_ids({"state": {"$ne": "COMPLETED"}})
    if not ids or incomplete:
        sys.exit(f"Workflow did not complete: {len(incomplete)} unfinished of {len(ids)} tasks")
    print(f"completed {len(ids)} Fireworks")
    sys.exit(0)

if sys.argv[1:] not in (["average"], ["profile"]):
    sys.exit(__doc__)
if lp.get_fw_ids():
    sys.exit("Use a new private LaunchPad file for each exercise run.")
lp.reset("", require_password=False)

if sys.argv[1:] == ["average"]:
    names = sorted(glob.glob(os.path.join(HERE, "input", "*.csv")))
    limit = int(os.environ.get("QCG_MAX_INPUTS") or os.environ.get("MAX_INPUTS", "100"))
    if limit < 0:
        sys.exit("QCG_MAX_INPUTS must be nonnegative; 0 selects all files")
    names = names[:limit] if limit else names
    if not names:
        sys.exit("No input CSV files found; extract example_04/input.tar.gz first.")
    output_dir = tempfile.mkdtemp(prefix="fw-averages-", dir=os.environ.get("TMPDIR"))
    averages = []
    outputs = []
    for path in names:
        out = os.path.join(output_dir, os.path.basename(path))
        outputs.append(out)
        command = shlex.join([sys.executable, os.path.join(EX4, "average.py"), path])
        averages.append(Firework(ScriptTask.from_str(f"{command} > {shlex.quote(out)}"),
                                 name=os.path.basename(path)))
    # parents=averages is the dependency qcg_job_v0.py forgets: FireWorks will not run this
    # Firework before every average has finished
    manifest = os.path.join(output_dir, "selected.json")
    with open(manifest, "w", encoding="utf-8") as stream:
        json.dump(outputs, stream)
    command = shlex.join([sys.executable, os.path.join(HERE, "..", "aggregate.py"),
                          "--manifest", manifest])
    aggregate = Firework(ScriptTask.from_str(f"{command} > {shlex.quote(os.path.join(HERE, 'result.csv'))}"),
                         name="aggregate", parents=averages)
    lp.add_wf(Workflow(averages + [aggregate], name="average"))
    print(f"added {len(averages)} averages and the aggregation")
elif sys.argv[1:] == ["profile"]:
    times = [t.strip() for t in open(os.environ.get("TIMES_FILE", os.path.join(EX5, "times.txt"))) if t.strip()]
    tasks = os.environ.get("TASK_DIR", os.path.join(HERE, "tasks"))
    os.makedirs(tasks, exist_ok=True)
    fws = [Firework(ScriptTask.from_str(
        shlex.join([sys.executable, os.path.join(EX5, "sleep.py"), t])
        + " > " + shlex.quote(os.path.join(tasks, f"{i}.out"))), name=f"sleep_{i}")
           for i, t in enumerate(times)]
    lp.add_wf(Workflow(fws, name="profile"))
    print(f"added {len(fws)} sleeping tasks")
else:
    sys.exit(__doc__)
