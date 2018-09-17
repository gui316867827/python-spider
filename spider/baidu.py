'''
Created on 2018年7月5日


@author: F-Monkey
'''
from selenium.webdriver.common.by import By
from pytesseract import image_to_string
from PIL import Image
from time import sleep
from spider import driver
import io
import pytesseract

class baiduDriver(driver):
    xiangqin_bar = 'https://tieba.baidu.com/f?kw=%E7%9B%B8%E4%BA%B2&ie=utf-8'

    def __init__(self, headless=False, waitTime=None, waitFrequency=None, forbidden_pic=False, forbidden_js=False):
        driver.__init__(self, headless=headless, waitTime=waitTime, waitFrequency=waitFrequency, forbidden_pic=forbidden_pic, forbidden_js=forbidden_js)
        self.browser.get(self.xiangqin_bar)
        self._login_()

    def _login_(self):
        login_xpath = '//*[@id="com_userbar"]/ul/li[4]/div/a'
        self.find(By.XPATH, login_xpath, need_wait=True).click()

        user_login_id = 'TANGRAM__PSP_11__footerULoginBtn'
        self.find(By.ID, user_login_id, need_wait=True).click()

        username_id = 'TANGRAM__PSP_11__userName'
        password_id = 'TANGRAM__PSP_11__password'
        submit_btn_id = 'TANGRAM__PSP_11__submit'
        self.find(By.ID, username_id, need_wait=True).send_keys('12345')
        self.find(By.ID, password_id, need_wait=False).send_keys('43223')
        self.find(By.ID, submit_btn_id, need_wait=False).click()
        self._save_img()

    def _save_img(self):
        print('save.....')
        verifyCodeImg_id = 'TANGRAM__PSP_11__verifyCodeImg'
        img = self.find(By.ID, verifyCodeImg_id, need_wait=True)
        img_src = ''
        while(True):
            sleep(0.5)
            img_src = img.get_attribute('src')
            if 'https://passport.baidu.com/passApi/img/small_blank.gif' != img_src and img_src != '':
                break
        self.browser.viewportSize = {'width':2048, 'height':1600}
        self.browser.maximize_window()
        # 全截图
        screenshot_as_png = self.browser.get_screenshot_as_png() 
        # 截图 、 截图
        left = img.location['x']
        top = img.location['y']
        right = img.location['x'] + img.size['width']
        bottom = img.location['y'] + img.size['height']
        im = Image.open(io.BytesIO(screenshot_as_png))
        im = im.crop((left, top, right, bottom))
        filename = 'demo.png'
        im.save(filename)
        print('save end...')
        analysisPic(filename)
        self.browser.quit()


def analysisPic(img_path):
    '''
    response = requests.get(img_path)
    im = Image.open(BytesIO(response.content))
    '''
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    im = Image.open(img_path)
    # 图片去边
    width = im.size[0]
    height = im.size[1]
    left = 4
    top = 4
    right = width - 4
    bottom = height - 4 
    box = (int(left), int(top), int(right), int(bottom))
    im = im.crop(box)
    im = im.resize((width * 4, height * 4), Image.BILINEAR)
#     im.save('demo.png')
    
    # 图片灰度处理
    imgray = im.convert('L')
#     imgray.save('demo_gray.png')
    
    # 图片降噪
    threshold = 150
    table = [] 
    for i in range(256): 
        if i < threshold: 
            table.append(0) 
        else: 
            table.append(1) 
    out = imgray.point(table, '1')
#     out.save('demo_threshold.png')
    s = image_to_string(imgray)
    print(s)
    return s

'''
Created on Aug 15, 2018

@author: tangjf
'''

from selenium.webdriver.common.by import By
from spider import driver


class tieba(driver):
    url = 'https://www.baidu.com/'
    
    def __login__(self):
        login_btn_xpath = '//*[@id="u1"]/a[7]'
        user_login_btn_ID = 'TANGRAM__PSP_10__footerULoginBtn'
        self.find(By.XPATH, login_btn_xpath).click()
        self.find(By.ID, user_login_btn_ID).click()
        username_id = 'TANGRAM__PSP_10__userName'
        password_id = 'TANGRAM__PSP_10__password'
        submit_id = 'TANGRAM__PSP_10__submit'
        self.find(By.ID, username_id).send_keys('')
        self.find(By.ID, password_id, False).send_keys('')
        self.find(By.ID, submit_id, False).click()
        send_msg_ID = 'TANGRAM__36__button_send_mobile'
        self.find(By.ID, send_msg_ID).click()
        value = input('msg:')
        msg_input = 'TANGRAM__36__input_vcode'
        self.find(By.ID, msg_input).send_keys(value)
        
    def __init__(self, headless=False, waitTime=None, waitFrequency=None, forbidden_pic=False, forbidden_js=False):
        driver.__init__(self, headless=headless, waitTime=waitTime, waitFrequency=waitFrequency, forbidden_pic=forbidden_pic, forbidden_js=forbidden_js)
        self.browser.get(self.url)
        self.__login__()
    
    def delete(self, url):
        self.browser.get(url)


if __name__ == '__main__':
    t = tieba()
    t.delete('https://tieba.baidu.com/p/5840862909')

if __name__ == '__main__':
    bd = baiduDriver()
