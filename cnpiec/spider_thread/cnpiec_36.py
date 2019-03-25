from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import time



def get_html(url):
    headers = {
        'Cookie': '__jsluid=103538a88b629d026e15777eaa4718a5; JSESSIONID=77E8749F59C1A3881FE128B24D540B1C',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    data = requests.get( url ,headers = headers)
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):
    headers = {
        'Cookie': '__jsluid=103538a88b629d026e15777eaa4718a5; JSESSIONID=77E8749F59C1A3881FE128B24D540B1C',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    def get(self, num):

        urls = []

        url = 'http://www.zfcg.suzhou.gov.cn/content/queryContent.action'
        headers = {
            'Cookie': '__jsluid=103538a88b629d026e15777eaa4718a5; JSESSIONID=77E8749F59C1A3881FE128B24D540B1C',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        data = {
            'channelId': '8',
            'page': str(num + 1),
            'rows': '10',
            'title': '',
            'area': ''
        }
        r = requests.post(url, data=data, headers=headers)
        for item in r.json()['rows']:
            date = item['releaseTime'].split(' ')[0]
            url_n = 'http://www.zfcg.suzhou.gov.cn/html/content/' + item['cpContentId'] + ".shtml"

            self.set_list(urls,url_n,date)
        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find(attrs={'class': 'M_title'}).get_text().strip()
        text = soup.find(attrs={'class': 'Article'}).get_text().strip()
        text = "".join(text.split())

        self.set_text(text)
        self.set_title(title)

