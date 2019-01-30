
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import random
import json




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url="http://new.zmctc.com/zjgcjy/jyxx/004001/004001002/?Paging="+str(num+1)
        header = {"User-Agent":
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        data = requests.get(url, headers=header)
        data.encoding = "UTF-8"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div = soup.find("div", align="center")
        for tr_tag in div.find_all("tr", height="30"):
            a = tr_tag.find("a")
            url_n = "http://new.zmctc.com" + a["href"]
            date = tr_tag.find("td", width="80").text[1:-1]
            self.set_list(urls,url_n,date)
        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        resq = requests.get(url, headers=header)
        resq.encoding = "UTF-8"
        data = resq.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find("table", id="tblInfo")
        td_tag = table_tag.find("td", id="tdTitle")
        t_font = td_tag.find("font", style="font-size: 25px")
        title = t_font.text.strip()
        text = "".join(table_tag.text.split())
        self.set_text(text)
        self.set_title(title)

if __name__ == '__main__':
    num=1
    url = "http://new.zmctc.com/zjgcjy/jyxx/004001/004001002/?Paging=" + str(num + 1)
    header = {"User-Agent":
                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    data = requests.get(url, headers=header)
    data.encoding = "UTF-8"
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    div = soup.find("div", align="center")
    for tr_tag in div.find_all("tr", height="30"):
        a = tr_tag.find("a")
        url_n = "http://new.zmctc.com" + a["href"]
        date = tr_tag.find("td", width="80").text[1:-1]
        print(type(date))
