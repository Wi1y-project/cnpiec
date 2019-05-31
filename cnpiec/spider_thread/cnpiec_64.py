import requests
import cnpiec.spider_modules.standard_spider as ss
from bs4 import BeautifulSoup


def get_html(url, data1, headers):

    data = requests.post(url, data=data1, timeout=20, headers=headers)

    data.encoding = 'utf-8'
    data = data.text
    return data


class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        url = 'http://www.ccgp-guizhou.gov.cn/article-search.html'
        data = {
            'siteId': '1',
            'category.id': '1153797950913584',
            'areaName': '',
            'tenderRocurementPm': '',
            'keywords': '',
            'articlePageNo': '2',
            'articlePageSize': '15'
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Cookie': 'gzprocurement.session.id=4225018076623282; __jsluid=4716fff97726d7cfb5d20610770fc6a8; JSESSIONID=F7F7EE67E876B577B6B6B3F754848736',
            'Host': 'www.ccgp-guizhou.gov.cn',
            'Origin': 'http://www.ccgp-guizhou.gov.cn',
            'Referer': 'http://www.ccgp-guizhou.gov.cn/list-1153797950913584.html?siteId=45234234657',
            'Upgrade-Insecure-Requests': '1'
        }

        s = BeautifulSoup(get_html(url, data1=data, headers=headers), 'html.parser')
        div = s.find(attrs={'class': 'xnrx'})
        for item in div.find_all('li'):
            title = item.find('a').get_text()
            date = item.find('span').get_text().replace('.', '-')
            url_n = 'http://www.ccgp-guizhou.gov.cn' + item.find('a').get('href')
            self.set_list(urls, url_n, date, title)

        return urls


class thrid(ss.EndSpider):
    def get(self, url):
        text = 'empty'
        self.set_text(text)

