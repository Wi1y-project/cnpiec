import re
import os
from cnpiec.spider_modules.common import common_keys
from cnpiec.spider_modules import name_manager
from cnpiec.spider_modules import standard_spider
import time
import datetime
import jpype
from jpype import *
import logging
from logging import handlers
from configparser import ConfigParser
import thulac


logging.basicConfig(level = logging.INFO,format = common_keys.LOGGER_FORMAT)
logger=logging.getLogger("writefile_logger")



def create_single_file():
    '''
    检查写入文件的路径是否存在
    :return:
    '''
    logger.info("检查写入文件路径："+common_keys.FILE_PATH + "/CNPIEC.txt")
    if not os.path.exists(common_keys.FILE_PATH):
        os.mkdir(common_keys.FILE_PATH)
    return common_keys.FILE_PATH + "/CNPIEC.txt"

def run_write():
    logger.info("write file 启动，加载数据...")
    update_path()
    set_logger_file()
    logger.info("加载jvm...")
    jpype.startJVM(common_keys.JVM_PATH, "-Djava.class.path=" + common_keys.JAR_PATH)
    logger.info("加载切词器...")
    thu1 = thulac.thulac(model_path=common_keys.THULAC_MODEL_PATH)

    file=create_single_file()

    write_file(file,thu1)

def set_logger_file():
    logger.info("加载log文件...")
    log_file = common_keys.LOGGER_PATH + "writefile_logger.log"
    fh = handlers.RotatingFileHandler(log_file)
    formater_str = logging.Formatter(common_keys.LOGGER_FORMAT)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formater_str)
    logger.addHandler(fh)

def set_rowkey_profix():
    """
    获取当前时间，设定当前rowkey的前缀
    :return:
    """
    logger.info("设置rowkey前缀。")
    if common_keys.ROWKEY_PROFIX!=None:
        common_keys.LAST_ROWKEY_PROFIX=common_keys.ROWKEY_PROFIX

    #获取当天时间（long）
    d = time.mktime(datetime.datetime.now().date().timetuple())
    common_keys.KEY_TIME = sys.maxsize - long(d)
    name_manager.set_string(common_keys.KEY_TIME_NAME,common_keys.KEY_TIME)

    h = datetime.datetime.now().hour
    if h < common_keys.SECOND_TIME:
        name_manager.set_string(common_keys.KEY_TIME_S_NAME,common_keys.FIRST_TIME_S)
        common_keys.ROWKEY_PROFIX = create_rowkey_profix(common_keys.KEY_TIME,common_keys.FIRST_TIME_S)#str(common_keys.KEY_TIME)+"_"+common_keys.FIRST_TIME_S
    else:
        name_manager.set_string(common_keys.KEY_TIME_S_NAME, common_keys.SECOND_TIME_S)
        common_keys.ROWKEY_PROFIX=create_rowkey_profix(common_keys.KEY_TIME,common_keys.SECOND_TIME_S)#str(common_keys.KEY_TIME)+"_"+common_keys.SECOND_TIME_S

def write_file(file_path,thu1):
    '''
    读取数据写入文件中
    :param file_path:
    :return:
    '''

    max_num = load_num()

    common_keys.KEY_NUM=max_num
    file=None
    logger.info("数据加载结束：rowkey num=" + str(
        common_keys.KEY_NUM) + ",rowkey profix=" + common_keys.ROWKEY_PROFIX + ",last rowkey profix=" + str(common_keys.LAST_ROWKEY_PROFIX))
    while (True):

        logger.info("检查rowkey...")
        set_rowkey_profix()
        if common_keys.LAST_ROWKEY_PROFIX != common_keys.ROWKEY_PROFIX:
            logger.info("rowkey前缀改变，更新rowkey文件。")
            write_rowkey(max_num)
            max_num = 0

        if not name_manager.has_next(common_keys.FINISH_LIST_NAME):
            logger.info("无数据，等待中...")
            if file!=None:
                file.close()
            file = None
            time.sleep(common_keys.WAIT_TIME)
            continue

        logger.info("检查到数据，开始生成rowkey...")
        rowkey = create_rowkey(max_num)
        name_manager.set_string(common_keys.KEY_NUM_NAME,str(max_num))
        max_num += 1

        logger.info("生成rowkey："+rowkey+",开始写数据...")
        string = name_manager.get(common_keys.FINISH_LIST_NAME)
        bean = standard_spider.Bean()
        bean.parser(string)
        bean.cut = do_cut(bean.title,thu1)
        bean.need = needs(bean)
        bean.year=re.search("\d{4}",bean.date).group()
        bean.fill_date=str(datetime.datetime.now().date())

        bean.responsible = responsible(bean.url)
        line = rowkey + "##" + bean.name + "##" + bean.customerid + "##" + bean.year + "##" + bean.flag + "##" + bean.title + "##" + bean.url + "##" + bean.fill_date + "##" + bean.date + "##" + bean.operator + "##" + bean.need + "##" + bean.text

        line = re.sub("\s+", " ", line)
        # rowkey_file.write(rowkey+"\n")
        if file==None:
            file = open(file_path, "w+", encoding="utf-8")
        file.write(line + "\n")

