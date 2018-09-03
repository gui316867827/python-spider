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

headers ={}

def get_soup(url, parser='html.parser'):
    time = 0
    while(True):
        if time > 10:
            return
        try:
            resp = requests.request(method='GET', url=url, headers=headers, timeout=2)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, parser)
            else:
                time += 1
                print('try to connect to url:\'%s\' for %d times...response_code:%d...' % (url, time, resp.status_code))
        except Exception as ex:
            time += 1
            print('try to connect to url:\'%s\' for %d times' % (url, time))
            print('get_soup:' + str(ex))



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

class staticSource():
    
    def __init__(self,pageSource):
        self.soup = get_soup(pageSource)
        