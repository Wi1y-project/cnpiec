import redis
import re
import datetime
import time
from  cnpiec.spider_modules import standard_spider
from cnpiec.spider_modules.common import common_keys
import jpype
from jpype import *
import sys






# jvmPath = 'C:/Program Files/Java/jre1.8.0_191/bin/server/jvm.dll'

jpype.startJVM(common_keys.jvmPath, "-Djava.class.path="+common_keys.JAR_PATH)



redis_ = redis.Redis(host=common_keys.REDIS_IP, port=common_keys.REDIS_PORT, db=common_keys.REDIS_DB, decode_responses=True)
REDIS_ERR_NAME="err"
FINISH_LIST_NAME="finish"
def print_errs(file):
    num=redis_.llen(REDIS_ERR_NAME)
    if num != 0:
        err_file=open(file,"a+",encoding="utf-8")
        while(True):
            if redis_.llen(REDIS_ERR_NAME) == 0:
                break
            line=redis_.rpop(REDIS_ERR_NAME)
            err_file.write(str(datetime.datetime.now())+" "+line+"\n")

def write_file(file_path):
    file = open(file_path, "w+", encoding="utf-8")
    rowkey_file = open(common_keys.ROWKEY_PATH, "w+", encoding="UTF-8")

    i=0
    start_row=create_rowkey(i)
    while(True):
        if redis_.llen(FINISH_LIST_NAME) == 0:
            break
        string=redis_.lpop(FINISH_LIST_NAME)
        bean=standard_spider.Bean()
        bean.parser(string)
        bean.need = needs(bean)
        rowkey=create_rowkey(i)
        line=rowkey+"##"+bean.name + "##" + bean.url + "##" + bean.date + "##" + bean.title + "##" + bean.text + "##" + bean.responsible+"##"+bean.need
        line=re.sub("\s+"," ",line)
        # rowkey_file.write(rowkey+"\n")
        file.write(line + "\n")
        i+=1
    end_row=create_rowkey(i-1)
    rowkey_file.write(common_keys.NOTE + common_keys.START_ROW + "=" + start_row + "\n" + common_keys.END_ROW + "=" + end_row)

def create_rowkey(i):
    d=time.mktime(datetime.datetime.now().date().timetuple())
    t=sys.maxsize-long(d)
    # t=sys.maxsize-long(time.time())
    h=datetime.datetime.now().hour
    # print(datetime.datetime.now().date().timetuple())
    # print(time.mktime(datetime.datetime.now().date().timetuple()))
    # print(t)
    fs="2"
    if common_keys.FIRST_TIME<=h<common_keys.SECOND_TIME:
        fs="1"

    return str(t)+"_"+str.zfill(str(i),5)+"_"+fs







def needs(bean):
    for c, i in enumerate(common_keys.keyword_arr1):
        if i in bean.cut:
            return  "y"
        elif c == len(common_keys.keyword_arr1) - 1:
            for c2, j in enumerate(common_keys.keyword_arr2):
                if j in bean.cut:
                   return java_part(bean.cut)
                elif c2 == len(common_keys.keyword_arr2) - 1:
                   return "n"

def java_part(parm):

    Trainer = JClass('Trainer')
    t = Trainer()
    t.setMode(t.inPut())
    t.processText(parm)
    res = t.getResult()
    if 'y' in res:
        return 's'
    else:
        return res

class Name_Manager(object):
    '''
    负责管理每一个线程向redis中存入数据的名称

    '''
    def __init__(self,name):
        '''

        :param name: 整爬虫的名称
        '''
        self.name=name
        self.list=self.name+"_list"
        self.done=self.name + "_done"


    def create_set_name(self):
        return self.name + "_set"

    def create_date_name(self):
        return self.name + "_date"

    def set_err(self,bean):
        redis_.lpush(REDIS_ERR_NAME,bean.to_string())

    def set_finish(self,bean):
        redis_.lpush(FINISH_LIST_NAME,bean.to_string())

    def get_done(self):
        return redis_.get(self.done)

    def set_done(self,bool):
        redis_.getset(self.done, str(bool))

    def clear_done(self):
        redis_.delete(self.done)

    def put_bean(self, bean):
        redis_.lpush(self.list, bean.to_string())

    def get_bean(self):
        return  redis_.rpop(self.list)

    def has_next(self):
        return not redis_.llen(self.list) == 0

    def is_increment(self,url):
        num=redis_.sadd(self.create_set_name(),url)
        return num==1

    def delete_url(self,url):
        redis_.srem(self.create_set_name(),url)

    def get_last_date(self):
        return redis_.get(self.create_date_name())

    def set_last_date(self,date):
        redis_.set(self.create_date_name(),date)

    def create_lock_name(self):
        return self.name+"_lock"

    def get_lock(self):
        return redis_.setnx(self.create_lock_name(),1)

    def release_lock(self):
        redis_.delete(self.create_lock_name())

    def delete_all(self):
        for key in redis_.keys(self.name+"*"):
            redis_.delete(key)


def query():

    for i in range(50):
        keys="cnpiec_"+str(i)+"_*"
        print("查询值：",keys)
        for key in redis_.keys(keys):
            # redis_.delete(key)
            # print(key+" "+redis_.type(key))
            if redis_.type(key) == "string":
                print(key + ":", redis_.get(key))
            elif redis_.type(key) == "list":
                print(key + " size:", redis_.llen(key), " values:")
            elif redis_.type(key) == "set":
                print(key + ":", redis_.scard(key), ":")




if __name__ == '__main__':
    file=open(common_keys.ROWKEY_PATH,"w+",encoding="UTF-8")
    file.write(common_keys.NOTE+common_keys.START_ROW+"="+"sdfsf"+"\n"+common_keys.END_ROW+"="+"sfsdf")


    # for i in range(10):
    #     print(create_rowkey(i))
    #     time.sleep(1)
    # redis_.srem("cnpiec_47_set","http://ecp.cnnc.com.cn/xzbgg/66179.jhtml")
    # query()
    # for key in redis_.keys("*"):
    #     redis_.delete(key)
