import requests
import time

TODAY = 'today'
TOKYO = 'tokyo'

AREA_MAP = {'tokyo': '23'}


def date2str(date=TODAY):
    datestr = str(date)
    if datestr == TODAY:
        return time.strftime('%Y%m%d', time.localtime())
    else:
        try:
            # test if given value is compatible with the format
            time.strptime(datestr, '%Y%m%d')
        except Exception:
            return ''

        return datestr



def get_program_contents(date=TODAY, area=TOKYO):
    program_url = 'https://tv.yahoo.co.jp/listings'

    datestring = date2str(date)

    payload = {
        'va': '24',  # 24時間表示
        '0':  # 番組詳細を表示しない
        'd': datestring,
        'a': area_id
    }

