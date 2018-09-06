'''
@author: wb-tjf399322
'''
import os
import json
import platform

print(os.getcwd())


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


if __name__ == '__main__':
    trim_str()
