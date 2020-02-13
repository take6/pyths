from selenium import webdriver
import time
import urllib

from . import util

TODAY = 'today'
TOMORROW = 'tomorrow'
TOKYO = 'tokyo'

AREA_MAP = {'tokyo': '23'}


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


def get_url(date=TOMORROW, area=TOKYO):
    program_url = 'https://tv.yahoo.co.jp/listings'

    datestring = date2str(date)

    area_id = AREA_MAP.get(area, None)

    assert area_id is not None

    payload = {
        'va': '24',  # 24時間表示
        'vd': '0',  # 番組詳細を表示しない
        'd': datestring,
        'a': area_id,
        'st': '5'  # 5時を先頭に
    }

    params = urllib.parse.urlencode(payload)

    return '{}?{}'.format(program_url, params)


def get_page_contents(date=TOMORROW, area=TOKYO):
    url = get_url(date=date, area=area)

    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    return browser.find_element_by_tag_name('html')
