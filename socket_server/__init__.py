import socket
import time
import json
import re
import jieba
from spider import baiduTieba
from util import jieba_words


def baiduTiebaSpider(json_data):
    response_temp = {}
    data = json.loads(json_data)
    print(data)
    if data and re.match(r'^https?:/{2}\w.+$', data['url']):
        startTime = int(time.time())
        all_user_contents = baiduTieba.start(data['url'])
        response_temp['status'] = 'success'
        response_temp['data'] = all_user_contents
        contents = []
        for content_list in all_user_contents.values():
            contents += content_list
        response_temp['frequency_count'] = jieba_words.analysisWords(contents)
        try:
            response_temp['picPath'] = jieba_words.createWordCloud(contents)
        except Exception as ex:
            print(ex)
        print('spider end !!!  has cost %ds' % (int(time.time()) - startTime))
    else :
        response_temp['status'] = 'error'
        response_temp['message'] = 'spider error, cause request url:' + data
    return response_temp


class server():
    
    def init_source(self):
        jieba_words.init()
#        json.loads('/home/tangjf/programs/workspace/python/webapp_spider/socket_server/headers.json')
    
    def __init__(self, address='localhost', port=8888):
        self.re_compire = re.compile('https://tieba.baidu.com/p/\/d')
        self.sk = socket.socket()
        self.sk.bind((address, port))
        self.sk.listen(5)
        self.init_source()

    def start(self):
        while True:
            conn, client_address = self.sk.accept()
            print('client_address:%s' % (str(client_address)))
            data = str(conn.recv(1024), encoding='utf8')
            conn.send(bytes(str(json.dumps(baiduTiebaSpider(data), ensure_ascii=False)), encoding="utf8"))
            conn.close()
    
    
if __name__ == '__main__':
    s = server()
    s.start()
