import logging
from logging import handlers
from cnpiec.spider_modules import name_manager
import os
import shutil
from configparser import ConfigParser
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import jpype






LOGGER_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# BACKUP_PATH="/home/ntrl"
# COPY_PATH="/home/ntrl/temp/file"
# ERR_PATH="/home/ntrl/temp/err"
# LOGGER_PATH="/home/ntrl/temp/loger.log"






class common_keys:
    FIRST_TIME=6
    SECOND_TIME=18
    REDIS_IP = "10.3.1.99"
    REDIS_PORT = "6379"
    REDIS_DB = "12"
    jvmPath = 'C:/File/soft/java/jre1.8/bin/server/jvm.dll'
    JAR_PATH="/home/classifier.jar"
    THULAC_MODEL_PATH = 'C:/File/soft/python36/Lib/site-packages/thulac/models'
    URL_NAME = "url"
    DATE_NAME = "date"
    TITLE_NEME = "title"
    TEXT_NEME = "text"
    RETRY_NEME = "retry"
    ERR_NAME = "err"
    TITLE_CUT = "cut"
    NAME = "name"
    RESPONSIBLE = "responsible"
    NEED = "need"

    #文件下载路径
    FILE_PATH = "C:/SpiderResultFile"
    #复制文件路径，暂时不用
    COPY_PATH = "C:/temp/file"

    #错误文件路径
    ERR_PATH = "C:/temp/err"

    #写日志的文件路径
    LOGGER_PATH = "C:/temp/loger.log"

    CONF_NAME = "conf.cfg"


    keyword_arr1 = ["文献", "纸质", "纸本", "数据库", "画册", "杂志", "书刊", "报刊", "期刊", "刊物", "期刊订购", "原版图书", "外文图书", "纸质图书", "图书供货",
                    "图书供应", "图书购置", "图书采购", "图书资料", "图书项目", "古籍", "书籍", "电子图书", "电子资源", "全文", "馆配", "馆藏", "订购", "续订",
                    "增订", "查阅", "订阅", "阅览", "编目", "唱片", "平台采购", "数据编制", "数据处理", "数据加工", "数据获取", "数据资源", "数字资源", "网络资源",
                    "资源建设", "资料购买", "软件租赁", "爱思唯尔", "外版", "使用权", "会议录"]
    keyword_arr2 = ["图书", "书", "刊", "库", "报", "软件", "档案", "资料", "材料", "数据", "合集", "电子", "数字化", "图书馆", "索引"]




logging.basicConfig(level = logging.INFO,format = LOGGER_FORMAT)
logger=logging.getLogger("logger")
fh=handlers.RotatingFileHandler(common_keys.LOGGER_PATH)
formater_str=logging.Formatter(LOGGER_FORMAT)
fh.setLevel(logging.ERROR)
fh.setFormatter(formater_str)
logger.addHandler(fh)


def run():
    # conf = ConfigParser()
    conf = Conf_Parser()
    conf.read(common_keys.CONF_NAME)
    thread=[]
    for item in conf.items("task"):
        pyname=item[0]
        classes=item[1].split(",")
        if classes.__len__() != 2:
            raise ValueError("配置class数量有误。")
        run_single(pyname,classes[0],classes[1],thread)

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    # file = create_file()
    file=create_single_file()
    rowkey_file=create_rowkey_file()
    name_manager.write_file(file,rowkey_file)
    # copy_file(file)
    name_manager.print_errs(common_keys.ERR_PATH)


def run_single(pyname,first,second,thread):
    pyfile = __import__("cnpiec.spider_thread." + pyname, fromlist=True)
    f = getattr(pyfile, first)
    s = getattr(pyfile, second)

    nm = name_manager.Name_Manager(pyname)

    thread.append(f(nm))
    thread.append(s(nm))

def create_file():
    if not os.path.exists(common_keys.FILE_PATH):
        os.mkdir(common_keys.FILE_PATH)
    list = os.listdir(common_keys.FILE_PATH)
    file_num = list.__len__()
    file_name = "CNPIEC_"
    return common_keys.FILE_PATH + "/" + file_name + str(file_num).zfill(5) + "_" + str(datetime.datetime.now().date())
def create_single_file():
    if not os.path.exists(common_keys.FILE_PATH):
        os.mkdir(common_keys.FILE_PATH)
    return common_keys.FILE_PATH + "/CNPIEC.txt"

def create_rowkey_file():
    return common_keys.FILE_PATH+"/ROWKEY.txt"

# def copy_file(file):
#     logger.info("开始复制文件...")
#     if os.path.exists(COPY_PATH):
#         os.remove(COPY_PATH)
#     if not os.path.exists(file):
#         logging.info("下载文件为空！")
#     else:
#         shutil.copy(file,COPY_PATH)
#
#     logger.info("文件复制成功！")


class Conf_Parser(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr



def test():
    print("start...")
    time.sleep(120)
    print("done!")


if __name__ == '__main__':
    thread=[]
    pyname="cnpiec_30"
    first="first"
    second="thrid"

    run_single(pyname,first,second,thread)

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    file = create_single_file()
    rowkey_file=create_rowkey_file()
    name_manager.write_file(file,rowkey_file)
    # copy_file(file)
    name_manager.print_errs(common_keys.ERR_PATH)
    # query()
    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=run,trigger="cron",day="*",hour="0,12")
    # scheduler.start()

    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=test,trigger="cron",day="*",hour="14",minute="*")
    # scheduler.start()

