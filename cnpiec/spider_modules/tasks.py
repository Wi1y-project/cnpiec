import logging
from logging import handlers
from cnpiec.spider_modules import name_manager
from cnpiec.spider_modules.common import common_keys
import os
import threading
from configparser import ConfigParser
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
from jpype import long

LOGGER_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# BACKUP_PATH="/home/ntrl"
# COPY_PATH="/home/ntrl/temp/file"
# ERR_PATH="/home/ntrl/temp/err"
# LOGGER_PATH="/home/ntrl/temp/loger.log"


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


class Conf_Parser(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr

def test():
    thread = []
    pyname = "cnpiec_44"
    first = "first"
    second = "thrid"
    # second = "second"

    run_single(pyname, first, second, thread)

    for t in thread:
        t.start()

    for t in thread:
        t.join()



if __name__ == '__main__':
    test()


    # query()
    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=run,trigger="cron",day="*",hour="*",minute="0,10,20,30,40,50")
    # scheduler.start()

    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=test,trigger="cron",day="*",hour="14",minute="*")
    # scheduler.start()

