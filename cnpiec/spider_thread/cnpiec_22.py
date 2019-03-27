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
        #url = 'http://cg.hzft.gov.cn/www/noticelist.do'
        if num == 0:
            url = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cgyg/index.html'
        else:
            url = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cgyg/index_'+ str(num) + '.html'
        
        soup = BeautifulSoup(get_html(url),'html.parser')

        div = soup.find(attrs={'class':'list_list'})
        for li in div.find_all('li'):

            url_n = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cgyg' + li.find('a').get('href').replace('./', '/')
            date = li.get_text().split('\n')[2].strip()
            self.set_list(urls,url_n,date)
        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find('h1').get_text().strip()
        date = soup.find(attrs={'class':'mid'}).get_text().strip().split('发布时间:')[1].split(' ')[0].strip()
        text = soup.find(attrs={'class':'detail_con'}).get_text().strip()
        text = "".join(text.split())
        self.set_text(text)
        self.set_title(title)

        





