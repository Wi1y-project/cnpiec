
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss




def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):

    def get(self,num):

        urls = []
        if num==0:
            url = 'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index.html'
        else:
            url = 'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_'+ str(num + 1) +'.html'
        
        soup = BeautifulSoup(get_html(url),'html.parser')
        temp = []
        for i in soup.find_all(attrs={'class':'txt1'}):
            try:
                temp.append(i.find('span').get_text())
            except:
                pass
        div = soup.find(attrs={'id':'tablediv'})
        for c, a in enumerate(div.find_all('a')):
            url_n = 'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/' + a.get('href').replace('./','')
            date = temp[c]
            self.set_list(urls, url_n, date)
        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find(attrs={'class':'txt2'}).get_text().strip()
        text = soup.find_all(attrs={'class':'txt7'})[1].get_text().strip()
        text = "".join(text.split())


        self.set_text(text)
        self.set_title(title)