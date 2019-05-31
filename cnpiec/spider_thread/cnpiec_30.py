import requests
import cnpiec.spider_modules.standard_spider as ss
import json
import datetime


class first(ss.StartSpider):

    def get(self,num):
        urls = []
        url = "http://www.ccgp-qinghai.gov.cn/es-articles/es-article/_search"
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Content-Type': 'application/json'
        }
        data = {"from": str(num * 15), "size": "15", "query": {"bool": {"must": [{"term": {"siteId": {"value": "38", "boost": 1}}},{"bool": {"should": [{"wildcard": {"districtCode": "6399*"}}]}}, {"wildcard": {"path": {"wildcard": "*6zcyannouncement26*","boost": 1}}}],"adjust_pure_negative": 'true', "boost": 1, "should": []}},"sort": [{"publishDate": {"order": "desc"}}, {"_id": {"order": "desc"}}], "_source": {"includes": ["title", "articleId", "siteId", "cover", "url", "pathName", "publishDate", "attachmentUrl","districtName", "gpCatalogName"], "excludes": ["content"]}}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        j = r.json()
        for item in j['hits']['hits']:
            url_n = 'http://www.ccgp-qinghai.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement3001/' + str(
                item['_id']) + '.html'
            title = item['_source']['title']
            date_temp = str(item['_source']['publishDate'])[:-3]
            date_temp = int(date_temp)
            timeArray = datetime.datetime.utcfromtimestamp(date_temp)
            date = timeArray.strftime("%Y-%m-%d")
            self.set_list(urls, url_n, date, title)
        return urls


class thrid(ss.EndSpider):
    def get(self, url):

        text = 'empty'
        self.set_text(text)

