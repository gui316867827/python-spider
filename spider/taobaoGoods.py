'''
Created on Sep 5, 2018

@author: F-Monkey
'''
from spider import get_json

'''
    start page
    https://s.taobao.com/search?data-value=88&ajax=true&callback=jsonp1077&q=%E6%96%87%E8%83%B8
'''

'''
    comments
    
'''
base_url = 'https://s.taobao.com/search?data-value={pageNum}&ajax=true&callback={callback}&q={search_data}'
call_back = 'jsonp1077'

    
def get_one_arr_shops(arr_page):
    _json = get_json(arr_page, callback=call_back)

# all pages of each 44 shops
def get_all_arr_shops(search_data):
    url = base_url.replace('{search_data}', search_data).replace('{callback}', call_back);
    return [url.replace('{pageNum}', str(44 * i)) for i in range(100)]


def start(searchdata):
    pass


if __name__ == '__main__':
    for i in get_all_arr_shops('%E6%96%87%E8%83%B8'):
        print(i)
    
