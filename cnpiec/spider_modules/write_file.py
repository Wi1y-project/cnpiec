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
import thulac


jpype.startJVM(common_keys.jvmPath, "-Djava.class.path="+common_keys.JAR_PATH)
thu1 = thulac.thulac(model_path=common_keys.THULAC_MODEL_PATH)
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
            common_keys.LAST_ROWKEY_PROFIX = common_keys.ROWKEY_PROFIX
            set_rowkey_profix()
            common_keys.ROWKEY_CONDITION.release()
            break
        else:
            common_keys.ROWKEY_CONDITION.wait()

def reset_time():
    while (True):
        if common_keys.ROWKEY_CONDITION.acquire():
            common_keys.KEY_NUM = 0

            # d = time.time()
            d = time.mktime(datetime.datetime.now().date().timetuple())
            common_keys.KEY_TIME = sys.maxsize - long(d)

            common_keys.LAST_ROWKEY_PROFIX = common_keys.ROWKEY_PROFIX
            set_rowkey_profix()
            print_errs(common_keys.ERR_PATH)
            name_manager.set_string(common_keys.KEY_TIME_NAME,str(common_keys.KEY_TIME))
            common_keys.ROWKEY_CONDITION.release()
            break
        else:
            common_keys.ROWKEY_CONDITION.wait()
    # print_errs(common_keys.ERR_PATH)

def set_rowkey_profix():
    h = datetime.datetime.now().hour
    if h < common_keys.SECOND_TIME:
        name_manager.set_string(common_keys.KEY_TIME_S_NAME,common_keys.FIRST_TIME_S)
        common_keys.ROWKEY_PROFIX =str(common_keys.KEY_TIME)+"_"+common_keys.FIRST_TIME_S
    else:
        name_manager.set_string(common_keys.KEY_TIME_S_NAME, common_keys.SECOND_TIME_S)
        common_keys.ROWKEY_PROFIX=str(common_keys.KEY_TIME)+"_"+common_keys.SECOND_TIME_S

def write_file(file_path):
    max_num = load_num()
    common_keys.KEY_NUM=max_num
    file=None

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
            # print("================",max_num)
            # print("==========",common_keys.KEY_NUM)
            if common_keys.KEY_NUM == 0 and max_num != 0:
                write_rowkey(max_num)

            max_num = common_keys.KEY_NUM
            rowkey = create_rowkey(max_num)
            common_keys.KEY_NUM += 1
            name_manager.set_string(common_keys.KEY_NUM_NAME,str(max_num))
            common_keys.ROWKEY_CONDITION.release()
        else:
            common_keys.ROWKEY_CONDITION.wait()
            continue

        bean.year=re.search("\d{4}",bean.date).group()
        bean.fill_date=str(datetime.datetime.now().date())

        bean.cut = do_cut(bean.title)
        bean.responsible = responsible(bean.url)
        print(bean.cut,bean.responsible)
        line = rowkey + "##" + bean.name + "##" + bean.customerid + "##" + bean.year + "##" + bean.flag + "##" + bean.title + "##" + bean.url + "##" + bean.fill_date + "##" + bean.date + "##" + bean.operator + "##" + bean.need + "##" + bean.text


        line = re.sub("\s+", " ", line)
        # rowkey_file.write(rowkey+"\n")
        if file==None:
            file = open(file_path, "w+", encoding="utf-8")
        file.write(line + "\n")

def do_cut(title):
    a = ""
    cuts = thu1.cut(title, text=False)
    for i in cuts:
        if 'n' == i[1] or 'v' == i[1] or 'a' == i[1] or 'j' == i[1] or 'x' == i[1] or 'd' == i[1] or 'g' == i[1]:
            a += i[0] + ' '
    return a

