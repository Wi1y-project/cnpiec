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

    def get(self,num):

        urls = []
        url = "http://zbb.nefu.edu.cn/sfw_cms/e"
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '298',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=41E3F06FD2F9DDFFC740185DEDBBE293; contextpath=%2Fsfw_cms',
            'Host': 'zbb.nefu.edu.cn',
            'Origin': 'http://zbb.nefu.edu.cn',
            'Referer': 'http://zbb.nefu.edu.cn/sfw_cms/e?page=cms.psms.gglist&typeDetail=XQ',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = {
            't_': '0.1558959636854571',
            'window_': 'json',
            'start': '1',
            'limit': '100',
            'filter': '',
            'sort': 'edate desc',
            # 'typePublish': 'ZC',
            # 'typePublish': 'YQ',
            # 'typePublish': 'CS',
            # 'typePublish': 'BY',
            # 'typePublish': 'BG',
            'typeDetail': 'XQ',
            'shoppingType': '',
            'notShoppingType': '',
            'isEnd': '',
            'categoryId': '4392',
            'keywords': '',
            'request_method_': 'ajax',
            'browser_': 'notmsie',
            'page': 'cms.psms.publish.query'
        }
        r = requests.post(url, data=data, headers=headers)
        for item in r.json()['resultset']:
            if item['businessName'] == None:
                continue
            title = item['businessName']
            date = item['createTime'].split(' ')[0]
            url_n = 'http://zbb.nefu.edu.cn/provider/#/publish/' + item['syncId']
            map['http://zbb.nefu.edu.cn/provider/#/publish/' + item['syncId']] = title
        

            self.set_list(urls,url_n,date)
        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        text = 'empty'
        title = map[url]

        self.set_text(text)
        self.set_title(title)

