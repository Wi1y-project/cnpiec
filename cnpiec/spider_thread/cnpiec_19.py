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
        url = 'http://zb.ccnu.edu.cn/portal/topicView.do?method=view&id=3832576'
        
        data = {
            'ec_i': 'topicChrList_20070702',
            'topicChrList_20070702_crd': '50',
            'topicChrList_20070702_f_a':'',
            'topicChrList_20070702_p': str(num + 1),
            'topicChrList_20070702_s_name':'',
            'topicChrList_20070702_s_topName': '',
            'id': '3832576',
            'id': '3832576',
            'topicChrList_20070702_rd': '50',
            'topicChrList_20070702_f_name': '',
            'topicChrList_20070702_f_topName': '',
            'topicChrList_20070702_f_ldate': ''
        }
        r = requests.post(url,data = data)
        s = BeautifulSoup(r.content, "html.parser")
        for a in s.find_all('a'):
            try:
                if 'viewer' in a.get('href'):
                    #print ('http://zb.ccnu.edu.cn' + a.get('href') + '##' +a.get_text() + '##'+ a.find_parent().find_parent().find_all('td')[3].get_text().split(' ')[0])
                    url_n = 'http://zb.ccnu.edu.cn' + a.get('href')
                    date = url_n.split('##')[2]
                    map['http://zb.ccnu.edu.cn' + a.get('href') + '##' +a.get_text()] = a.get_text()
                    self.set_list(urls,url_n,date)

            except:
                pass
            
        return urls

        


class thrid(ss.EndSpider):
    def get(self,url):

        title = map[url]

        text = 'empty'

        self.set_text(text)
        self.set_title(title)
        

