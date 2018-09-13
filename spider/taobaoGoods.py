'''
Created on Sep 5, 2018

@author: F-Monkey
'''
from spider import get_data, assert_data
import threading
import re
import json

'''
    start page
    https://s.taobao.com/search?data-value=88&ajax=true&callback=jsonp1077&q=%E6%96%87%E8%83%B8
'''

'''
    comments
    
'''
base_url = 'https://s.taobao.com/search?data-value={pageNum}&ajax=true&callback={callback}&q={search_data}'
call_back = 'jsonp1077'



def parse_one_arr_shops(one_page):
    data = get_data(one_page)
    data = re.findall(r'"itemlist":(.+?),"bottomsearch"', data)[0]
    data = data.replace('class="icon-text-1111-stock"', 'class=\'icon-text-1111-stock\'')
    
    json_ = json.loads(data)
    shop_item = json_['data']['auctions']
    for shop in shop_item:
        all_arr_shops.append((shop['nick'], shop['nid'], shop['user_id']))
    
    
def get_one_arr_shops(all_arr_shops_page):
    lock.acquire()
    while len(all_arr_shops_page) > 0:
        each_page = all_arr_shops_page.pop()
    lock.release()
    if each_page:
        assert_data(parse_one_arr_shops, each_page)
    

# all pages of each 44 shops
def get_all_arr_shops(search_data):
    url = base_url.replace('{search_data}', search_data).replace('{callback}', call_back);
    return [url.replace('{pageNum}', str(44 * i)) for i in range(100)]


def start(search_data):
    global response_data
    global lock
    global all_arr_shops
    all_arr_shops = []
    lock = threading.Lock()
    get_all_arr_shops(search_data)
    pass
    

if __name__ == '__main__':
    for i in get_all_arr_shops('%E6%96%87%E8%83%B8'):
        print(i)
    
