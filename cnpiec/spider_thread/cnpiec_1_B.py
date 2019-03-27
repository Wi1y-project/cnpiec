
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re




class first(ss.StartSpider):
    def get(self,num):
        urls=[]
        if num == 0:
            url="http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/index.html"
        else:
            url="http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/index_"+str(num+1)+".html"

        data = requests.get(url)
        data.encoding = "gbk"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")

        for li in soup.find_all("li"):
            url_n = "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg" + li.find("a")["href"][1:]
            date = li.find("span").text
            self.set_list(urls,url_n,date)

        return urls


class second(ss.EndSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "gbk"
        data = resq.text
        title = self.get_title(data)
        text = self.get_text(data)
        self.set_title(title)
        self.set_text(text)


    def get_title(self,html):
        str4 = '<span style="font-size: 20px;font-weight: bold">.*\n?.*</span>'
        patten4 = re.compile(str4)
        result4 = patten4.findall(html)
        soup = BeautifulSoup(result4[0], "html.parser")
        return soup.find_all("span")[0].get_text().strip().replace("\n", " ")

    def get_text(self,html):
        test_result = re.search('<div align="left" style="padding-left:30px;">', html)
        data_div_front = html[test_result.span()[1]:]
        test_result = re.search('</div>', data_div_front)
        data_div = data_div_front[0:test_result.span()[0]]

        str = ""

        soup = BeautifulSoup(data_div, "html.parser")
        [s.extract() for s in soup('style')]

        for tag in soup.find_all("p"):
            str = str + tag.get_text().strip()

        return str.replace("\n", "")

