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
        
        
        url = 'https://cg.uestc.edu.cn/f/list-16b1c59063ab42bd84c0ea4c56cfa16e.html?pageNo='+ str(num + 1) +'&pageSize=5'
        r = requests.get(url)
        r.encoding = 'utf-8'
        s = BeautifulSoup(r.text,'html.parser')
        ul = s.find(attrs = {'class':'frame_list_image'})
        for li in ul.find_all('li'):
            
            url_n = 'https://cg.uestc.edu.cn' + li.find('a').get('href')
            date = li.find(attrs = {'class':'time'}).get_text().replace('-','').replace('年','-').replace('月','-').replace('日','')
            self.set_list(urls,url_n,date)
        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")

        try:
            title = "".join(soup.find(attrs={'class':'MsoNormal'}).get_text().strip().split())
        except:
            title = soup.find(attrs={'class':'title'}).get_text().strip()
        date = soup.find(attrs={'class':'time'}).get_text().replace('年','-').replace('月','-').replace('日','-')
        
        text = soup.find(attrs={'class':'content'}).get_text().strip()
        text = "".join(text.split())

        self.set_text(text)
        self.set_title(title)

        

