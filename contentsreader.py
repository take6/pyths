from selenium import webdriver
import time
import urllib

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

    area_id = AREA_MAP.get(area, None)

    assert area_id is not None

    payload = {
        'va': '24',  # 24時間表示
        'vd': '0',  # 番組詳細を表示しない
        'd': datestring,
        'a': area_id
    }

    params = urllib.parse.urlencode(payload)

    url = '{}?{}'.format(program_url, params)

    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    return browser.page_source
