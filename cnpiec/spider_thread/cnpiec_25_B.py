
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import random
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        if num == 0:
            url = "http://zbb.njau.edu.cn/pservices/index.jhtml"
        else:
            url = "http://zbb.njau.edu.cn/pservices/index_" + str(num + 1) + ".jhtml"

        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        dl_tag = soup.find("dl", class_="llist")
        for dd_tag in dl_tag.find_all("dd", cid="4"):
            url_n = dd_tag.find("a")["href"]
            date = dd_tag.find("span").text
            self.set_list(urls, url_n, date)
        return urls


class thrid(ss.EndSpider):
    def get(self, url):
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        tag = soup.find("div", class_="lright cright")
        text = tag.find_all(attrs={'class': 'ccontent'})[0].get_text().strip()
        title = tag.find("h1").get_text()
        self.set_text(text)
        self.set_title(title)