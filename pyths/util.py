import datetime
import functools
import time


def timeit(f):
    @functools.wraps
    def wrapper(*args, **kwargs):
        start_time = time.time()
        ret = f(*args, **kwargs)
        end_time = time.time()
        print('{}: elapsed {}sec'.format(str(f), end_time - start_time))
        return ret

    return wrapper


def str_today():
    return time.strftime('%Y%m%d', time.localtime())


def str_tomorrow():
    t = time.localtime()
    today = datetime.datetime(year=t.tm_year, month=t.tm_mon, day=t.tm_mday)
    oneday = datetime.timedelta(days=1)
    tomorrow = today + oneday
    return tomorrow.strftime('%Y%m%d')
