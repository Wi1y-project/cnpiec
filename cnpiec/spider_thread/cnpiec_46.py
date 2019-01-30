
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import random
import json



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):

    def get(self,num):
        urls = []

        url = "http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?pageSize=15&pageNo=" + str(
            num) + "&sourceAnnouncementType=3001&url=http%3A%2F%2Fnotice.zcy.gov.cn%2Fnew%2FnoticeSearch"
        data = requests.get(url)
        data.encoding = "UTF-8"
        data = data.text
        josns = json.loads(data)
        items = josns["articles"]
        for item in items:
            id = item["id"]
            url_0 = "http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?noticeId=" + id + "&url=http%3A%2F%2Fnotice.zcy.gov.cn%2Fnew%2FnoticeDetail"
            resq = requests.get(url_0)
            resq.encoding = "UTF-8"
            data = resq.text
            jsons = json.loads(data)
            n_date = jsons["noticePubDate"]
            date = n_date.split(" ")[0]
            self.set_list(urls,url_0,date)

        return urls


class thrid(ss.EndSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "UTF-8"
        data = resq.text
        jsons = json.loads(data)
        title = jsons["noticeTitle"].replace("\n","")
        content = jsons["noticeContent"]
        soup = BeautifulSoup(content, "html.parser")
        [s.extract() for s in soup("style")]
        text = soup.text
        text = "".join(text.split())
        self.set_title(title)
        self.set_text(text)



