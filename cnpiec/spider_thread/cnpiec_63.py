import requests
import cnpiec.spider_modules.standard_spider as ss


def get_html(url, data1):

    data = requests.post(url, data=data1, timeout=20)

    # data.encoding = 'utf-8'
    data = data.json()
    return data


class first(ss.StartSpider):

    def get(self,num):
        
        urls = []
        url = 'http://www.ccgp-yunnan.gov.cn/bulletin.do?method=moreListQuery'
        data = {
            'current': str(num),
            'rowCount': '10',
            'searchPhrase': '',
            'query_sign': '1'
        }
        j = get_html(url, data1=data)
        for item in j['rows']:
            date = item['beginday']
            title = item['bulletintitle']
            url_n = 'http://www.ccgp-yunnan.gov.cn/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + str(item['bulletin_id'])
            self.set_list(urls, url_n, date, title)

        return urls


class thrid(ss.EndSpider):
    def get(self, url):
        text = 'empty'
        self.set_text(text)

