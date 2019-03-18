import threading
import logging
import random
import datetime
import time
import json
import thulac
import jpype
from jpype import JClass
from cnpiec.spider_modules.tasks import common_keys






logger=logging.getLogger("logger")
thu1 = thulac.thulac(model_path = common_keys.THULAC_MODEL_PATH)

class StartSpider(threading.Thread):
    def __init__(self,nm):
        threading.Thread.__init__(self)
        self.nm=nm
        self.url_increment=increment(self.nm)
        self.null_num=0
        self.MAX_NULL_NUM=10

    def get(self,num):
        pass

    def set_list(self,list,url,date):
        list.append((url,date))

    def run(self):
        logger.info(self.nm.name+" StartSpider start as "+self.name+"...")
        i=0

        err_time=0
        err_count=0
        while(True):
            logger.info(self.nm.name + "__"+self.name+" run page: "+str(i))
            try:
                time.sleep(random.random()*3)
                list=self.get(i)
            except:
                logger.error(self.nm.name+" Start Thread has err. err page: "+ str(i),exc_info = True)
                err_time+=1
                if err_time>5:
                    err_count+=1
                    i+=1
                    if err_count>5:
                        bean=Bean()
                        bean.name=self.nm.name
                        bean.err="请求页面出错，异常退出！"
                        self.nm.set_err(bean)
                        break
                continue

            do_exit=True
            has_increment=False
            print("---------------------","page"+str(i))
            for item in list:
                url=item[0]
                date=item[1]
                print(url,date)
                if self.url_increment.date_compare(date):
                    if self.url_increment.url_compare(url,date):
                        bean=Bean()
                        bean.date=date
                        bean.url=url
                        self.nm.put_bean(bean)
                        has_increment=True
                    do_exit=False

            if not has_increment :
                self.null_num+=1
                if self.null_num>self.MAX_NULL_NUM:
                    do_exit=True
            # print("================",do_exit)
            if do_exit:
                logger.info(self.nm.name+" start thread finsh.")
                self.nm.set_done(True)
                self.url_increment.date_check()
                break
            else:
                i+=1

class Bean():
    def __init__(self):
        self.url=""
        self.date=""
        self.title=""
        self.text=""
        self.retry=0
        self.err=""
        self.cut=""
        self.name=""
        self.responsible=""
        self.need=""


    def create_dict(self):
        return {common_keys.URL_NAME:self.url,common_keys.DATE_NAME:self.date,
                 common_keys.TITLE_NEME:self.title,common_keys.TEXT_NEME:self.text,
                common_keys.RETRY_NEME:self.retry,common_keys.ERR_NAME:self.err,
                common_keys.TITLE_CUT:self.cut,common_keys.NAME:self.name,
                common_keys.RESPONSIBLE:self.responsible,common_keys.NEED:self.need}

    def parser_dict(self,dicts):
        self.url=dicts[common_keys.URL_NAME]
        self.date=dicts[common_keys.DATE_NAME]
        self.title=dicts[common_keys.TITLE_NEME]
        self.text=dicts[common_keys.TEXT_NEME]
        self.retry=dicts[common_keys.RETRY_NEME]
        self.err=dicts[common_keys.ERR_NAME]
        self.cut=dicts[common_keys.TITLE_CUT]
        self.name=dicts[common_keys.NAME]
        self.responsible=dicts[common_keys.RESPONSIBLE]
        self.need=dicts[common_keys.NEED]

    def to_string(self):
        if self.url =="":
            raise ValueError("url 不能为空！")
        if self.date =="":
            raise ValueError("date 不能为空！")

        return json.dumps(self.create_dict())

    def parser(self,string):
        self.parser_dict(json.loads(string))
