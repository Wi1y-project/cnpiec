from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import time



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        
        if num == 0:
            url = 'http://www.gzsggzyjyzx.cn/jygkgycq/index.jhtml'
        else:
            url = 'http://www.gzsggzyjyzx.cn/jygkgycq/index_' + str(num) + '.jhtml'
        r = requests.get(url)
        r.encoding = 'utf-8'
        s = BeautifulSoup(r.text,'html.parser')
        div = s.find(attrs = {'class':'article_listbox'})
        for i in div.find_all('li'):
             
            url_n = i.find('a').get('href')
            date = i.find_all('span')[1].get_text()
            self.set_list(urls,url_n,date)
        return urls

class thrid(ss.EndSpider):
    def get(self,url):
        
        html = get_html(url)
        
        s = BeautifulSoup(html, "html.parser")

        title = s.find(attrs = {'class':'article_head'}).get_text().strip()
        date = s.find(attrs = {'class':'article_subtitle'}).find('span').get_text().strip().replace('发布时间：','').split(' ')[0]
        text = s.find(attrs={'class':'detail_box'}).get_text().strip()
        text = "".join(text.split())
        self.set_text(text)
        self.set_title(title)
        



