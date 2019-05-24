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
            url="http://www.ccgp.gov.cn/zydwplcg/zy/zyzb/index.htm"
        else:
            url="http://www.ccgp.gov.cn/zydwplcg/zy/zyzb/index_" + str(num)+".htm"
        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        ul_tag = soup.find("ul", class_="ulst")
        li_tags = ul_tag.find_all("li")
        for li_tag in li_tags:
            a = li_tag.find("a")
            url_n = "http://www.ccgp.gov.cn" + a["href"][8:]
            string = li_tag.text
            start = string.index("日期：")
            end = string.index("地域：")
            date = string[start + 3:end-6].strip()
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
        print(title)
        print(text)
        self.set_title(title)
        self.set_text(text)

if __name__ == '__main__':
    url="http://www.ccgp.gov.cn/cggg/zygg/gkzb/201811/t20181129_11229095.htm"
    # print(first(None).get(0))
    thrid(None).get(url)