class EndSpider(threading.Thread):
    def __init__(self,nm):
        threading.Thread.__init__(self)
        self.nm=nm
        self.temp_title=None
        self.temp_text=None

    def get(self,url):
        pass

    def set_title(self,title):
        self.temp_title=title

    def set_text(self,text):
        self.temp_text=text

    def run(self):
        logger.info(self.nm.name+" end thread start as "+self.name+"...")

        while (True):
            if self.nm.has_next():
                bean=Bean()
                bean.parser(self.nm.get_bean())
            else:
                if self.nm.get_done() == str(True):
                    break
                else:
                    logger.info(self.nm.name + "__"+self.name+" end thread :当前任务已完成，等待新任务...")
                    time.sleep(10)
                    continue
            try:
                logger.info(self.nm.name + "__"+self.name+ " 开始爬取："+bean.url)
                time.sleep(random.random()*3)
                self.get(bean.url)
            except Exception as e:
                logger.error(self.nm.name + " end Thread has err. err url : "+bean.url, exc_info=True)
                bean.retry +=1

                if bean.retry <5:
                    logger.info(self.nm.name + " err url : " + bean.url+" 重试次数："+str(bean.retry)+"。小于5次,继续重试...")
                    self.nm.put_bean(bean)
                else:
                    logger.info(self.nm.name + " err url : " + bean.url + " 重试次数：" + str(bean.retry) + "。大于5次,不再重试。")
                    bean.err=e.__str__()
                    bean.date=""
                    bean.title=""
                    bean.text=""

                    self.nm.delete_url(bean.url)
                    self.nm.set_err(bean)

                continue
            try:
                self.set_parm(bean)
                self.nm.set_finish(bean)
            except Exception as e:
                logger.error(self.nm.name + " end Thread download value has err. err url : " + bean.url, exc_info=True)
                bean.retry += 1

                if bean.retry < 5:
                    logger.info(self.nm.name + " err url : " + bean.url + " 重试次数：" + str(bean.retry) + "。小于5次,继续重试...")
                    self.nm.put_bean(bean)
                else:
                    logger.info(self.nm.name + " err url : " + bean.url + " 重试次数：" + str(bean.retry) + "。大于5次,不再重试。")
                    bean.err = e.__str__()
                    bean.date = ""
                    bean.title = ""
                    bean.text = ""
                    self.nm.delete_url(bean.url)
                    self.nm.set_err(bean)


        logger.info(self.nm.name+ " end thread finsh!")
        self.nm.clear_done()



    def set_parm(self,bean):

        if self.temp_title == None:
            raise ValueError("title 不能为空！")

        if self.temp_text == None:
            raise ValueError("text 不能为空！")

        bean.title=self.temp_title
        self.temp_title=None
        bean.text=self.temp_text
        self.temp_text=None

        if self.nm == None:
            print("nm为空，请确认是否为测试！")
        else:
            bean.name=self.nm.name
        bean.title="".join(bean.title.split())
        bean.text="".join(bean.text.split())
        bean.cut=self.do_cut(bean.title)
        bean.responsible = self.responsible(bean.url)
        # bean.need = self.java_part(bean.title)

    def do_cut(self,title):
        a = ""
        cuts = thu1.cut(title, text=False)
        for i in cuts:
            if 'n' == i[1] or 'v' == i[1] or 'a' == i[1] or 'j' == i[1] or 'x' == i[1] or 'd' == i[1] or 'g' == i[1]:
                a += i[0] + ' '
        return a

    # def java_part(self, parm):
    #
    #     Trainer = JClass('Trainer')
    #     t = Trainer()
    #     t.setMode(t.inPut())
    #     t.processText(parm)
    #     res = t.getResult()
    #     if 'y' in res:
    #         return 's'
    #     else:
    #         return res

    def responsible(self,site):

        if '/' in site.replace('http://', '').replace('https://', ''):
            site = site.replace('http://', '').replace('https://', '').split('/')[0].strip()
        else:
            site = site.replace('http://', '').replace('https://', '').strip()

        site_map = {
            'www.gzsggzyjyzx.cn': '王洋',
            'www.ccgp-jiangsu.gov.cn': '何一石',
            'www.ccgp-shandong.gov.cn': '孟宏权',
            'cgb.xjtu.edu.cn': '秦超,刘波',
            'ggzy.xjbt.gov.cn': '刘波',
            'zbxx.ycit.cn': '王美怡',
            'www.ccgp-yancheng.gov.cn': '何一石',
            'www.zjzfcg.gov.cn': '董伟琨',
            'www.bidchance.com': '孟宏权,杨跃,高世明,张琦,杨跃,杜士荣,秦超,赵潇潇,刘柳,姜波,郑子玉,沈婧男,肖俊文,李东海',
            'www.ccgp.gov.cn': '王雪娟,肖俊文,刘波,刘向平,孟宏权,刘波,师光辉,张洁,骆金伟,李晓光,金丽荣,姜波,沈婧男,赵潇潇,李东海,孙秀焕,杨跃,王洋,刘默'
        }

        try:
            return site_map[site]
        except:
            return '无负责人'




    def test(self,url):
        bean=Bean()
        print("test get 方法...")
        self.get(url)
        print("测试get方法的结果...")
        self.set_parm(bean)
        print(bean.name + "##" + bean.url + "##" + bean.date + "##" + bean.title + "##" + bean.text + "##" + bean.cut)


class increment():
    def __init__(self,nm):
        self.nm=nm
        self.format="%Y-%m-%d"
        self.default_date="2019-1-29"
        self.current_date=None
        self.last_date=None
        self.url_date=None

    def get_date(self):
        ld = self.nm.get_last_date()
        if ld == None:
            self.last_date = datetime.datetime.strptime(self.default_date, self.format)
        else:
            self.last_date = datetime.datetime.strptime(ld, self.format)

    def get_url_date(self,date):
        self.url_date=datetime.datetime.strptime(date,self.format)
        return self.url_date
    def is_increment(self,url,date):
        '''
            判断所传的url是否是增量，会按照传入的日期判断
        :param url:
        :param date: 日期格式为：XXXX-XX-XX
        :return:
        '''


        if self.date_compare(date):
            return self.url_compare(url,date)
        else:
            return False

    def date_compare(self,date):
        if self.last_date ==None:
            self.get_date()
        url_date=self.get_url_date(date)
        # print("+++++++++++",url_date,self.last_date)
        return  url_date>=self.last_date


    def url_compare(self,url,date):
        url_date = self.get_url_date(date)
        result = self.nm.is_increment(url)
        if result:
            if self.current_date == None:
                self.current_date = url_date
            if url_date > self.current_date:
                self.current_date = url_date
        return result


    def date_check(self):
        if self.current_date != None:
            while True:
                if self.nm.get_lock():
                    condition_date_str=self.nm.get_last_date()
                    if condition_date_str == None:
                        condition_date = datetime.datetime.strptime(self.default_date, self.format)
                    else:
                        condition_date = datetime.datetime.strptime(condition_date_str, self.format)
                    if self.current_date>condition_date:
                        if self.current_date>datetime.datetime.now():
                            self.current_date=datetime.datetime.now()
                        self.nm.set_last_date(str(self.current_date.date()))
                    self.nm.release_lock()
                    break
                else:
                    time.sleep(1)
