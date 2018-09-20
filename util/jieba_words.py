'''
Created on Sep 1, 2018

@author: F-Monkey
'''

import jieba
import jieba.posseg as pseg
from jieba import analyse
from scipy.misc import imread
from wordcloud.wordcloud import WordCloud
import uuid
import os
import platform
import threading
from collections import Counter
import json


def init():
    global jiebaSource
    jiebaSource = os.getcwd()
    jieba.load_userdict(jiebaSource + '/jieba_dict')
    

def analysisContent(content):
    extract_tags = analyse.extract_tags(sentence=content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'nr'), withFlag=True)
    for tag in extract_tags:
        print(tag)
        
def parse_word_list(contents):
    if type(contents) is list:
        return ' '.join(contents)
    else:
        return contents

    
def parse_words(sentence):
    jieba.load_userdict('jieba_dict')
    seg_list = pseg.cut(sentence)
    for (k, v) in seg_list:
        print(str(k) + '---' + str(v))
    
def analysisWords(contents):
    content = parse_word_list(contents)
    seg_list = pseg.cut(content)
    c = Counter()
    result_dict = {}
    for (k, v) in seg_list:
        if len(k) > 0 and k != '\t' and k != '\n' and v != 'x':
            c[k] += 1
    for (k, v) in c.most_common(20):
        result_dict[k] = v
    return json.dumps(result_dict, ensure_ascii=False)

def __create__(text, pic_path):
    if str(platform.system()).lower() == 'windows':
        font_path = 'C:/Windows/Fonts/STFANGSO.ttf'
    else:
        font_path = '/usr/share/fonts/win/msyh.ttf'
    mask = imread(jiebaSource + '/back.jpg')  # 读取背景图片
    wordcloud = WordCloud(
                mask=mask,
                background_color='white',
                max_font_size=240,
                random_state=180,
                font_path=font_path).generate(text)
    wordcloud.to_file(pic_path)


def createWordCloud(contents, lazy=True):
    word_list = [" ".join(jieba.cut(sentence)) for sentence in contents]
    new_text = parse_word_list(word_list)
    result_pic = str(uuid.uuid1()) + '.png'
    if lazy:
        t = threading.Thread(target=__create__, args=(new_text, result_pic,))
        t.start()
    else:
        __create__(new_text, result_pic) 
    return os.path.abspath(result_pic)

if __name__ == '__main__':
    parse_words('我想去阿里巴巴西溪园区1号楼1楼')

    #analysisWords('楼主天天看吧里大家的相亲经历，也来分享一下自己的相亲经历吧。由于事情已经过去一段时间了，肯定没有当时的聊天记录了。相亲女的照片大多我都删了，如果大家想看，我在电脑里找找，能发就发一下。')
