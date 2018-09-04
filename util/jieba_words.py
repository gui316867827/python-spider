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

def init():
    global jiebaSource
    jiebaSource = os.getcwd()
    jieba.load_userdict(jiebaSource + '/jieba_dict')
    

def analysisContent(content):
    extract_tags = analyse.extract_tags(sentence=content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'nr'), withFlag=True)
    for tag in extract_tags:
        print(tag)

    
def analysisWords(content):
    return pseg.cut(content)

def __create__(text,pic_path):
    if str(platform.system()).lower() == 'windows':
        font_path = 'C:/Windows/Fonts/STFANGSO.ttf'
    else:
        font_path = '/usr/share/fonts/win/msyh.ttf'
    mask = imread(jiebaSource+'/back.jpg')  # 读取背景图片
    wordcloud = WordCloud(
                mask=mask,
                background_color='white',
                max_font_size=240,
                random_state=180,
                font_path=font_path).generate(text)
    wordcloud.to_file(pic_path)
    
def createWordCloud(contents,lazy=True):
    word_list = [" ".join(jieba.cut(sentence)) for sentence in contents]
    new_text = ' '.join(word_list)
    result_pic = str(uuid.uuid1()) + '.png'
    if lazy:
        t = threading.Thread(target=__create__,args=(new_text, result_pic,))
        t.start()
    else:
        __create__(new_text, result_pic) 
    return os.path.abspath(result_pic)

