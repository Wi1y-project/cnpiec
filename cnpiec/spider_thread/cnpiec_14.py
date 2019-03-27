
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import json



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):

    def get(self,num):
        if num == 0:
            pass
        else:
            num  = str(num) + '0'
        urls = []
        url = "http://www.hebpr.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextDataNew"
        data = {
            "token": "", "pn": str(num), "rn": '10', "sdt": "", "edt": "", "wd": "", "inc_wd": "", "exc_wd": "",
            "fields": "title",
            "cnum": "001;002", "sort": "{\"showdate\":\"0\"}", "ssort": "title", "cl": '200', "terminal": "",
            "condition": '[]', "time": 'null', "highlights": "title", "statistics": 'null', "unionCondition": 'null',
            "accuracy": "", "noParticiple": "0", "searchRange": 'null', "isBusiness": '1'
        }

        r = requests.post(url, json.dumps(data))
        for item in r.json()['result']['records']:

            date = item['infodate'].split(' ')[0]
            url_n = 'http://www.hebpr.gov.cn' + item['linkurl']
            self.set_list(urls,url_n,date)
                
        return urls


class thrid(ss.EndSpider):
    def get(self,url):

        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find(attrs={'class':'ewb-poll-tt'}).get_text().strip()
        text = soup.find(attrs={'id':'content'}).get_text().strip()
        text = "".join(text.split())


        self.set_text(text)
        self.set_title(title)


