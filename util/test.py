'''
@author: wb-tjf399322
'''
import os
import json
import platform
import re
from spider.baidu import analysisPic
from PIL import Image
from pytesseract.pytesseract import image_to_string
import pytesseract
from _io import StringIO
import requests
from spider import get_data


def test_dict():
    temp = {}
    list_ = [1, 2, 3, 4]
    temp['data'] = list_
    print(json.dumps(temp))


def testJson():
    s = '{flag:all,data:1111}'
    loads = json.loads(s)
    print(loads['flag'])


def get_cpu_count():
    from multiprocessing import cpu_count
    print(cpu_count())


def trim_str():
    s = 'json(12json(3123141232)'
    print(s.replace('json(', '', 1)[:-1])


def trim_json():
    data = '''
        
    '''
    print(data)
    print(data[7326:])
    json_ = json.loads(data.replace('\"', '\''))
    print(len(json_['data']['comment_list']))
    for k in json_['data']['comment_list']:
        print(k)


def trans_str(s):
    return s.replace('=', '').replace('?', '').replace('x', '*')


def str_arithmetic(s):
    s = trans_str(s)
    print(s)
    a = eval(s)
    print (a)


def test_dict1():
    d = {}
    d['name'] = '111'
    d['aa'] = '222'
    d['333'] = '3'
    keys = list(d.keys())
    for k in keys:
        print(d.pop(k))
    
    
def test_set():
    l = range(50)
    print(l)


def subStr(content):
    return content[:]


def request__(file, url):
    with open(file, 'w') as f:
        data = get_data(url)
        print(data)
        f.write(data)

    
if __name__ == '__main__':
        #request__('1', 'https://s.taobao.com/search?data-key=s%2Cps&data-value=0%2C1&ajax=true&_ksTS=1537662580742_866&callback=jsonp867&initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%96%87%E8%83%B8&suggest=history_1&_input_charset=utf-8&wq=wenxiong&suggest_query=wenxiong&source=suggest&bcoffset=-6&ntoffset=0&p4ppushleft=1%2C48&s=132')
        request__('2', 'https://s.taobao.com/search?data-key=s%2Cps&data-value=0%2C1&ajax=true&_ksTS=1537662580742_866&callback=jsonp867&initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%96%87%E8%83%B8&suggest=history_1&_input_charset=utf-8&wq=wenxiong&suggest_query=wenxiong&source=suggest&bcoffset=-6&ntoffset=0&p4ppushleft=1%2C48&s=176')
