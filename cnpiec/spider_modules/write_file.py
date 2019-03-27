import re
import os
from cnpiec.spider_modules.common import common_keys
from cnpiec.spider_modules import name_manager
from cnpiec.spider_modules import standard_spider
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime
import jpype
from jpype import *
from cnpiec.spider_modules.tasks import logger
import threading


jpype.startJVM(common_keys.jvmPath, "-Djava.class.path="+common_keys.JAR_PATH)

def create_single_file():
    if not os.path.exists(common_keys.FILE_PATH):
        os.mkdir(common_keys.FILE_PATH)
    return common_keys.FILE_PATH + "/CNPIEC.txt"



def run_write():
    logger.info("write start...")
    file=create_single_file()
    scheduler_thread().start()

    write_file(file)



def reset_num():
    while(True):
        if common_keys.ROWKEY_CONDITION.acquire():
            common_keys.KEY_NUM=0
            h = datetime.datetime.now().hour
            common_keys.LAST_ROWKEY_PROFIX = common_keys.ROWKEY_PROFIX
            if h < common_keys.SECOND_TIME:
                common_keys.ROWKEY_PROFIX = str(common_keys.KEY_TIME) + common_keys.FIRST_TIME_S
            else:
                common_keys.ROWKEY_PROFIX = str(common_keys.KEY_TIME) + common_keys.SECOND_TIME_S
            common_keys.ROWKEY_CONDITION.release()
            break
        else:
            common_keys.ROWKEY_CONDITION.wait()

def reset_time():
    while (True):
        if common_keys.ROWKEY_CONDITION.acquire():
            common_keys.KEY_NUM = 0


            d = time.mktime(datetime.datetime.now().date().timetuple())
            common_keys.KEY_TIME = sys.maxsize - long(d)
            h = datetime.datetime.now().hour
            common_keys.LAST_ROWKEY_PROFIX = common_keys.ROWKEY_PROFIX
            if h < common_keys.SECOND_TIME:
                common_keys.ROWKEY_PROFIX =str(common_keys.KEY_TIME)+common_keys.FIRST_TIME_S
            else:
                common_keys.ROWKEY_PROFIX=str(common_keys.KEY_TIME)+common_keys.SECOND_TIME_S
            print_errs(common_keys.ERR_PATH)
            common_keys.ROWKEY_CONDITION.release()
            break
        else:
            common_keys.ROWKEY_CONDITION.wait()
    # print_errs(common_keys.ERR_PATH)




def write_file(file_path):
    max_num = 0
    file=None
    rowkey_file=None

    while (True):
        if not name_manager.has_next(common_keys.FINISH_LIST_NAME):
            logger.info("无数据，等待中...")
            if file!=None:
                file.close()
            file = None
            time.sleep(common_keys.WAIT_TIME)
            continue
        logger.info("数据写入中...")
        string = name_manager.get(common_keys.FINISH_LIST_NAME)
        bean = standard_spider.Bean()
        bean.parser(string)
        bean.need = needs(bean)
        if common_keys.ROWKEY_CONDITION.acquire():
            if common_keys.KEY_NUM == 0 and max_num != 0:
                # print("reset+++++++++++++++++++")
                start_row ,end_row= create_start_end_rowkey(0,max_num)
                if rowkey_file ==None:
                    rowkey_file = open(common_keys.ROWKEY_PATH, "w+", encoding="UTF-8")
                rowkey_file.write(common_keys.NOTE + common_keys.START_ROW + "=" + start_row + "\n" + common_keys.END_ROW + "=" + end_row)
                rowkey_file.close()
                rowkey_file=None

            max_num = common_keys.KEY_NUM
            rowkey = create_rowkey(max_num)
            common_keys.ROWKEY_CONDITION.release()
        else:
            common_keys.ROWKEY_CONDITION.wait()
            continue


        common_keys.KEY_NUM += 1

        bean.year=re.search("\d{4}",bean.date).group()
        bean.fill_date=str(datetime.datetime.now().date())

        line = rowkey + "##" + bean.name + "##" +bean.customerid+"##"+bean.year+"##"+bean.flag+"##"+bean.title+"##"+bean.url+"##"+bean.fill_date+"##"+bean.date+"##"+bean.operator+"##"+bean.need+"##"+bean.text
        line = re.sub("\s+", " ", line)
        # rowkey_file.write(rowkey+"\n")
        if file==None:
            file = open(file_path, "w+", encoding="utf-8")
        file.write(line + "\n")

def print_errs(file):

    if name_manager.has_next(common_keys.REDIS_ERR_NAME):
        err_file=open(file,"a+",encoding="utf-8")
        while(name_manager.has_next(common_keys.REDIS_ERR_NAME)):
            line=name_manager.get(common_keys.REDIS_ERR_NAME)
            err_file.write(str(datetime.datetime.now())+" "+line+"\n")



def create_rowkey(i):
    if common_keys.KEY_TIME==None:
        reset_time()
    return common_keys.ROWKEY_PROFIX+str.zfill(str(i), 5)

def create_start_end_rowkey(start,end):
    return common_keys.LAST_ROWKEY_PROFIX+str.zfill(str(start), 5),common_keys.LAST_ROWKEY_PROFIX+str.zfill(str(end), 5)


def needs(bean):
    for c0,key in enumerate(common_keys.keyword_arr3):
        if key in bean.title:
            return "n"
    for c, i in enumerate(common_keys.keyword_arr1):
        if i in bean.title:
            return  "y"
        elif c == len(common_keys.keyword_arr1) - 1:
            for c2, j in enumerate(common_keys.keyword_arr2):
                if j in bean.title:
                   return java_part(bean.cut)
                   #  pass
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

class scheduler_thread(threading.Thread):
    def run(self):
        scheduler = BlockingScheduler()
        # scheduler.add_job(func=reset_num,trigger="cron",day="*",hour=common_keys.SECOND_TIME)
        # scheduler.add_job(func=reset_time, trigger="cron", day="*", hour="0")

        scheduler.add_job(func=reset_time, trigger="cron", day="*", hour="*", minute="*")
        scheduler.start()





if __name__ == '__main__':
    run_write()
    # bean=standard_spider.Bean()
    # bean.title="兵团检察院“两房”室内设计装修项目招标公告"
    # print(needs(bean))
    #
    # string="2019-01-05"
    # print(datetime.datetime.now().date())
    # start_row = create_rowkey(0)
    # end_row = create_rowkey(10)
    # rowkey_file = open(common_keys.ROWKEY_PATH, "w+", encoding="UTF-8")
    # print(common_keys.NOTE + common_keys.START_ROW + "=" + start_row + "\n" + common_keys.END_ROW + "=" + end_row)
    # rowkey_file.write( common_keys.NOTE + common_keys.START_ROW + "=" + start_row + "\n" + common_keys.END_ROW + "=" + end_row)



