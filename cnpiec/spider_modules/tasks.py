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





logging.basicConfig(level = logging.INFO,format = common_keys.LOGGER_FORMAT)
logger=logging.getLogger("logger")
thread=[]
alive_thread=[]

def run():
    is_alive()
    thread.clear()
    conf = Conf_Parser()
    conf.read(common_keys.CONF_NAME,encoding="utf-8")

    logger.info("加载配置的爬虫...")
    for item in conf.items("task"):
        pyname=item[0]
        classes=item[1].split(",")
        if classes.__len__() != 2:
            raise ValueError("配置class数量有误。")
        run_single(pyname,classes[0],classes[1])

    for t in thread:
        t.start()


def run_single(pyname,first,second):
    logger.info("加载爬虫："+pyname+",起始线程："+first+",结束线程："+second)
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
    '''
    python自带模块读取conf中的cnpiec_1_A为cnpiec_1_a，该类读取为cnpiec_1_A
    '''
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr

def test():
    thread = []
    pyname = "cnpiec_14"
    first = "first"
    second = "thrid"
    # second = "second"

    run_single(pyname, first, second, thread)

    for t in thread:
        t.start()

    for t in thread:
        t.join()

def update_path():
    """
    将conf中path中设置的路径读取到common文件中
    :return:
    """
    logger.info("加载conf中配置的路径...")
    conf = ConfigParser()
    conf.read(common_keys.CONF_NAME, encoding="utf-8")
    for item in conf.items("path"):
        setattr(common_keys,item[0].upper(),item[1])


def set_log_file():
    """
    设置logger文件
    :return:
    """
    logger.info("加载log文件...")
    path=common_keys.LOGGER_PATH+"task_logger.log"
    fh=handlers.RotatingFileHandler(path)
    formater_str=logging.Formatter(common_keys.LOGGER_FORMAT)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formater_str)
    logger.addHandler(fh)

def is_alive():
    has_alive=False
    for t in thread:
        if t.is_alive():
            has_alive=True
            logger.info(t.get_name()+" 线程未结束！")
            alive_thread.append(t)

    if not  has_alive:
        logger.info("无未退出线程！")


if __name__ == '__main__':
    update_path()
    set_log_file()

    # test()
    # update_path()
    # run()

    # query()
    scheduler=BlockingScheduler()
    scheduler.add_job(func=run,trigger="cron",day="*",hour="*",minute="0,10,20,30,40,50")
    scheduler.start()

    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=test,trigger="cron",day="*",hour="14",minute="*")
    # scheduler.start()

