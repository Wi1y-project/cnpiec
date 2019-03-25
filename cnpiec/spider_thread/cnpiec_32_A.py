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
        url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp'
        data = {
            'subject':'',
            'pdate': '',
            'areacode':'',
            'unitname': '',
            'kindof':'', 
            'projectname':'', 
            'projectcode':'', 
            'colcode': '0301',
            'curpage': str(num + 1)
        }
        r = requests.post(url,data = data)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'html.parser')

        div = soup.find_all(attrs={'class':'aa'})
        for a in div:
            url_n = 'http://www.ccgp-shandong.gov.cn' + a.get('href')
            date = a.find_parent().get_text().split('\n')[3]
            self.set_list(urls,url_n,date)
        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        html = get_html(url)

        try:
            soup = BeautifulSoup(html, "html.parser")


            title = soup.find(attrs={'class':'aa'}).find_all('div')[0].get_text().strip()
        except:
            title="现邀请你公司参加报价"
        try:
            date = soup.find(attrs={'class':'aa'}).get_text().strip().split('发布时间：')[1].split(' ')[0].replace('年','-').replace('月','-').replace('日','')
        except:
            date = "None"

        text = soup.find(attrs={'class':'aa'}).get_text().strip()
        text = "".join(text.split())
        self.set_text(text)
        self.set_title(title)