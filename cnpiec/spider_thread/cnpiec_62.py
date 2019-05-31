import requests
import cnpiec.spider_modules.standard_spider as ss



def get_html(url):

    data = requests.get(url)
    data.encoding = 'utf-8'
    data = data.json()
    return data


class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        url = 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi='+str(num)+'&ps=20'
        j = get_html(url)
        for item in j['notices']:
            title = item['title']
            date = item['issueTime'].split(' ')[0]
            url_n = 'https://www.cqgp.gov.cn/notices/detail/' + item['id']
            self.set_list(urls, url_n, date, title)

        return urls


class thrid(ss.EndSpider):
    def get(self, url):
        text = 'empty'
        self.set_text(text)

