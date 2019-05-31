
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):

    def get(self,num):

        urls = []

        if num == 0:
            url = 'http://cgglzx1.jlu.edu.cn/?l1/fpage/c000402/w/p'
        else:
            url = 'http://cgglzx1.jlu.edu.cn/?l1/fpage/c000402/w/p'+ str(num)
        soup = BeautifulSoup(get_html(url),'html.parser')


        for a in soup.find_all(attrs={'id':'Columnnewslist'}):
            
            url_n = a.find('a').get('href').replace('./', 'http://cgglzx1.jlu.edu.cn/')
            r = requests.get(url_n)
            s = BeautifulSoup(r.text,'html.parser')
            temp = s.find(attrs={'id':'Newsshowtime'}).get_text().strip()
            mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", temp)
            date = mat.group(0)

            self.set_list(urls,url_n,date)
        return urls


class thrid(ss.EndSpider):
    def get(self,url):

        html = get_html(url)

        soup = BeautifulSoup(html, "html.parser")

       
        title = soup.find(attrs={'id':'Newsshowtitle'}).get_text().strip()

        text = soup.find(attrs={'id':'NewsshowContent'}).get_text().strip()
        text = "".join(text.split())

        self.set_text(text)
        self.set_title(title)
        
if __name__ == '__main__':
    pass



