'''
Created on Sep 5, 2018

@author: F-Monkey
'''
import threading
from spider import get_soup, wait_thread_executers
import re
import json

tieba_url = 'https://tieba.baidu.com/f?kw={data}&ie=utf-8&pn='
baidu_base_url = 'https://tieba.baidu.com'


def parse_user(url):
    soup = get_soup(url)
    if not soup:
        return None
    userInfo = soup.find(name='div', attrs={'class':'userinfo_userdata'})
    userinfo__head = soup.find(name='div', attrs={'id':'j_userhead'}) 
    if userInfo :
        sex = userInfo.find(name='span', attrs={'class':'userinfo_sex_male'})
        if sex:
            sex_ = 'male'
        else:
            sex_ = 'female'
        try:
            user_head = userinfo__head.find(name='img', attrs={'src':re.compile(r'http://?.*')})['src'];
        except Exception as ex:
            print(ex)
            user_head = ''
        name_ = re.findall(r'用户名:(.+?)<', str(userInfo))[0]
        age_ = re.findall(r'吧龄:(.+?)<', str(userInfo))[0]
        titles_ = re.findall(r'发贴:(.+?)<', str(userInfo))[0]
        u = User(name_, user_head, url, sex_, age_, titles_)
        return str(json.dumps(u.__dict__, ensure_ascii=False));
    return str(json.dumps(User(url=url).__dict__, ensure_ascii=False))


# this soup is about each floor ....            
def parse_user_and_content(soup):
    user_url = soup.find('a', attrs={'href':re.compile(r'^/home/main/?.*')})
    content = soup.find('div', attrs={'id':re.compile(r'post_content_?.*')})
    return parse_user(baidu_base_url + user_url['href']), content.text.strip()


class User():

    def __init__(self, name=None, head=None, url=None, sex=None, tbAge=None, tbTitleCount=None):
        self.name = name if name else ''
        self.sex = sex if sex else ''
        self.head = head if head else ''
        self.url = url
        self.tbAge = tbAge if tbAge else ''
        self.tbTitleCount = tbTitleCount if tbTitleCount else ''

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        if self.url == other.url:
            return True
        else:
            return False
    
    def to_dict(self):
        u = {}
        u['name'] = self.name
        u['sex'] = self.sex
        u['url'] = self.url
        u['tbAge'] = self.tbAge
        u['tbTitleCount'] = self.tbTitleCount
        u['head'] = self.head
        return u


class article():
    
    default_len = 50
    article_urls = []   

    def __init__(self, name):
        self.base_url = tieba_url.replace('{data}', name)
        self.pages = [self.base_url + str(50 * i) for i in range(self.default_len)]
        
    def __get_articles__(self):
        while len(self.pages) > 0:
            url = self.pages.pop()
            soup = get_soup(url)
            self.lock.acquire()
            self.article_urls.extend([baidu_base_url + a['href'] for a in soup.findAll('a', attrs={'href':re.compile(r'^/p/\d{10}')})])
            self.lock.release()
    
    def start(self):
        self.lock = threading.Lock()
        wait_thread_executers(fun=self.__get_articles__)
        return self.article_urls


class content():
    all_user_contents = {}

    def __init__(self, articles):
        self.articles = articles
    
    def __analysis_article__(self, base_url):
        soup = get_soup(base_url)
        if not soup:
            return
        childrens = []
        li = soup.find(name='li', class_='pager_theme_4')
        if li:
            [childrens.append(child) for child in soup.find(name='li', class_='pager_theme_4').children]
            childrens = list(filter(lambda x:str(x) != '\n' and str(x).__contains__('href') , childrens))
        pages = []
        pages.append(base_url)
        try:
            if(len(childrens) > 2):
                [pages.append(base_url + '?pn=' + str(i)) for i in range(2, int(re.findall(r'.*pn=(\d+)', childrens[len(childrens) - 1]['href'])[0]) + 1)]
        except Exception as ex:
            print('get_all_pages...exception:{} base_url:{}'.format(str(ex), base_url))
        for page in pages:
            soup = get_soup(page)
            if soup:
                for content_div in soup.find_all('div', attrs={'class', 'l_post_bright'}):
                    try:
                        user, content = parse_user_and_content(content_div)
                        self.lock.acquire()
                        if self.all_user_contents.__contains__(user):
                            self.all_user_contents[user].append(content)
                        else:
                            self.all_user_contents[user] = [content]
                        self.lock.release()
                    except Exception as ex:
                        print(ex)
    
    def __analysis_articles__(self):
        while len(self.articles) > 0 :
            url = self.articles.pop()
            print(url)
            self.__analysis_article__(url)
    
    def start(self):
        self.lock = threading.Lock()
        wait_thread_executers(fun=self.__analysis_articles__)
        return self.all_user_contents


def start(search_data):
    a = article(search_data)
    articles = a.start()
    print(len(articles))
    c = content(articles=articles)
    all_user_contents = c.start()
    for u in all_user_contents:
        print(u.to_dict())


if __name__ == '__main__':
    a = article('相亲')
    articles = a.start()
    print(len(articles))
    c = content(articles=articles)
    all_user_contents = c.start()
    for u in all_user_contents:
        print(u.to_dict())
