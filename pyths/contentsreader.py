from selenium import webdriver
import time
import urllib

from .config import CONFIG
from . import util

TODAY = 'today'
TOMORROW = 'tomorrow'

AREA_LIST = {'tokyo': '23'}

DEBUG = True


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
        'vb': '0',  # 番組詳細を表示しない
        'd': datestring,
        'a': area_id,
        'st': '5'  # 5時を先頭に
    }

    params = urllib.parse.urlencode(payload)

    return '{}?{}'.format(program_url, params)


def get_page_contents(date=TOMORROW, area=None):
    url = get_url(date=date, area=area)

    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    page_source = browser.page_source

    if DEBUG:
        with open('prog{}.html'.format(util.str_tomorrow()), 'w') as f:
            f.write(page_source)

    browser.quit()

    return page_source
