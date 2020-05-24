from requests_oauthlib import OAuth1Session
import pandas as pd
import os
import sys

from pyths.config import CONFIG


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
        contents = ' 2時間サスペンスはありません\n'

    if not isinstance(datestr, str):
        datestr = str(datestr)

    assert len(datestr) == 8
    year = datestr[0:4]
    month = datestr[4:6].lstrip('0')
    day = datestr[6:].lstrip('0')
    date = f'{year}年{month}月{day}日'
    report = f'{date}:\n' + contents

    return report


def push_report(msg):
    print(msg)
    tweet(msg)


def inform(filename):
    # filename: progYYYYMMDD.csv
    #datestr = int(os.path.basename(filename).replace('prog', '').replace('.csv', ''))
    df = load_data(filename)
    datestr = df['Date'][0]
    report = generate_report(df, datestr)
    push_report(report)


def get_destination(dst_name):
    if 'messaging' in CONFIG:
        destinations = CONFIG['messaging']
        dst = destinations.get(dst_name, None)
    else:
        dst = None
    return dst


def tweet(msg):
    dst = get_destination('twitter')
    if dst is not None:
        consumer_key = dst['consumer_key']
        consumer_secret = dst['consumer_secret']
        access_token = dst['access_token']
        access_token_secret = dst['access_token_secret']
        session = OAuth1Session(consumer_key, consumer_secret,
                                access_token, access_token_secret)
        url = dst['url']
        params = {'status': msg}
        res = session.post(url, params=params)
        if res.status_code == 200:
            print('TWEET: Success.')
        else:
            print('TWEET: Failed. : {}'.format(res.status_code))


###
def configure(parser):
    parser.add_argument(
        'csvdata',
        help='name of CSV file')


def get_help():
    return 'report 2H suspense drama'


def main(args):
    csvdata = args.csvdata
    inform(csvdata)