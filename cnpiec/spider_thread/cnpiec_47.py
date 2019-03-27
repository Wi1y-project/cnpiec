
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re


class first(ss.StartSpider):

    def get(self,num):
        urls = []
        if num==0:
            url="http://ecp.cnnc.com.cn/xzbgg/index.jhtml"
        else:
            url="http://ecp.cnnc.com.cn/xzbgg/index_"+str(num+2)+".jhtml"
        data = requests.get(url)
        data.encoding = "UTF-8"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="List1")

        for li in div_tag.find_all("li"):
            a = li.find("a")["href"]
            url_n = "http://ecp.cnnc.com.cn" + a
            date = li.find("span", class_="Right Gray").text
            self.set_list(urls,url_n,date)
        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "UTF-8"
        data = resq.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="W980 Center PaddingTop10")
        title = div_tag.find("h1").text.strip()

        start = data.find('<div class="Contnet" style="min-height:500px; padding:0 30px;">')
        end = data.find('<ul style="text-align:center; padding:10px;">')
        text = data[start:end]
        p = re.compile('(?<=\>).*?(?=\<)')
        result = p.findall(text)
        text = "".join(result)
        self.set_text(text)
        self.set_title(title)
