import logging
from logging import handlers
from cnpiec.spider_modules import name_manager
import os
import shutil
from configparser import ConfigParser
import datetime
import redis
from apscheduler.schedulers.blocking import BlockingScheduler

BACKUP_PATH="C:/SpiderResultFile"
COPY_PATH="C:/temp/file"
ERR_PATH="C:/temp/err"
LOGGER_PATH="C:/temp/loger.log"
LOGGER_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'




THULAC_MODEL_PATH='C:/File/soft/python36/Lib/site-packages/thulac/models'
CONF_NAME="conf.cfg"

logging.basicConfig(level = logging.INFO,format = LOGGER_FORMAT)
logger=logging.getLogger("logger")
fh=handlers.RotatingFileHandler(LOGGER_PATH)
formater_str=logging.Formatter(LOGGER_FORMAT)
fh.setLevel(logging.INFO)
fh.setFormatter(formater_str)
logger.addHandler(fh)


def run():
    conf = ConfigParser()
    conf.read(CONF_NAME)
    thread=[]
    for item in conf.items("task"):
        pyname=item[0]
        classes=item[1].split(",")
        if classes.__len__() != 2:
            raise ValueError("配置class数量有误。")

        pyfile = __import__("cnpiec.spider_thread." + pyname, fromlist=True)
        f=getattr(pyfile,classes[0])
        s=getattr(pyfile,classes[1])

        nm = name_manager.Name_Manager(pyname)

        thread.append(f(nm))
        thread.append(s(nm))

    for t in thread:
        t.start()

    for t in thread:
        t.join()

    file = create_file()
    name_manager.write_file(file)
    copy_file(file)
    name_manager.print_errs(ERR_PATH)



def create_file():
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)
    list = os.listdir(BACKUP_PATH)
    file_num = list.__len__()
    file_name = "CNPIEC_"
    return BACKUP_PATH + "/" + file_name + str(file_num).zfill(5) + "_" + str(datetime.datetime.now().date())

def copy_file(file):
    logger.info("开始复制文件...")
    if os.path.exists(COPY_PATH):
        os.remove(COPY_PATH)
    if not os.path.exists(file):
        logging.info("下载文件为空！")
    else:
        shutil.copy(file,COPY_PATH)

    logger.info("文件复制成功！")




def test():
    print(datetime.datetime.now(),"dfasd")


if __name__ == '__main__':
    run()
    # query()
    # scheduler=BlockingScheduler()
    # scheduler.add_job(func=run,trigger="cron",day="*",hour="0,12")
    # scheduler.start()

