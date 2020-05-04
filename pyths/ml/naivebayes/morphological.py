# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from pyths.config import CONFIG
appid = CONFIG['morphological']['appid']
pageurl = CONFIG['morphological']['baseurl']


# Yahoo形態素解析の結果をリストで返す
def split(sentence, appid=appid, results='ma', appfilter='1|2|3|4|5|9|10'):
    sentence = sentence.encode('utf-8')
    params = {
        'appid': appid,
        'results': results,
        'filter': appfilter,
        'sentence': sentence,
    }
    r = requests.get(pageurl, params=params)
    content = r.text
    soup = BeautifulSoup(content, features='html.parser')

    return [w.surface.string for w in soup.ma_result.word_list]