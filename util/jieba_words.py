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

global jiebaSource

def init():
    jiebaSource = os.getcwd()
    jieba.load_userdict(jiebaSource + '/jieba_dict')
    

def analysisContent(content):
    extract_tags = analyse.extract_tags(sentence=content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'nr'), withFlag=True)
    for tag in extract_tags:
        print(tag)

    
def analysisWords(content):
    return pseg.cut(content)
   
    
def createWordCloud(contents):
    word_list = [" ".join(jieba.cut(sentence)) for sentence in contents]
    new_text = ' '.join(word_list)
    coloring = imread(jiebaSource+'/back.jpg')  # 读取背景图片
    uuid_1 = uuid.uuid1()
    result_pic = str(uuid_1) + '.png'
    fontname = '/usr/share/fonts/win/msyh.ttf'
    wordcloud = WordCloud(
        mask=coloring,
        background_color='white',
        max_font_size=240,
        random_state=180,
        font_path=fontname).generate(new_text)
    wordcloud.to_file(result_pic)
    return os.path.abspath(result_pic)

