from selenium import webdriver
import time
import urllib

from .config import CONFIG
from . import util

TODAY = 'today'
TOMORROW = 'tomorrow'

AREA_LIST = {'tokyo': '23'}


def date2str(date=TOMORROW):
    datestr = str(date)
    if datestr == TODAY:
        return util.str_today()
    elif datestr == TOMORROW:
        return util.str_tomorrow()
    else:
        try:
            # test if given value is compatible with the format
            time.strptime(datestr, '%Y%m%d')
        except Exception:
            return ''

        return datestr


def get_url(date=TOMORROW, area=None):
    program_url = 'https://tv.yahoo.co.jp/listings'

    datestring = date2str(date)

    if area is None:
        area = CONFIG['tvprogram']['area'].lower()
    area_id = AREA_LIST.get(area, None)

    assert area_id is not None

    payload = {
        'va': '24',  # 24時間表示
        'vb': '１',  # 番組詳細を表示しない
        'd': datestring,
        'a': area_id,
        'st': '5',  # 5時を先頭に
        've': '0',  # 「見たい」ボタン不要
    }

    params = urllib.parse.urlencode(payload)

    return '{}?{}'.format(program_url, params)


def get_page_contents(htmldata, date=TOMORROW, area=None):
    url = get_url(date=date, area=area)

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=options)

    try:
        browser.get(url)
        page_source = browser.page_source
    finally:
        browser.quit()

    if htmldata is None:
        htmldata = 'prog{}.html'.format(util.str_tomorrow())

    with open(htmldata, 'w') as f:
        f.write(page_source)

    return page_source


###
def configure(parser):
    parser.add_argument(
        'yyyymmdd',
        help='date for TV program to get')
    parser.add_argument(
        'htmldata',
        help='name of output HTML file name')


def get_help():
    return 'get TV program data as HTML'


def main(args):
    htmldata = args.htmldata

    datestr = args.yyyymmdd
    if datestr is None:
        datestr = TOMORROW

    status = 0
    ret = None
    try:
        ret = get_page_contents(htmldata, datestr)
    except Exception as e:
        print('ERROR: {}'.format(str(e)))
        status = 1

    return ret, status
