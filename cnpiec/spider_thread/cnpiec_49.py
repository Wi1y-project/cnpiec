from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import datetime


def get_html(url):

    data = requests.get(url)
    data.encoding = 'utf-8'
    return data.text


def getyesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return str(yesterday).replace('-', ':')

class first(ss.StartSpider):

    def get(self,num):
        urls = []
        request_date = getyesterday()
        url = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index="+str(num + 1)+"&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=" + str(
            request_date) + "&end_time=" + str(request_date) + "&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName="

        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        ul_tag = soup.find("div", class_="vT-srch-result-list")
        li_tags = ul_tag.find_all("li")
        for li_tag in li_tags:
            a = li_tag.find("a")
            url_n = a["href"]
            title = a.text.strip()
            date = '2019-12-10'
            print(url_n, date, title)
            self.set_list(urls,url_n,date)

        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        head = soup.find("div", class_="vF_detail_main")
        title = head.find("h2").text.strip()
        text = soup.find("div", class_="table").text

        self.set_title(title)
        self.set_text(text)

