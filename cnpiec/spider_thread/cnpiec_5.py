
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import time
import faker
import re




class first(ss.ThreadingSpider):

    def get(self,num):
        self.urls = []
        url="http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/"
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
        self.list=[]

        self.get_url_argv(data)
        self.get_urls(url)
        return self.urls

    def get_url_argv(self,html):
        soup = BeautifulSoup(html, "html.parser")
        for ul_tag in soup.find_all("ul", class_="nav-second-level"):
            for a_tag in ul_tag.find_all("a", class_="zc"):
                codes = a_tag["codes"]
                name = a_tag.get_text()
                self.list.append([codes, name])

    def get_urls(self,url):
        for argv in self.list:
            new_url = url + "?zone_code=" + argv[0] + "&zone_name=" + argv[1]
            self.urls.append(new_url)

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
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
        try:
            soup = BeautifulSoup(data, "html.parser")
            div_tag = soup.find("div", class_="wrapTable")
            tbody = div_tag.find("tbody")
            for tr in tbody.find_all("tr"):
                a_tag = tr.find("a")
                url_n = "http://cz.fjzfcg.gov.cn" + a_tag["href"]
                date = tr.find_all("td")[1].text
                result = self.url_increment.is_increment(url_n, date)
                if result:
                    urls.append(url_n)
        except:
            return self.attr.DONE
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):

        f = faker.Factory.create()
        ua = f.user_agent()
        cookies = {
            "csrftoken": "x8Q7GKWYqCf7E6AJ18FnPFzoRAe1vfYTgIZkdMaBrGzF2yqNjNwVDtlgZphgXPPf"
        }
        try:
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
        except:
            return self.attr.DONE

        data.encoding = 'utf-8'
        data = data.text
        date=self.get_date(data)
        title=self.get_title(data)
        text=self.get_text(data)
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

    def get_date(self,html):
        soup = BeautifulSoup(html, "html.parser")
        for div_tag in soup.find_all("div", class_="clearfix"):
            span = div_tag.find_all("span")
        return span[2].get_text()


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
    j = job.Job("cnpiec_5")
    j.submit("first","second","thrid",pyname="cnpiec_5")
    # j.clear_schedule()
