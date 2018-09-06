import socket
import time
import json
import re
import jieba
from util import jieba_words


def create_success_response():
    response_temp = {}
    response_temp['status'] = 'success'
    return response_temp


def create_error_response(data):
    response_temp = {}
    response_temp['status'] = 'error'
    response_temp['message'] = 'spider error, cause request data:' + str(data)
    return response_temp


def spider_runner(json_data):
    data = json.loads(json_data)
    try:
        runner = __import__('spider.' + data['actionType'], fromlist=True)
    except Exception as ex:
        print(ex)
        return create_error_response(data)
    if data and re.match(r'^https?:/{2}\w.+$', data['url']):
        startTime = int(time.time())
        all_user_contents = runner.start(data['url'])
        response_temp = create_success_response()
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
        return response_temp
    else :
        return create_error_response(data)


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
            conn.send(bytes(str(json.dumps(spider_runner(data), ensure_ascii=False)), encoding="utf8"))
            conn.close()
    
    
if __name__ == '__main__':
    s = server()
    s.start()
