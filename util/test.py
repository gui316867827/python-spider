'''
@author: wb-tjf399322
'''
import os
import json
import platform

print(os.getcwd())

def test_dict():
    temp ={}
    list_ = [1,2,3,4]
    temp['data'] = list_
    print(json.dumps(temp))

def testJson():
    s = '{flag:all,data:1111}'
    loads = json.loads(s)
    print(loads['flag'])

if __name__ == '__main__':
    testJson()
def get_cpu_count():
    from multiprocessing import cpu_count
    print(cpu_count())
if __name__ == '__main__':
    get_cpu_count()
