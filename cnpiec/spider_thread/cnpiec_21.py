
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import datetime
import random
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        if num==0:
            url = "http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/index.html"
        else:
            url = "http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/index_" + str(num)+".html"


        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        num = re.search("/index", url).span()[0]
        url = url[:num]
        div = soup.find("div", class_="list_list")
        if div is None:
            div = soup.find("div", class_="list_list02")
        for li_tag in div.find_all("li"):

            a_tag = li_tag.find("a")["href"]
            url_n = url + a_tag[1:]
            [s.extract() for s in li_tag('a')]
            date =li_tag.text.strip()
            if date== "":
                date= str(datetime.datetime.now().date())

            self.set_list(urls,url_n,date)
        return urls




class thrid(ss.EndSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        title = soup.find("h1").get_text().strip().replace("\n", "")
        text = soup.find("div", class_="detail_con").get_text().strip().replace("\n", "")
        self.set_title(title)
        self.set_text(text)


