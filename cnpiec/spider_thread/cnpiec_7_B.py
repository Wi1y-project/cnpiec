from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import time

map = {}
def get_html(url):
    '''
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'PortalCookie=jTCTpTETttqIwcX_t4BcgKRCoKVR1XgHPDBah0gbbEFKlhQdzvg3!-1271392995',
        'Host':'www.gdgpo.gov.cn',
        'If-Modified-Since':'Tue, 19 Mar 2019 01:01:43 GMT',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

    }
    '''
    data = requests.get(url)
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        url = 'http://www.gdgpo.gov.cn/queryMoreCityCountyInfoList2.do'
        data = {
            'channelCode': '00051',
            'pointPageIndexId': '1',
            'pageIndex': str(num + 1),
            'pageSize': '15'
            #'pointPageIndexId': '1'
        }
        r = requests.post(url,data = data)
        r.encoding = 'utf-8'
        s = BeautifulSoup(r.text,'html.parser')
        #print (s.find(attrs = {'class':'m_m_c_list'}))
        for i in s.find(attrs = {'class':'m_m_c_list'}).find_all('li'):

            date = i.find('em').get_text().split(' ')[0].strip()
            for a in i.find_all('a'):
                if 'showNotice' in a.get('href'):

                    title = a.get('title')
                    temp = 'http://www.gdgpo.gov.cn' + a.get('href')
                    url_n =temp
                    map[temp]= title

                    self.set_list(urls,url_n,date)
        return urls

        


class thrid(ss.EndSpider):
    def get(self,url):
        title =map[url]


        text = "empty"

        self.set_text(text)
        self.set_title(title)
