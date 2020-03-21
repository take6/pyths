import pandas as pd


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
