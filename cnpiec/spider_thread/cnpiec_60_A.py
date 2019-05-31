import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss



def get_html(url):

    data = requests.get(url)
    data.encoding = 'utf-8'
    data = data.text
    return data


class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        url = 'http://www.gxzfcg.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cggg/param_bulletin/20/page_'+str(num)+'.html'
        s = BeautifulSoup(get_html(url), 'html.parser')
        div = s.find(attrs={'class': 'column infoLink noBox unitWidth_x6'})
        for i in div.find_all('li'):
            url_n = i.find('a').get('href')
            url_n = 'http://www.gxzfcg.gov.cn' + url_n
            date = i.find(attrs={'class': 'date'}).get_text()
            self.set_list(urls, url_n, date)

        return urls


class thrid(ss.EndSpider):
    def get(self, url):

        s = BeautifulSoup(get_html(url), 'html.parser')
        title = s.find(attrs={'class': 'reportTitle'}).find('h1').get_text()
        text = s.find(attrs={'class': 'frameReport'}).get_text()
        text = ' '.join(text.split())

        self.set_text(text)
        self.set_title(title)

