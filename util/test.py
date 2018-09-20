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
    
if __name__ == '__main__':
    r = [1,2,3,4,5]
    r = list(set(r))
    print(r[0])
