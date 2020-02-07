import selenium
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


def get_url(date=TODAY, area=TOKYO):
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

    return '{}?{}'.format(program_url, params)


def get_page_contents(date=TODAY, area=TOKYO):
    url = get_url(date=date, area=area)

    options = selenium.webdriver.ChromeOptions()
    options.headless = True
    browser = selenium.webdriver.Chrome(options=options)
    browser.get(url)

    return browser.get_element_by_tag_name('html')
