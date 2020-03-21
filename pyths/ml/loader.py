import pandas as pd

from . import naivebayes

DF_HEADER = ['Date', 'Channel', 'Start', 'Duration', 'Title', 'Summary',
             'Suspense', '2HSuspense']


def load_data(filename):
    if isinstance(filename, str):
        df = pd.read_csv(
            filename,
            header=None,
            names=DF_HEADER)
        return df
    elif isinstance(filename, list):
        return pd.concat([load_data(f) for f in filename], axis=0)
    else:
        raise RuntimeError('filename must be either string or list of strings.')


def load_model(filename):
    machine_types = [naivebayes.NaiveBayes]
    for mt in machine_types:
        try:
            machine = mt()
            machine.load_model(filename)

            return machine
        except AssertionError:
            print('Failed to load as {}. Try next'.format(mt.__class__.__name__))
            continue

    return None
