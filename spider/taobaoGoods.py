'''
Created on Sep 5, 2018

@author: F-Monkey
'''
from spider import get_data
import threading
import re
import json
import time

'''
    start page
    https://s.taobao.com/search?data-value=88&ajax=true&callback=jsonp1077&q=%E6%96%87%E8%83%B8
'''

'''
    comments
    
'''


# countent
# style size
def parse_auctionSku(rateContent, auctionSku):
    data = {}
    data['rateContent'] = rateContent
    ss = auctionSku.split(';')
    style = ss[0].split(':')[1] 
    size = ss[1].split(':')[1]
    data['color'] = style
    data['size'] = size
    return data


class content():
    content_base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={nid}&sellerId={user_id}&currentPage={num}'
    nick_rate_msg = {}
    
    def __init__(self, shops):
        self.shops = shops

    def __get_content_of_shop__(self):
        while len(self.shops) > 0:
            nick, nid, user_id = self.shops.pop()
            shop_content_url = self.content_base_url.replace('{nid}', nid).replace('{user_id}', user_id)
            self.__get_contents__(nick, shop_content_url)
        '''
            self.shops_urls.append(shop_content_url)
        for nick in self.nick_urls:
            urls = self.nick_urls[nick]
            for url in urls:
        '''

    def __get_content__(self, nick, data):
        json_ = json.loads(data.replace(r'jsonp128(', '')[:-2 if data[:-1] == ',' else -1])
        for rate in json_['rateDetail']['rateList']:
            self.lock.acquire()
            d = parse_auctionSku(rate['rateContent'], rate['auctionSku'])
            print(d)
            if self.nick_rate_msg.__contains__(nick):
                # same content
                if self.nick_rate_msg[nick].__contains__(d):
                    self.lock.release()
                    return
                print(d)
                self.nick_rate_msg[nick].append(d)
            else:
                self.nick_rate_msg[nick] = [d]
            self.lock.release()
    
    def __get_contents__(self, nick, url):
        pageNum = 0
        last_data = None
        while(True):
            if pageNum > 70 :
                break
            data = get_data(url.replace('{num}', str(pageNum)))
            pageNum += 1
            if data:
                if pageNum > 1:
                    if last_data and data[:50] != last_data[:50]:
                        self.__get_content__(nick, data)
                    else:
                        break
                else:
                    self.__get_content__(nick, data)
                last_data = data
            else:
                if data:
                    break
                else:
                    continue
                
    def start(self):
        self.lock = threading.Lock()
        thread_list = [threading.Thread(target=self.__get_content_of_shop__) for t in range(8)]
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        return self.nick_rate_msg

        
class shop():
    shops_base_url = 'https://s.taobao.com/search?data-value={pageNum}&ajax=true&callback={callback}&q={search_data}'
    call_back = 'jsonp1077'
    __shops__ = []

    def __init__(self, goodsName):
        url = self.shops_base_url.replace('{search_data}', goodsName).replace('{callback}', self.call_back);
        self.pages_url = set([url.replace('{pageNum}', str(44 * i)) for i in range(100)])
    
    def __get_one_page_shops__(self):
        page = None
        while len(self.pages_url) > 0:
            page = self.pages_url.pop()
            if page:
                data = get_data(page)
                try:
                    data = re.findall(r'"itemlist":(.+?),"bottomsearch"', data)[0]
                    data = data.replace('class="icon-text-1111-stock"', 'class=\'icon-text-1111-stock\'')
                    json_ = json.loads(data)
                    shop_item = json_['data']['auctions']
                    for shop in shop_item:
                        key = (shop['nick'], shop['nid'], shop['user_id'])
                        if not self.__shops__.__contains__(key):
                            self.lock.acquire()
                            self.__shops__.append((shop['nick'], shop['nid'], shop['user_id']))
                            self.lock.release()
                except:
                    pass
    
    def start(self):
        self.lock = threading.Lock()
        thread_list = [threading.Thread(target=self.__get_one_page_shops__) for t in range(8)]
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        return self.__shops__

    
def start(search_data):
    start_time = time.time()
    s = shop(search_data)
    shops = s.start()
    print('has get %d shops.....cost %ds' % (len(shops), (time.time() - start_time)))
    c = content(shops)
    cs = c.start()
    print('has get %d contents.....cost %ds' % (len(cs), (time.time() - start_time)))
    return cs


if __name__ == '__main__':
    start('%E6%96%87%E8%83%B8')
