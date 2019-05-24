from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import datetime


class first(ss.StartSpider):

    def get(self,num):
        urls = []
        if num == 0:
            url="http://htgs.ccgp.gov.cn/GS8/contractpublish/index"
        else:
            url="http://htgs.ccgp.gov.cn/GS8/contractpublish/index_" + str(num + 2)
        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        ul_tag = soup.find("ul", class_="ulst")
        li_tags = ul_tag.find_all("li", style="height:60px")
        for li_tag in li_tags:
            a = li_tag.find("a")
            url_n = "http://htgs.ccgp.gov.cn/GS8/contractpublish" + a["href"][1:]
            string = li_tag.text
            start = string.index("发布时间：")
            end = string.index("地域：")
            date = string[start + 5:end].strip()
            self.set_list(urls,url_n,date)

        return urls




class thrid(ss.EndSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        head = soup.find("div", class_="vT_detail_header")
        title = head.find("h2").text.strip()
        text = soup.find("div", class_="vT_detail_content w900c").text
        self.set_title(title)
        self.set_text(text)


