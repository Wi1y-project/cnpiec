import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re


def get_html(url):

    data = requests.get(url)
    data.encoding = 'utf-8'
    data = data.text
    return data


class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        url = 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&moreType=provincebuyBulletinMore&channelCode=sjcg2&rp=25&page='+str(num)
        s = BeautifulSoup(get_html(url), 'html.parser')
        div = s.find(attrs={'class': 'info'})
        for i in div.find_all('li'):
            title = i.find('a').get('title')
            url_n = i.find('a').get('href').split('/view/')[1]
            url_n = 'http://www.ccgp-sichuan.gov.cn/view/' + url_n
            date2 = i.find('div').find('span').get_text()
            date_temp = i.find('div')
            date1 = re.sub(r'<span>.*</span>', "", str(date_temp))
            date1 = date1.replace('<div class="time curr">', '').replace('</div>', '').strip()
            date = date1 + '_' + date2
            self.set_list(urls, url_n, date, title)

        return urls


class thrid(ss.EndSpider):
    def get(self, url):
        text = 'empty'
        self.set_text(text)


