import redis
import threading
import datetime
from  cnpiec.spider_modules import tasks,standard_spider
import jpype
from jpype import *

REDIS_IP="10.3.1.99"
REDIS_PORT="6379"
REDIS_DB="12"

# jvmPath = 'C:/Program Files/Java/jre1.8.0_191/bin/server/jvm.dll'
jvmPath = 'C:/File/soft/java/jre1.8/bin/server/jvm.dll'
jpype.startJVM(jvmPath, "-Djava.class.path=D:/classifier.jar")

keyword_arr1 = ["文献","纸质","纸本","数据库","画册","杂志","书刊","报刊","期刊","刊物","期刊订购","原版图书","外文图书","纸质图书","图书供货","图书供应","图书购置","图书采购","图书资料","图书项目","古籍","书籍","电子图书","电子资源","全文","馆配","馆藏","订购","续订","增订","查阅","订阅","阅览","编目","唱片","平台采购","数据编制","数据处理","数据加工","数据获取","数据资源","数字资源","网络资源","资源建设","资料购买","软件租赁","爱思唯尔","外版","使用权","会议录"]
keyword_arr2 = ["图书","书","刊","库","报","软件","档案","资料","材料","数据","合集","电子","数字化","图书馆","索引"]

redis_ = redis.Redis(host=REDIS_IP, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
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
    while(True):
        if redis_.llen(FINISH_LIST_NAME) == 0:
            break
        string=redis_.lpop(FINISH_LIST_NAME)
        bean=standard_spider.Bean()
        bean.parser(string)
        bean.need = needs(bean)



        file.write(
            bean.name + "##" + bean.url + "##" + bean.date + "##" + bean.title + "##" + bean.text + "##" + bean.responsible+"##"+bean.need + "\n")

def needs(bean):
    for c, i in enumerate(keyword_arr1):
        if i in bean.cut:
            return  "y"
        elif c == len(keyword_arr1) - 1:
            for c2, j in enumerate(keyword_arr2):
                if j in bean.cut:
                   return java_part(bean.cut)
                elif c2 == len(keyword_arr2) - 1:
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
    # redis_.srem("cnpiec_47_set","http://ecp.cnnc.com.cn/xzbgg/66179.jhtml")
    query()
    # for key in redis_.keys("*"):
    #     redis_.delete(key)
