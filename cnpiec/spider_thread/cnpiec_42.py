
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss


class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url = "http://czj.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=40&perpage=10"
        data = {
            'col': '1',
            'appid': '1',
            'webid': '7',
            'path': '/',
            'columnid': '2399',
            'sourceContentType': '1',
            'unitid': '7729',
            'webname': '盐城市财政局',
            'permissiontype': '0'
        }
        r = requests.post(url, data=data)
        s = BeautifulSoup(r.text, 'html.parser')
        for i in s.find_all('record'):
            soup = BeautifulSoup(i.get_text(), 'html.parser')

            title = soup.find('a').get_text()
            date = soup.find_all('td')[1].get_text().replace(' ', '')
            url_n = "http://czj.yancheng.gov.cn" + soup.find('a').get('href') + "##" + title
            print(url_n, title, date)
            self.set_list(urls,url_n,date)
        return urls

class thrid(ss.EndSpider):
    def get(self,url):
        title = url.split('##')[1]
        r= requests.get(url.split('##')[0])
        s = BeautifulSoup(r.text,'html.parser')
        try:
            text = s.find(attrs={'class': 'cas_content'}).get_text().strip()
            text = "".join(text.split())
        except:
            text = "empty"


        self.set_title(title)
        self.set_text(text)

