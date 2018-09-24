'''
@author: F-Monkey
'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import json
import requests
from bs4 import BeautifulSoup
from multiprocessing import cpu_count
import threading
import re
from re import RegexFlag

emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=RegexFlag.UNICODE)


class thread_manager():

    def __init__(self, target, args, poolsize=None):
        if not target:
            raise RuntimeError('target can not be None!!!')
        size = poolsize if poolsize else cpu_count()
        self.thread_list = [MyThread(func=target, args=args) for t in range(size)]  # @UnusedVariable

    def start(self):
        for t in self.thread_list:
            t.start()

    def wait(self):
        for t in self.thread_list:
            t.join()
            
    def get_results(self):
        results = []
        for t in self.thread_list:
            result = t.get_result()
            if type(result) == list:
                results.extend(result)
            else:
                results.append(result)
        return results

        
class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def assert_data(func, *args):
    try:
        return func(*args)
    except Exception as ex:
        print(ex)


def delete_unsupport_unicode(s):
    try:
        text = s.decode('utf8')
    except:
        print('unsupport unicode : utf8')
        return 
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return highpoints.sub(u'', text)


def get_data(url, headers={}, encoding='utf8'):
    time = 0
    while(True):
        if time > 10:
            print('abandon to connect to url....%s' % (url))
            return
        try:
            resp = requests.request(method='GET', url=url, headers=headers, timeout=2)
            if resp.status_code == 200:
                resp.encoding = encoding
                return resp.text
            else:
                time += 1
                print('try to connect to url:\'%s\' for %d times...response_code:%d...' % (url, time, resp.status_code))
        except:
            time += 1
            print('try to connect to url:\'%s\' for %d times' % (url, time))

                     
def get_soup(url, parser='lxml', headers={}):
    try:
        return BeautifulSoup(get_data(url, headers), parser)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    print(get_soup('https://www.baidu.com'))


def get_json(url, callback, headers={}):
    data = get_data(url, headers)
    if not data:
        return
    if callback:
        index = -2 if data[-1] == ';' else -1
        return assert_data(json.loads, (data.replace(callback + '(', '', 1)[:index]))
    else:
        return assert_data(json.loads, (data))


class driver():
    
    def __wait__(self, type_, value, waitTime=None):
        wait = waitTime if waitTime else self.waitTime
        locator = (type_, value)
        WebDriverWait(self.browser, wait, self.waitFrequency).until(EC.presence_of_element_located(locator))
        
    def __init__(self, waitTime=None, waitFrequency=None, forbidden_pic=False, forbidden_js=False, headless=False):
        self.waitTime = waitTime if waitTime else 20;
        self.waitFrequency = waitFrequency if waitFrequency else 0.5
        
        chrome_options = webdriver.ChromeOptions()
        prefs = {
                'profile.default_content_setting_values':{
                        'images':2 if forbidden_pic else 1,
                        'javascript': 2 if forbidden_js else 1
                    }
            }
        chrome_options.add_experimental_option('prefs', prefs)
        if headless:
            chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def find(self, by, value, need_wait=True):
        if need_wait :
            self.__wait__(by, value)
        return self.browser.find_element(by, value)

    def get_page_source(self):
        return self.browser.page_source
    
    
class staticSource():
    
    def __init__(self, pageSource):
        self.soup = get_soup(pageSource)


def wait_thread_executers(fun):
    thread_list = [threading.Thread(target=fun) for t in range(8)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()      
