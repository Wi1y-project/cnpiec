import threading
import logging
import random
import datetime
import time
import json
import thulac
from cnpiec.spider_modules import tasks

URL_NAME="url"
DATE_NAME="date"
TITLE_NEME="title"
TEXT_NEME="text"
RETRY_NEME="retry"
ERR_NAME="err"
TITLE_CUT="cut"
NAME="name"



logger=logging.getLogger("logger")
thu1 = thulac.thulac(model_path = tasks.THULAC_MODEL_PATH)

class StartSpider(threading.Thread):
    def __init__(self,nm):
        threading.Thread.__init__(self)
        self.nm=nm
        self.url_increment=increment(self.nm)

    def get(self,num):
        pass

    def set_list(self,list,url,date):
        list.append((url,date))

    def run(self):
        logger.info(self.nm.name+" StartSpider start...")
        i=0
        while(True):
            logger.info(self.nm.name + " run page: "+str(i))
            try:
                time.sleep(random.random()*3)
                list=self.get(i)
            except:
                logger.error(self.nm.name+" Start Thread has err. err page: "+ str(i),exc_info = True)

            do_exit=True
            for item in list:
                url=item[0]
                date=item[1]
                # print(url,date)
                if self.url_increment.date_compare(date):
                    if self.url_increment.url_compare(url,date):
                        bean=Bean()
                        bean.date=date
                        bean.url=url
                        self.nm.put_bean(bean)
                    do_exit=False
            # print(do_exit)
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


    def create_dict(self):
        return {URL_NAME:self.url,DATE_NAME:self.date,
                 TITLE_NEME:self.title,TEXT_NEME:self.text,
                RETRY_NEME:self.retry,ERR_NAME:self.err,
                TITLE_CUT:self.cut,NAME:self.name}

    def parser_dict(self,dicts):
        self.url=dicts[URL_NAME]
        self.date=dicts[DATE_NAME]
        self.title=dicts[TITLE_NEME]
        self.text=dicts[TEXT_NEME]
        self.retry=dicts[RETRY_NEME]
        self.err=dicts[ERR_NAME]
        self.cut=dicts[TITLE_CUT]
        self.name=dicts[NAME]

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
        self.title=None
        self.text=None

    def get(self,url):
        pass

    def set_title(self,title):
        self.title=title

    def set_text(self,text):
        self.text=text

    def run(self):
        logger.info(self.nm.name+" end thread start...")

        while (True):
            if self.nm.has_next():
                bean=Bean()
                bean.parser(self.nm.get_bean())
            else:
                if self.nm.get_done() == str(True):
                    break
                else:
                    logger.info(self.nm.name + " end thread :当前任务已完成，等待新任务...")
                    time.sleep(10)
                    continue
            try:
                logger.info(self.nm.name+" 开始爬取："+bean.url)
                time.sleep(random.random()*3)
                self.get(bean.url)
            except Exception as e:
                logger.error(self.nm.name + " end Thread has err. err url : "+bean.url, exc_info=True)
                bean.retry +=1

                if bean.retry <5:
                    self.nm.put_bean(bean)
                else:
                    bean.err=e.__str__()
                    self.nm.delete_url(bean.url)
                    self.nm.set_err(bean)
            try:
                self.set_parm(bean)
                self.nm.set_finish(bean)
            except Exception as e:
                logger.error(self.nm.name + " end Thread has err. err url : " + bean.url, exc_info=True)
                bean.err = e.__str__()
                self.nm.delete_url(bean.url)
                self.nm.set_err(bean)

        logger.info(self.nm.name+ " end thread finsh!")
        self.nm.clear_done()



    def set_parm(self,bean):

        if self.title == None:
            raise ValueError("title 不能为空！")

        if self.text == None:
            raise ValueError("text 不能为空！")

        bean.title=self.title
        self.title=None
        bean.text=self.text
        self.text=None

        bean.name=self.nm.name
        bean.title="".join(bean.title.split())
        bean.text="".join(bean.text.split())
        bean.cut=self.do_cut(bean.title)

    def do_cut(self,title):
        a = ""
        text = thu1.cut(title, text=False)
        for i in text:
            if 'n' == i[1] or 'v' == i[1] or 'a' == i[1] or 'j' == i[1] or 'x' == i[1] or 'd' == i[1] or 'g' == i[1]:
                a += i[0] + ' '
        return a




class increment():
    def __init__(self,nm):
        self.nm=nm
        self.format="%Y-%m-%d"
        self.default_date="2019-1-15"
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