def responsible(site):

    if '/' in site.replace('http://', '').replace('https://', ''):
        site = site.replace('http://', '').replace('https://', '').split('/')[0].strip()
    else:
        site = site.replace('http://', '').replace('https://', '').strip()

    site_map = {
        'www.gzsggzyjyzx.cn': '王洋',
        'www.ccgp-jiangsu.gov.cn': '何一石',
        'www.ccgp-shandong.gov.cn': '孟宏权',
        'cgb.xjtu.edu.cn': '秦超,刘波',
        'ggzy.xjbt.gov.cn': '刘波',
        'zbxx.ycit.cn': '王美怡',
        'www.ccgp-yancheng.gov.cn': '何一石',
        'www.zjzfcg.gov.cn': '董伟琨',
        'www.bidchance.com': '孟宏权,杨跃,高世明,张琦,杨跃,杜士荣,秦超,赵潇潇,刘柳,姜波,郑子玉,沈婧男,肖俊文,李东海',
        'www.ccgp.gov.cn': '王雪娟,肖俊文,刘波,刘向平,孟宏权,刘波,师光辉,张洁,骆金伟,李晓光,金丽荣,姜波,沈婧男,赵潇潇,李东海,孙秀焕,杨跃,王洋,刘默'
    }

    try:
        return site_map[site]
    except:
        return '无负责人'

def write_rowkey(max_num):
    start_row, end_row = create_start_end_rowkey(0, max_num)
    rowkey_file = open(common_keys.ROWKEY_PATH, "w+", encoding="UTF-8")
    rowkey_history=open(common_keys.ROWKEY_HISTORY_PATH,"a+",encoding="utf-8")
    rowkey_file.write(
        common_keys.NOTE + common_keys.START_ROW + "=" + start_row + "\n" + common_keys.END_ROW + "=" + end_row)
    rowkey_history.write(str(datetime.datetime.now().date())+"    start:"+start_row+"    end:"+end_row+"\n")
    rowkey_history.close()
    rowkey_file.close()

def load_num():
    '''
    从redis中读取上次停止前的rowkey数据，并判断是否更新rowkey文件
    :return:
    '''
    temp_num=name_manager.get_string(common_keys.KEY_NUM_NAME)
    temp_time=name_manager.get_string(common_keys.KEY_TIME_NAME)
    temp_s=name_manager.get_string(common_keys.KEY_TIME_S_NAME)

    # print(temp_num,temp_time,temp_s)
    if temp_num ==None:
        return 0

    d = time.mktime(datetime.datetime.now().date().timetuple())
    common_keys.KEY_TIME = sys.maxsize - long(d)

    if common_keys.KEY_TIME ==int(temp_time):
        h = datetime.datetime.now().hour
        if h < common_keys.SECOND_TIME:
            common_keys.ROWKEY_PROFIX = str(common_keys.KEY_TIME) + "_" + common_keys.FIRST_TIME_S
            return int(temp_num)
        else:
            if temp_s =="1":
                common_keys.LAST_ROWKEY_PROFIX=temp_time+"_"+temp_s
                write_rowkey(int(temp_num))
                return 0
            else:
                return int(temp_num)
    else:
        common_keys.LAST_ROWKEY_PROFIX = temp_time + "_" + temp_s
        write_rowkey(int(temp_num))
        return 0

def print_errs(file):
    if name_manager.has_next(common_keys.REDIS_ERR_NAME):
        err_file=open(file,"a+",encoding="utf-8")
        while(name_manager.has_next(common_keys.REDIS_ERR_NAME)):
            line=name_manager.get(common_keys.REDIS_ERR_NAME)
            err_file.write(str(datetime.datetime.now())+" "+line+"\n")

def create_rowkey(i):
    if common_keys.KEY_TIME==None :
        reset_time()
    if common_keys.ROWKEY_PROFIX ==None:
        set_rowkey_profix()
    return common_keys.ROWKEY_PROFIX+"_"+str.zfill(str(i), 5)

def create_start_end_rowkey(start,end):
    return common_keys.LAST_ROWKEY_PROFIX+"_"+str.zfill(str(start), 5),common_keys.LAST_ROWKEY_PROFIX+"_"+str.zfill(str(end), 5)


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
        scheduler.add_job(func=reset_num,trigger="cron",day="*",hour=common_keys.SECOND_TIME)
        scheduler.add_job(func=reset_time, trigger="cron", day="*", hour="0")

        #scheduler.add_job(func=reset_time, trigger="cron", day="*", hour="*", minute="*")
        scheduler.start()





if __name__ == '__main__':
    run_write()
    # reset_time()
    # print(datetime.datetime.now().date())
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



