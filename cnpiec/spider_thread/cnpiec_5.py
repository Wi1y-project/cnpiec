
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import faker
import re




class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url="http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/?page="+str(num)
        f = faker.Factory.create()
        ua = f.user_agent()
        cookies = {
            "csrftoken": "x8Q7GKWYqCf7E6AJ18FnPFzoRAe1vfYTgIZkdMaBrGzF2yqNjNwVDtlgZphgXPPf"
        }
        data = requests.get(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',

            'Host': 'cz.fjzfcg.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua
        }, cookies=cookies)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="wrapTable")
        tbody = div_tag.find("tbody")
        for tr in tbody.find_all("tr"):
            a_tag = tr.find("a")
            url_n = "http://cz.fjzfcg.gov.cn" + a_tag["href"]
            date = tr.find_all("td")[1].text
            self.set_list(urls,url_n,date)
        return urls

class thrid(ss.EndSpider):
    def get(self,url):

        f = faker.Factory.create()
        ua = f.user_agent()
        cookies = {
            "csrftoken": "x8Q7GKWYqCf7E6AJ18FnPFzoRAe1vfYTgIZkdMaBrGzF2yqNjNwVDtlgZphgXPPf"
        }
        data = requests.get(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',

            'Host': 'cz.fjzfcg.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua
        }, cookies=cookies)


        data.encoding = 'utf-8'
        data = data.text
        title=self.get_title(data)
        text=self.get_text(data)
        self.set_title(title)
        self.set_text(text)


    def get_title(self,html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("h2")[0].get_text()

    def get_text(self,html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("div", class_="notice-con")[0].get_text().strip().replace("\n", "")


def test():
    url = "http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/?zone_code=3500&zone_name=省本级"
         # "http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/?zone_code=3500&zone_name=%E7%9C%81%E6%9C%AC%E7%BA%A7"
    f = faker.Factory.create()
    ua = f.user_agent()
    print(ua)
    cookies = {
        "csrftoken":"x8Q7GKWYqCf7E6AJ18FnPFzoRAe1vfYTgIZkdMaBrGzF2yqNjNwVDtlgZphgXPPf"
    }
    data = requests.get(url, headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',

        'Host': 'cz.fjzfcg.gov.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua
         },cookies = cookies)
    print (data.status_code)
    data.encoding = 'utf-8'
    data = data.text
    print(data)
    soup = BeautifulSoup(data, "html.parser")
    div_tag= soup.find("div",class_="wrapTable")
    tbody=div_tag.find("tbody")
    for tr in tbody.find_all("tr"):
        a_tag=tr.find("a")
        url_n= "http://cz.fjzfcg.gov.cn" + a_tag["href"]
        date=tr.find_all("td")[1].text
        print(url_n,date)
if __name__ == '__main__':
    th=thrid(None)
    th.test("http://cz.fjzfcg.gov.cn/3500/notice/f9ebc6637c3641ee9017db2a94bfe5f0/c0743c99c2234903a9c0861786acabf8/")

