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
        url = 'http://www.hzctc.cn/SecondPage/GetNotice'
        data = {
            'area': '',
            'afficheType': '27',
            'IsToday': '',
            'title': '',
            'proID': '',
            'number': '',
            '_search': 'false',
            'nd': '1548384059780',
            'rows': '10',
            'page': str(num + 1),
            'sidx': 'PublishStartTime',
            'sord': 'desc'
        }
        r = requests.post(url,data = data)
        j = r.json()
        for i in j['rows']:
            print ('http://www.hzctc.cn/AfficheShow/Home?AfficheID=' + i['ID'] + '&IsInner=3&ModuleID=27')
            url_n = 'http://www.hzctc.cn/AfficheShow/Home?AfficheID=' + i['ID'] + '&IsInner=3&ModuleID=27'
            date = i['PublishStartTime'].split(' ')[0]
            self.set_list(urls,url_n,date)
        return urls

        


class second(ss.EndSpider):
    def get(self,url):

        html = get_html(url)
        s = BeautifulSoup(html, "html.parser")

        temp = " ".join(s.find(attrs = {'class':'AfficheTitle'}).get_text().strip().split())
        title = temp.split(' ')[0]
        date = temp.split(' ')[1]
        text = s.find(attrs={'class':'MainList'}).get_text().strip()
        text = "".join(text.split())

        self.set_text(text)
        self.set_title(title)
        
