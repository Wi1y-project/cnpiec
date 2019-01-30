
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import random
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url="http://www.ccgp-qinghai.gov.cn/jilin/zbxxController.form?declarationType=&type=1&pageNo=" + str(num)
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", class_="m_list_3")
        for li_tag in div_tag.find_all("li"):
            a_tag = li_tag.find("a")
            url_n = a_tag["href"]
            date = li_tag.find("span").text
            date = date.replace("年", "-")
            date = date.replace("月", "-")
            date = date.replace("日", "")
            self.set_list(urls,url_n,date)
        return urls

class thrid(ss.EndSpider):
    def get(self,url):

        dnum = re.search("(\d{4}/\d{1,2}/\d{1,2})", url).span()
        date = url[dnum[0]:dnum[1]]

        suffix_num = re.search("htmlURL=", url).span()
        suffix = url[suffix_num[1]:]
        new_url = "http://www.ccgp-qinghai.gov.cn/" + suffix
        data = requests.get(new_url)
        data.encoding = 'GBK'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")


        tag = soup.find("body")

        title = ""
        for p_title in tag.find_all("p", align="center"):
            title = title + p_title.get_text().strip()
            p_title.extract()

        [s.extract() for s in tag('input')]

        text = tag.get_text().strip()
        text = "".join(text.split())
        self.set_text(text)
        self.set_title(title)

