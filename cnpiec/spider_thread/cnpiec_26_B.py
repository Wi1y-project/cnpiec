
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []

        if num ==0:
            url="http://www.njgp.gov.cn/cgxx/cggg/bmjzcgjg/index.html"
        else:
            url="http://www.njgp.gov.cn/cgxx/cggg/bmjzcgjg/index_"+str(num)+".html"

        header = {"User-Agent":
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
                  "Upgrade-Insecure-Requests": "1"}
        data = requests.get(url, headers=header)
        data.encoding = 'utf-8'
        data = data.text

        nums = re.search("index", url).span()
        prefix = url[:nums[0]]

        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", class_="R_cont_detail")
        for li_tag in div_tag.find_all("li"):
            a_tag = li_tag.find("a")
            url_t = a_tag["href"]
            url_n = prefix + url_t[2:]
            [s.extract() for s in li_tag("a")]
            date = li_tag.text.strip()
            self.set_list(urls,url_n,date)
        return urls

class thrid(ss.EndSpider):
    def get(self,url):
        header = {"User-Agent":
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
                  "Upgrade-Insecure-Requests": "1"}
        data = requests.get(url, headers=header)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        tag = soup.find("div", class_="cont")
        title = tag.find("div", class_="title").get_text().strip()
        date = tag.find("div", class_="extra")
        [s.extract() for s in date('span')]

        text = tag.find("div", class_="article")
        [s.extract() for s in text('script')]
        [s.extract() for s in text('style')]

        text = text.get_text().strip()
        text = "".join(text.split())
        self.set_title(title)
        self.set_text(text)


