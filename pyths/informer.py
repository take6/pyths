import pandas as pd
import sys


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


def generate_report(df, datestr):
    contents = ''
    for index, row in df.iterrows():
        if row['2HSuspense'] == 1:
            start_time = row['Start']
            channel = row['Channel']
            title = row['Title']
            contents += f'  {channel}ch {start_time} {title}\n'

    if len(contents) == 0:
        report = f'{datestr} 2時間サスペンスはありません'
    else:
        report = f'{datestr}:\n' + contents

    return report


def push_report(msg):
    print(msg)


def inform(filename):
    # filename: progYYYYMMDD.csv
    datestr = int(filename.replace('prog', '').replace('.csv', ''))
    df = load_data(filename)
    report = generate_report(df, datestr)
    push_report(report)
