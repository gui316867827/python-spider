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


class content():
    content_base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={nid}&sellerId={user_id}&currentPage={num}'
    nick_urls = {}
    nick_rate_msg = {}
    
    def __init__(self, shops):
        for (nick, nid, user_id) in shops:
            shop_content_url = self.content_base_url.replace('{nid}', nid).replace('{user_id}', user_id)
            if self.nick_urls.__contains__(nick):
                self.nick_urls[nick].append(shop_content_url)
            else:
                self.nick_urls[nick] = [shop_content_url]

    def __get_content_of_shop__(self):
        for nick in self.nick_urls:
            urls = self.nick_urls.pop(nick)
            for url in urls:
                self.__get_contents__(nick, url)
    
    def __get_content__(self, nick, data):
        json_ = json.loads(data.replace(r'jsonp128(', '')[:-2 if data[:-1] == ',' else -1])
        for rate in json_['rateDetail']['rateList']:
            rateContent = rate['rateContent']  # countent
            auctionSku = rate['auctionSku']  # size style
            self.lock.acquire()
            if self.nick_rate_msg.__contains__(nick):
                # same content
                if self.nick_rate_msg[nick].__contains__((rateContent, auctionSku)):
                    return
                print(rateContent + '---' + auctionSku)
                self.nick_rate_msg[nick].append((rateContent, auctionSku))
            else:
                self.nick_rate_msg[nick] = [(rateContent, auctionSku)]
            self.lock.release()

    def __get_contents__(self, nick, url):
        pageNum = 0
        last_data = None
        print('url ==========================' + url)
        while(True):
            data = get_data(url.replace('{num}', str(pageNum)))
            pageNum += 1
            if data and data != last_data:
                last_data = data
                self.__get_content__(nick, data)
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
        self.pages = [url.replace('{pageNum}', str(44 * i)) for i in range(100)]
    
    def __get_one_page_shops__(self):
        self.lock.acquire()
        page = None
        while len(self.pages) > 0:
            page = self.pages.pop()
            if page:
                data = get_data(page)
                try:
                    data = re.findall(r'"itemlist":(.+?),"bottomsearch"', data)[0]
                    data = data.replace('class="icon-text-1111-stock"', 'class=\'icon-text-1111-stock\'')
                    json_ = json.loads(data)
                    shop_item = json_['data']['auctions']
                    for shop in shop_item:
                        self.__shops__.append((shop['nick'], shop['nid'], shop['user_id']))
                except:
                    pass
        self.lock.release()
    
    def start(self):
        self.lock = threading.Lock()
        start_time = time.time()
        thread_list = [threading.Thread(target=self.__get_one_page_shops__) for t in range(8)]
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        print('has get %d shops.....cost %ds' % (len(self.__shops__), (time.time() - start_time)))
        return self.__shops__

    
def start(search_data):
    s = shop(search_data)
    shops = s.start()
    c = content(shops)
    c.start()


if __name__ == '__main__':
    start('%E6%96%87%E8%83%B8')
