
from  cnpiec.spider_modules import name_manager
import time

def test_start(task_name,class_name):
    pyfile = __import__("cnpiec.spider_thread." + task_name, fromlist=True)
    f = getattr(pyfile, class_name)

    nm = name_manager.Name_Manager(task_name+"_test")
    f(nm).start()
    f.join()
    nm.delete_all()

def test_end(task_name,class_name,url):
    pyfile = __import__("cnpiec.spider_thread." + task_name, fromlist=True)
    e = getattr(pyfile, class_name)

    nm = name_manager.Name_Manager(task_name + "_test")
    e(nm).test(url)


if __name__ == '__main__':
    # taskname="cnpiec_45_A"
    # classname="thrid"
    # url="http://new.zmctc.com/zjgcjy/InfoDetail/?InfoID=fdfb461b-86cd-49ca-8215-80737d9a9d03&CategoryNum=004001001"
    # test_end(taskname,classname,url)
    start_time = time.time()
    while(time.time()<start_time+3):
        time.sleep(1)
        print(time.time())




