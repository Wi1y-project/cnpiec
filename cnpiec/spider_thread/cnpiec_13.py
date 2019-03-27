
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
        url = 'http://cg.hzft.gov.cn/www/noticelist.do'
        
        r = requests.post(url,data = {'page.pageNum': str(num + 1),"parameters['regionguid']": "","parameters['noticetype']": 3,"parameters['title']":""})
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'html.parser')

        div = soup.find(attrs={'class':'c_list_item'})
        for li in div.find_all('li'):
            url_n = 'http://cg.hzft.gov.cn/' + li.find('a').get('href')
            date = li.find('span').get_text().replace(' ','')
            self.set_list(urls,url_n,date)
                
        return urls


class thrid(ss.EndSpider):
    def get(self,url):

        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find(attrs={'class':'content_tit'}).get_text().strip()
        text = soup.find(attrs={'class':'detail_con'}).get_text().strip()
        text = "".join(text.split())


        self.set_text(text)
        self.set_title(title)





