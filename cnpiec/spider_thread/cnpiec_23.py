
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url = "http://www.jxsggzy.cn/web/jyxx/002006/002006001/" + str(num+1) + ".html"
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="ewb-infolist")
        for li_tag in div_tag.find_all("li"):
            a_tag = li_tag.find("a")
            url_n = "http://www.jxsggzy.cn" + a_tag["href"]
            date = li_tag.find("span").text
            self.set_list(urls,url_n,date)
        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div = soup.find_all("div", class_="article-info")[0]
        [s.extract() for s in div('script')]
        [s.extract() for s in div('style')]
        title = div.find_all("h1")[0].get_text().strip().replace("\n", "")
        text = div.find_all("div")[0].get_text().strip()
        self.set_title(title)
        self.set_text(text)




