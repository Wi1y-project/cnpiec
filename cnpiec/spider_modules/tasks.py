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


BACKUP_PATH="C:/SpiderResultFile"
COPY_PATH="C:/temp/file"
ERR_PATH="C:/temp/err"
LOGGER_PATH="C:/temp/loger.log"
LOGGER_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'





CONF_NAME="conf.cfg"

logging.basicConfig(level = logging.INFO,format = LOGGER_FORMAT)
logger=logging.getLogger("logger")
fh=handlers.RotatingFileHandler(LOGGER_PATH)
formater_str=logging.Formatter(LOGGER_FORMAT)
fh.setLevel(logging.ERROR)
fh.setFormatter(formater_str)
logger.addHandler(fh)


def run():
    # conf = ConfigParser()
    conf = Conf_Parser()
    conf.read(CONF_NAME)
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

    file = create_file()
    name_manager.write_file(file)
    copy_file(file)
    name_manager.print_errs(ERR_PATH)


def run_single(pyname,first,second,thread):
    pyfile = __import__("cnpiec.spider_thread." + pyname, fromlist=True)
    f = getattr(pyfile, first)
    s = getattr(pyfile, second)

    nm = name_manager.Name_Manager(pyname)

    thread.append(f(nm))
    thread.append(s(nm))

def create_file():
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)
    list = os.listdir(BACKUP_PATH)
    file_num = list.__len__()
    file_name = "CNPIEC_"
    return BACKUP_PATH + "/" + file_name + str(file_num).zfill(5) + "_" + str(datetime.datetime.now().date())
def create_single_file():
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)
    return BACKUP_PATH + "/CNPIEC.txt"

def copy_file(file):
    logger.info("开始复制文件...")
    if os.path.exists(COPY_PATH):
        os.remove(COPY_PATH)
    if not os.path.exists(file):
        logging.info("下载文件为空！")
    else:
        shutil.copy(file,COPY_PATH)

    logger.info("文件复制成功！")


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
    name_manager.write_file(file)
    copy_file(file)
    name_manager.print_errs(ERR_PATH)
    # query()
    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=run,trigger="cron",day="*",hour="0,12")
    # scheduler.start()

    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=test,trigger="cron",day="*",hour="14",minute="*")
    # scheduler.start()

