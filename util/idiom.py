'''
Created on Sep 19, 2018

@author: F-Monkey
'''
from pytesseract.pytesseract import image_to_string


def parseImg(img):
    s = image_to_string(img)
    return s.items()


def parseContent(content):
    return list(filter(lambda x: x != '' and x != '\n' and x != '\t', [s.strip() for s in content]))


if __name__ == '__main__':
    s = ''
    print(parseContent(s))
