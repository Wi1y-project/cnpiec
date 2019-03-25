from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import time


map = {}
def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '41',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': 'acw_tc=76b20f6015528955498484081e4a4c3788f9a0430e728fc5cc7ffb382116a7;JSESSIONID=77B2961332F402B631223825736BE3F2;USERLINK="TUQLAaawW/uVhnHut5AmuBfCn3diy4gbiXOyU3edT3ZNjtbm6+fEN0p8lBbqj2cXsHXmpIOULV7xFuCcVxnWVX4gkXhYyfXtA2xKJosUv1g=";SERVERID=886986a9686308421963ad416c44c990|1552897317|1552895549',
        'Host': 'sale.scbid.net',
        'Origin': 'http://sale.scbid.net',
        'Referer': 'http://sale.scbid.net/projectListPage?nature=2',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.121Safari / 537.36'

    }
    def get(self, num):

        urls = []

        url = 'http://sale.scbid.net/queryProjectInfo'


        data = {
            'projectName': '',
            'projectNature': '2',
            'pageNumber': str(num + 1)
        }
        r = requests.post(url, data=data, headers=self.headers)
        for item in r.json()['rowList']:
            title = item['projectName']
            date = item['bidBookStartTimeStr'].split(" ")[0]
            url_n = 'http://sale.scbid.net:80/saleProject/projectDetailPage?projectId=' + item['listId']
            map['http://sale.scbid.net:80/saleProject/projectDetailPage?projectId=' + item['listId']] = title
            self.set_list(urls,url_n,date)
        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        title = map[url]
        text = "empty"

        self.set_text(text)
        self.set_title(title)

