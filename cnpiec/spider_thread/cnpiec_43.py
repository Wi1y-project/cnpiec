
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss


class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url = 'https://www.ynggzy.com/jyxx/jsgcZbgg'
        data = {
            'currentPage': str(num + 1),
            'area': '000',
            'industriesTypeCode': '0',
            'scrollValue': '1101',
            'tenderProjectCode': '',
            'bulletinName': ''
        }
        r = requests.post(url, data=data)
        s = BeautifulSoup(r.text, 'html.parser')
        for a in s.find_all('a'):
            try:
                if 'Detail?' in a.get('href'):

                    title = a.get('title')
                    date = a.parent.parent.find_all('td')[3].get_text()
                    url_n = 'https://www.ynggzy.com' + a.get('href') + '##' + title
                    self.set_list(urls, url_n, date)

            except:
                pass

        return urls

class thrid(ss.EndSpider):
    def get(self,url):
        title = url.split('##')[1]
        r = requests.get(url.split('##')[0])
        s = BeautifulSoup(r.text,'html.parser')
        text = s.find(attrs={'class': 'detail_contect'}).get_text().strip()
        text = "".join(text.split())

        self.set_title(title)
        self.set_text(text)
