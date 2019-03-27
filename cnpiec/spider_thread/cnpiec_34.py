from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import time


map = {}
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

        url = "http://www.zfcg.sh.gov.cn/news.do?method=purchasePracticeMore"

        data = {
            'ec_i': 'bulletininfotable',
            'bulletininfotable_efn': '',
            'bulletininfotable_crd': '100',
            'bulletininfotable_p': str(num + 1),
            'bulletininfotable_s_bulletintitle': '',
            'bulletininfotable_s_beginday': '',
            'findAjaxZoneAtClient': 'false',
            'flag': 'cggg',
            'bFlag': '00',
            'treenum': '05',
            'method': 'purchasePracticeMore',
            'bulletininfotable_totalpages': '2',
            'bulletininfotable_totalrows': '158',
            'bulletininfotable_pg': '1',
            'bulletininfotable_rd': '100'
        }
        r = requests.post(url, data=data)  #
        s = BeautifulSoup(r.text, 'html.parser')
        div = s.find(attrs={'id':'bulletininfotable_table_body'})
        for i in div.find_all("tr"):
            title = i.find('a').get_text()
            date = i.find_all('td')[2].get_text().split(' ')[0].replace('(', '')
            url_n = 'http://www.zfcg.sh.gov.cn/emeb_bulletin.do?method=showbulletin&bulletin_id=' + i.find('a').get('value')
            map['http://www.zfcg.sh.gov.cn/emeb_bulletin.do?method=showbulletin&bulletin_id=' + i.find('a').get('value')] = title

            self.set_list(urls,url_n,date)

        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        title = map[url]
        text = "empty"

        self.set_text(text)
        self.set_title(title)
