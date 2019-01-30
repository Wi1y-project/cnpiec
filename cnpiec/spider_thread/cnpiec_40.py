
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import random
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url="http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002002/?Paging="+str(num+1)
        data = requests.get(url)
        data.encoding = "gbk"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        td_tag = soup.find("td", height="800")
        table_tag = td_tag.find("table", width="98%")
        for tr in table_tag.find_all("tr"):
            a = tr.find("a")
            date = tr.find("td", width="90")
            if a == None:
                continue
            url_n = "http://ggzy.xjbt.gov.cn" + a["href"]
            self.set_list(urls,url_n,date.text[1:-1])
        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "gbk"
        data = resq.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find("table", id="tblInfo")
        td_tag = table_tag.find("td", id="tdTitle")
        t_font = td_tag.find("font", style="font-size: 25px")
        title = t_font.text.strip()
        start = data.find(
            '<table cellspacing="0" cellpadding="0" border="0" style="border-width:0px;width:748px;border-collapse:collapse;">')
        end = data.find('</table></body>')
        text = data[start:end]
        p = re.compile('(?<=\>).*?(?=\<)')
        result = p.findall(text)
        text = "".join(result).replace("&nbsp;", "")
        if text == "":
            div = table_tag.find("div", class_="infodetail")
            [s.extract() for s in div("style")]
            text = div.text
        text = "".join(text.split())
        self.set_text(text)
        self.set_title(title)

