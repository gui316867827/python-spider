'''
Created on Sep 5, 2018

@author: F-Monkey
'''
from spider import get_data, emoji_pattern
import threading
import re
import json
import time
headers = {}
cookie = {}


class shop():

    def __init__(self, nick, shopId, sellerId):
        self.nick = nick
        self.shopId = shopId
        self.sellerId = sellerId

    def addContents(self, contents):
        self.contents = contents

    def __hash__(self):
        return hash(self.nick + self.sellerId + self.shopId)
    
    def __eq__(self, other):
        if type(other) == shop:
            return self.__hash__() == other.__hash__()
        return False

    def to_dict(self):
        data = {}
        data['nick'] = self.nick
        data['shopId'] = self.shopId
        data['sellerId'] = self.sellerId
        data['bras'] = self.contents
        return data

        
def parse_auctionSku(rateContent, auctionSku):
    data = {}
    data['rateContent'] = emoji_pattern.sub(r'', rateContent)
    if ';' in auctionSku:
        ss = auctionSku.split(';')
        style = ss[0].replace('颜色分类:', '')
        size = ss[1].replace('尺码:', '')
        data['color'] = style
        try:
            data['size'] = re.findall('(\d+)', size)[0]
            data['cup'] = size.replace(data['size'], '')
        except:
            data['size'] = size
    else:
        data['auctionSku'] = auctionSku
    return data


class content_runner():
    content_base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={nid}&sellerId={user_id}&currentPage={num}'
    nick_urls = {}
    nick_rate_msg = {}
    
    def __init__(self, shops):
        for (nick, nid, user_id) in shops:
            shop_content_url = self.content_base_url.replace('{nid}', nid).replace('{user_id}', user_id)
            s = shop(nick, nid, user_id)
            if self.nick_urls.__contains__(s):
                self.nick_urls[s].append(shop_content_url)
            else:
                self.nick_urls[s] = [shop_content_url]

    def __get_content_of_shop__(self):
        keys = list(self.nick_urls.keys())
        for s in keys:
            if self.nick_urls.__contains__(s):
                urls = self.nick_urls.pop(s)
                for url in urls:
                    self.__get_contents__(s, url)
            else:
                continue
    
    def __get_content__(self, s, data):
        json_ = json.loads(data.replace(r'jsonp128(', '')[:-2 if data[:-1] == ',' else -1])
        for rate in json_['rateDetail']['rateList']:
            self.lock.acquire()
            d = parse_auctionSku(rate['rateContent'], rate['auctionSku'])
            if self.nick_rate_msg.__contains__(s):
                # same content
                if self.nick_rate_msg[s].__contains__(d):
                    self.lock.release()
                    return
                self.nick_rate_msg[s].append(d)
            else:
                self.nick_rate_msg[s] = [d]
            self.lock.release()
    
    def __get_contents__(self, s, url):
        pageNum = 0
        last_data = None
        while(True):
            data = get_data(url.replace('{num}', str(pageNum)))
            if pageNum > 100:
                break
            pageNum += 1
            if data and data != last_data:
                last_data = data
                self.__get_content__(s, data)
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

        
class shop_runner():
    shops_base_url = 'https://s.taobao.com/search?data-value={pageNum}&ajax=true&callback={callback}&q={search_data}&s={pageNum}'
    call_back = 'jsonp1077'
    __shops__ = []

    def __init__(self, goodsName):
        url = self.shops_base_url.replace('{search_data}', goodsName).replace('{callback}', self.call_back);
        self.pages = [url.replace('{pageNum}', str(44 * i)) for i in range(15)]
    
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
                        data = (shop['nick'], shop['nid'], shop['user_id'])
                        if not self.__shops__.__contains__(data):
                            self.__shops__.append(data)
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
        self.__shops__ = list(set(self.__shops__))
        print('has get %d shops.....cost %ds' % (len(self.__shops__), (time.time() - start_time)))
        return self.__shops__

    
def start(search_data):
    s = shop_runner(search_data)
    shops = s.start()
    c = content_runner(shops)
    result = []
    nick_rate_msg = c.start();
    for shop in nick_rate_msg:
        shop.addContents(nick_rate_msg[shop])
        result.append(shop.to_dict())
    return result


import pymysql


def save_to_mysql(shops):
    for shop in shops:
        pymysql.connect("")


if __name__ == '__main__':
    for s in start('文胸'):
        print(s)
