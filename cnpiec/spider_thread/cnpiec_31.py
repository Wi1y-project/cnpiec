
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url = "http://soeasycenter.com/newTender"

        parm = {
            "periodTime": " 0.0",
            "pageNum": "1",
            "pageSize": "20",
        }

        data = requests.post(url, data=parm)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find("table", class_="table table-striped")
        [s.extract() for s in table('thead')]
        for tr_tag in table.find_all("tr"):
            a_tag = tr_tag.find("a")
            url_n = "http://soeasycenter.com" + a_tag["href"]
            date = tr_tag.find_all("td")[3].text
            self.set_list(urls,url_n,date)

        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'UTF-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", class_="maincontent")
        fdiv = div_tag.find("div", class_="mytop")
        title = fdiv.find("h4").get_text().strip()
        text = div_tag.find("div", class_="mymain").get_text().strip()
        text = "".join(text.split())
        self.set_title(title)
        self.set_text(text)


