import redis
import threading
import datetime
from  cnpiec.spider_modules import tasks,standard_spider

REDIS_IP="10.3.1.99"
REDIS_PORT="6379"
REDIS_DB="12"


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
        file.write(
            bean.name + "##" + bean.url + "##" + bean.date + "##" + bean.title + "##" + bean.text + "##" + bean.responsible+"##"+bean.need + "\n")


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
