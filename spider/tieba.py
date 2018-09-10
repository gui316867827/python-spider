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
