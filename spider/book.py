from selenium.webdriver.common.by import By
import re
import threadpool
from spider import driver, staticSource


class bookPage(staticSource):
    source = 'https://www.qisuu.la'
    
    def __init__(self):
        return staticSource.__init__(self, self.source)
    
    def _get_img(self, tag, ss):
        if tag.has_attr('src') and ss[len(ss) - 1] in tag.get_attr('src'):
            return True
        return False
    
    def _get(self, url):
        try:
            result = re.findall(r'get_down_url\((.+?)\)', str(self.soup.find('script', text=re.compile(r'get_down_url?.*')).text))[0]
            ss = re.findall(r'\d+\.?\d*', url.replace('.html', ''))
            imgs = self.soup.find_all('img')
            filter(lambda tag:self._get_img(tag, ss), imgs)
            src = imgs[1]['src']
            if self.source not in src :
                src = self.source + src
            print(result + ",'" + str(src) + "'")
            return result
        except:
            print(url)
            pass
        return None
    
    def get(self):
        pool = threadpool.ThreadPool(10)
        requests = threadpool.makeRequests(self._get, self.urls)
        [pool.putRequest(req) for req in requests]
        pool.wait()

        
class bookDriver(driver):
    _url = 'https://www.qisuu.la/';
    _static_url = 'http://zhannei.baidu.com/cse/site/?cc=qisuu.la&q='
    
    def __init__(self, url, waitTime=None, waitFrequency=None, forbidden_pic=False, forbidden_js=False):
        driver.__init__(self, url, waitTime=waitTime, waitFrequency=waitFrequency, forbidden_pic=forbidden_pic, forbidden_js=forbidden_js)
    
    def search(self, bookName):
        self.browser.get(self._static_url + bookName);
        results = self.find(By.ID, 'results')
        return bookPage(map(lambda b: str(b.get_attribute('href')), results.find_elements_by_xpath('div/h3/a'))).get()
    