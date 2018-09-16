'''
Created on Aug 31, 2018

@author: F-Monkey
'''
import re
import threading
import json
from spider import get_soup, thread_manager

headers = {}

baidu_base_url = 'https://tieba.baidu.com'


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


# 
def parse_content_soup(url):
    soup = get_soup(url)
    if soup:
        for content_div in soup.find_all('div', attrs={'class', 'l_post_bright'}):
            try:
                user, content = parse_user_and_content(content_div)
                if all_user_contents.__contains__(user):
                    all_user_contents[user].append(content)
                else:
                    all_user_contents[user] = [content]
            except Exception as ex:
                print('parse_content_soup:' + str(ex))


# get each page
def get_all_pages(base_url):
    soup = get_soup(base_url)
    if not soup:
        return
    childrens = []
    [childrens.append(child) for child in soup.find(name='li', class_='pager_theme_4').children]
    childrens = list(filter(lambda x:str(x) != '\n' and str(x).__contains__('href') , childrens))
    pages = []
    pages.append(base_url)
    try:
        if(len(childrens) > 2):
            [pages.append(base_url + '?pn=' + str(i)) for i in range(2, int(re.findall(r'.*pn=(\d+)', childrens[len(childrens) - 1]['href'])[0]) + 1)]
    except Exception as ex:
        print('get_all_pages...exception:{} base_url:{}'.format(str(ex), base_url))
    return pages


# pool 
def parse_all_content(pages):
    lock.acquire()
    page = None
    while(len(pages) > 0):
        page = pages.pop()
    lock.release()
    if page:
        parse_content_soup(page)


def get_all_pages_(name, page_count=50):
    root_url = 'https://tieba.baidu.com/f?kw={data}ie=utf-8&pn='
    root_url = root_url.replace('{data}', name)
    pages = []
    for url in  [root_url + str(i) for i in range(page_count)] :
        soup = get_soup(url)
        pages.extend([baidu_base_url + a['href'] for a in soup.findAll('a', attrs={'href':re.compile(r'^/p/\d{10}')})])
    return pages


def start(args):
#     if not re.match(r'^https?:/{2}\w.+$', base_url):
#         return
    if not args['name']:
        print('no argment \'name\' in %s' % (json.dumps(args)))
    global all_user_contents
    global lock
    all_user_contents = {}
    lock = threading.Lock()
    all_pages = []
    for base_url in get_all_pages_(name=args['name']):
        all_pages.extend(get_all_pages(base_url))
    thread_list = [threading.Thread(target=parse_all_content, args=(all_pages,)) for t in range(8)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    return all_user_contents


if __name__ == '__main__':
    for page in get_all_pages_():
        print(page)
