from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import cnpiec.spider_modules.standard_spider as ss
import re
import time



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.StartSpider):

    def get(self,num):
        print("111111111")
        urls = []
        url = 'http://cgb.xjtu.edu.cn/xajdWeb/wzgl.wznr.wangzhanshouye.getErJiDaoHangNeiRongByLmid.action'
        url1 = 'http://cgb.xjtu.edu.cn/xajdWeb/wzgl.wznr.wangzhanshouye.queryGongYongWangZhanNeiRongById.action'
        data = {
            'wznrId':'',
            'pageNo': str(num + 1),
            'daoHangLMID': 'ad21b3ab-de8b-4cc2-9ef0-ad013e9cffb4',
            'daoHangName': '采购信息',
            'dangQianBiaoTi': '采购公告',
            'daoHangLx': ''
        }
        r = requests.post(url,data = data)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'html.parser')

        div = soup.find(attrs={'class':'list_5'})
        for a in div.find_all('a'):
            
            parm = a.get('onclick').replace('queryWangZhanNeiRong','').replace('(','').replace(')','').replace("'","").split(',')
            data2 = {
                    'wznrId': parm[1],
                    'pageNo':'',
                    'daoHangLMID': parm[0],
                    'daoHangName': '采购信息',
                    'dangQianBiaoTi': '采购公告',
                    'daoHangLx': ''
                    }
            r1 = requests.post(url1,data = data2)
            s1 = BeautifulSoup(r1.text, "html.parser")

            self.set_list(urls,a.get('onclick'),s1.find(attrs={'class':'w2'}).get_text().strip().split('发布时间：')[1].split(' ')[0].strip())
        return urls



class thrid(ss.EndSpider):
    def get(self,url):
        url_parm = url.replace('queryWangZhanNeiRong','').replace('(','').replace(')','').replace("'","").split(',')
        url1 = 'http://cgb.xjtu.edu.cn/xajdWeb/wzgl.wznr.wangzhanshouye.queryGongYongWangZhanNeiRongById.action'
        data = {
                'wznrId': url_parm[1],
                'pageNo':'',
                'daoHangLMID': url_parm[0],
                'daoHangName': '采购信息',
                'dangQianBiaoTi': '采购公告',
                'daoHangLx': ''
                }

        r = requests.post(url1,data = data)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find(attrs={'class':'w1'}).get_text().strip()
        date = soup.find(attrs={'class':'w2'}).get_text().strip().split('发布时间：')[1].split(' ')[0].strip()
        text = soup.find(attrs={'class':'w3'}).get_text().strip()
        text = "".join(text.split())
        self.set_title(title)
        self.set_text(text)

        