def do_cut(title,thu1):
    logger.info("开始切词...")
    a = ""
    cuts = thu1.cut(title, text=False)
    for i in cuts:
        if 'n' == i[1] or 'v' == i[1] or 'a' == i[1] or 'j' == i[1] or 'x' == i[1] or 'd' == i[1] or 'g' == i[1]:
            a += i[0] + ' '
    return a

def responsible(site):
    '''
    设置负责人
    :param site:
    :return:
    '''

    logger.info("设置负责人...")
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
    '''
    更新rowkey文件（两个：一个当前使用，一个历史记录）
    :param max_num:
    :return:
    '''
    logger.info("更新rowkey文件...")
    start_row, end_row = create_start_end_rowkey(0, max_num)
    logger.info("起始rowkey："+start_row+"\t结束rowkey："+end_row)
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
    logger.info("加载rowkey数据...")
    temp_num=name_manager.get_string(common_keys.KEY_NUM_NAME)
    temp_time=name_manager.get_string(common_keys.KEY_TIME_NAME)
    temp_s=name_manager.get_string(common_keys.KEY_TIME_S_NAME)

    # print(temp_num,temp_time,temp_s)


    set_rowkey_profix()
    logger.info("当前时间段的rowkey前缀为："+common_keys.ROWKEY_PROFIX)

    if temp_num ==None:
        logger.info("rowkey num为空。")
        return 0

    temp_profix=create_rowkey_profix(temp_time,temp_s)
    logger.info("读取到redis中存储的rowkey前缀为："+temp_profix)

    if temp_profix == common_keys.ROWKEY_PROFIX:
        logger.info("读取到当前时间段的rowkey前缀，使用读取到的rowkey数据。")
        return  int(temp_num)
    else:
        logger.info("读取到其他时间段的rowkey前缀，更新rowkey文件。")
        common_keys.LAST_ROWKEY_PROFIX=temp_profix
        write_rowkey(int(temp_num))
        return 0


    # if common_keys.KEY_TIME ==int(temp_time):
    #
    #     h = datetime.datetime.now().hour
    #     if h < common_keys.SECOND_TIME:
    #         logger.info("创建rowkey前缀。")
    #         common_keys.ROWKEY_PROFIX = str(common_keys.KEY_TIME) + "_" + common_keys.FIRST_TIME_S
    #         return int(temp_num)
    #     else:
    #         if temp_s =="1":
    #             common_keys.LAST_ROWKEY_PROFIX=temp_time+"_"+temp_s
    #             write_rowkey(int(temp_num))
    #             return 0
    #         else:
    #             return int(temp_num)
    # else:
    #     common_keys.LAST_ROWKEY_PROFIX = temp_time + "_" + temp_s
    #     write_rowkey(int(temp_num))
    #     return 0

def create_rowkey_profix(r_time,r_temp_s):
    return str(r_time)+ "_" +str(r_temp_s)


# def print_errs(file):
#     if name_manager.has_next(common_keys.REDIS_ERR_NAME):
#         err_file=open(file,"a+",encoding="utf-8")
#         while(name_manager.has_next(common_keys.REDIS_ERR_NAME)):
#             line=name_manager.get(common_keys.REDIS_ERR_NAME)
#             err_file.write(str(datetime.datetime.now())+" "+line+"\n")

def create_rowkey(i):
    '''
    生成rowkey
    :param i:
    :return:
    '''
    if common_keys.KEY_TIME==None :
        d = time.mktime(datetime.datetime.now().date().timetuple())
        common_keys.KEY_TIME = sys.maxsize - long(d)
    if common_keys.ROWKEY_PROFIX ==None:
        set_rowkey_profix()
    return common_keys.ROWKEY_PROFIX+"_"+str.zfill(str(i), 5)

def create_start_end_rowkey(start,end):
    '''
    根据传入的数字，生成起始和结束的rowkey
    :param start:
    :param end:
    :return:
    '''
    start_rowkey=str(common_keys.LAST_ROWKEY_PROFIX)+"_"+str.zfill(str(start), 5)
    end_rowkey=str(common_keys.LAST_ROWKEY_PROFIX)+"_"+str.zfill(str(end), 5)
    return start_rowkey,end_rowkey


def needs(bean):
    '''
    判断该数据是否需要
    :param bean:
    :return:
    '''
    logger.info("开始生成标签")
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


def update_path():
    """
    将conf中path中设置的路径读取到common文件中
    :return:
    """
    logger.info("加载conf中配置的路径...")
    conf = ConfigParser()
    conf.read(common_keys.CONF_NAME, encoding="utf-8")
    for item in conf.items("path"):
        setattr(common_keys, item[0].upper(), item[1])

def test():
    t = datetime.datetime.strptime("2019-11-29", "%Y-%m-%d")
    d = time.mktime(t.timetuple())
    print(t.date())
    a = sys.maxsize - long(d)
    print(a)


if __name__ == '__main__':
    run_write()

    # d = time.mktime(datetime.datetime.now().date().timetuple())






