from glob import glob
import json
import os
from pathlib import Path
import sys
import tempfile

from qcg.pilotjob.api.job import Jobs
from qcg.pilotjob.api.manager import LocalManager


def succeeded(manager, ids):
    states = manager.status(ids)['jobs']
    return bool(ids) and all(states[name]['data']['status'] == 'SUCCEED' for name in ids)


def main():
    limit = int(os.environ.get('QCG_MAX_INPUTS', '0'))
    if limit < 0:
        raise ValueError('QCG_MAX_INPUTS must be nonnegative; 0 selects all files')
    names = sorted(glob('input/*.csv'))
    names = names[:limit] if limit else names
    if not names:
        raise ValueError('No input CSV files found')
    outputs = Path(tempfile.mkdtemp(prefix='qcg-averages-', dir='.')).resolve()
    manager = LocalManager()
    try:
        jobs = Jobs()
        files = []
        for filename in names:
            name = Path(filename).name
            output = outputs / name
            files.append(name)
            jobs.add(name=name, exec=sys.executable, args=['average.py', filename],
                     stdout=str(output), stderr=str(outputs / f'{name}.err'))
        print('-- submit computational jobs')
        ids = manager.submit(jobs)
        manager.wait4(ids)
        if not succeeded(manager, ids):
            raise RuntimeError('An average task failed; aggregation cannot run')
        (outputs / 'selected.json').write_text(json.dumps(files), encoding='utf-8')
        aggregate = Jobs()
        aggregate.add(name='aggregate', exec=sys.executable,
                      args=[str(Path(__file__).with_name('aggregate.py').resolve()),
                            str(outputs)],
                      stdout='result.csv', stderr=str(outputs / 'aggregate.err'))
        ids = manager.submit(aggregate)
        manager.wait4(ids)
        if not succeeded(manager, ids):
            raise RuntimeError('The aggregation task failed')
        print('-- finished')
    finally:
        manager.finish()


if __name__ == '__main__':
    main()
