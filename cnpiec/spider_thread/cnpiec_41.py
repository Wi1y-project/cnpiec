
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss


class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url="http://zbxx.ycit.cn/zbxx/Index.asp?page="+str(num+1)
        data = requests.get(url)
        data.encoding = "gbk"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find("table", width="722", height="500")
        td = table_tag.find("td", width="722")
        table = td.find("table")
        for tr in table.find_all("tr"):
            a = tr.find("a", target="_self")
            date = tr.find("td", align="right")
            if a == None:
                continue
            url_n = "http://zbxx.ycit.cn" + a["href"]
            self.set_list(urls,url_n,date.text.strip())
        return urls

class thrid(ss.EndSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "gbk"
        data = resq.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find("table", width="1004", height="462")
        td = table_tag.find("td", width="1000")
        table = td.find("table")
        title = table.find("td", class_="wzrr").text.strip()
        text = "".join(table_tag.text.split())
        self.set_title(title)
        self.set_text(text)

if __name__ == '__main__':
    num=0
    url = "http://zbxx.ycit.cn/zbxx/Index.asp?page=" + str(num + 1)
    data = requests.get(url)
    data.encoding = "gbk"
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    table_tag = soup.find("table", width="722", height="500")
    td = table_tag.find("td", width="722")
    table = td.find("table")
    for tr in table.find_all("tr"):
        a = tr.find("a", target="_self")
        date = tr.find("td", align="right")
        if a == None:
            continue
        url_n = "http://zbxx.ycit.cn" + a["href"]
        print(type(date),date.text.strip(),url_n)