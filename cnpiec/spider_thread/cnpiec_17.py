
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []

        url = "http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=0&pageSize=10&pageNo=" + str(num)
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", class_="List2")
        for li_tag in div_tag.find_all("li"):
            a_tag = li_tag.find("a")
            date = li_tag.find("span").text
            url_n = "http://www.hngp.gov.cn" + a_tag["href"]
            self.set_list(urls,url_n,date)
        return urls

class thrid(ss.EndSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find_all("div", class_="BorderEEE BorderRedTop")[0]

        [s.extract() for s in div_tag('style')]
        title = div_tag.find_all("h1")[0].get_text().strip().replace("\n", "")
        text = ""
        script = soup.find_all("script")
        for s in script:
            str = s.get_text()
            f = re.search("jQuery\(document\).ready\(function", str)
            if f:
                int = re.search('\$\.get\("/webfile.*\.htm"', str).span()
                t_url = "http://www.hngp.gov.cn" + str[int[0] + 7:int[1] - 1]

                t_data = requests.get(t_url)
                t_data.encoding = 'utf-8'
                t_data = t_data.text

                t_soup = BeautifulSoup(t_data, "html.parser")
                [s.extract() for s in t_soup('style')]
                text = t_soup.get_text().strip()
                text = "".join(text.split())
        self.set_text(text)
        self.set_title(title)


