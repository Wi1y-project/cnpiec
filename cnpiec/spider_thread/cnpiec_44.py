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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '__jsluid=cdbe8980f44c3f2a849e3f8f3c4c5988; bdshare_firstime=1546493177823; UM_distinctid=168976880f6620-0ee4fc0893ef7f-5d1f3b1c-1fa400-168976880f7341; CNZZDATA320139=cnzz_eid%3D1952083056-1548725175-%26ntime%3D1548725175; reg_referer="aHR0cDovL3d3dy5iaWRjaGFuY2UuY29tLw=="; Hm_lvt_2751005a6080efb2d39109edfa376c63=1550545270,1552894935; __jsl_clearance=1552977869.104|0|2Toj8oXwncDt0GX0g32KSI%2FknNc%3D; JSESSIONID=C8356F4BAD0B0D989526C841752C7502; Hm_lpvt_2751005a6080efb2d39109edfa376c63=1552977979',
        'Host': 'www.bidchance.com',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://www.bidchance.com/freesearch.do?&filetype=&channel=gonggao&currentpage=0&searchtype=sj&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    def get(self,num):
        
        urls = []
        
        url = 'http://www.bidchance.com/freesearch.do?&filetype=&channel=gonggao&currentpage='+str(num)+'&searchtype=sj&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment='
        r = requests.get(url,headers = self.headers)
        s = BeautifulSoup(r.text, "html.parser")

        for a in s.find_all(attrs = {'class':'datatr'}):
            

            url_n = 'http:' + a.find('a').get('href')
            map[url_n] = a.find('a').find('span').get_text()
            date = a.find_all('td')[3].get_text()
            self.set_list(urls,url_n,date,a.find('a').find('span').get_text())
            
        return urls

        

class thrid(ss.EndSpider):
    def get(self,url):

        text = 'empty'
        self.set_text(text)


