import requests
import cnpiec.spider_modules.standard_spider as ss
from bs4 import BeautifulSoup


def get_html(url):

    data = requests.get(url, timeout=20)

    data.encoding = 'utf-8'
    data = data.text
    return data


class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        if num == 0:
            url = 'http://www.ccgp.gov.cn/cggg/dfgg/index.htm'
        else:
            url = 'http://www.ccgp.gov.cn/cggg/dfgg/index_'+str(num)+'.htm'
        s = BeautifulSoup(get_html(url), 'html.parser')
        div = s.find(attrs={'class': 'c_list_bid'})
        for item in div.find_all('li'):
            title = item.find('a').get_text()
            url_n = 'http://www.ccgp.gov.cn/cggg/dfgg' + item.find('a').get('href').replace('./', '/')
            date = item.find_all('em')[1].get_text().split(' ')[0]
            self.set_list(urls, url_n, date, title)

        return urls


class thrid(ss.EndSpider):
    def get(self, url):
        text = 'empty'
        self.set_text(text)

