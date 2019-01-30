
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import random
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url = "http://www.hnggzy.com/hnsggzy/jyxx/002001/002001001/?Paging=" + str(num+1)

        data = requests.get(url)
        data.encoding = 'gb2312'
        data = data.text

        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", style="height:530px;")
        for tr_tag in div_tag.find_all("tr"):
            url_n = "http://www.hnggzy.com" + tr_tag.find("a")["href"]
            date = tr_tag.find_all("td")[2].text[1:-1]
            self.set_list(urls,url_n,date)
        return urls

class thrid(ss.EndSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'gb2312'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find_all("table", width="887")[0]
        title = table_tag.find_all("td", height="76")[0].get_text().strip().replace("\n", "")
        text = table_tag.find_all("td", style="padding:26px 40px 10px;")[0].get_text().strip()
        self.set_title(title)
        self.set_text(text)




