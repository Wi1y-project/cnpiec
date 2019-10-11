import threading
from  cnpiec.spider_modules import name_manager
import time

# def test_start(task_name,class_name):
#     pyfile = __import__("cnpiec.spider_thread." + task_name, fromlist=True)
#     f = getattr(pyfile, class_name)
#
#     nm = name_manager.Name_Manager(task_name+"_test")
#     f(nm).start()
#     f.join()
#     nm.delete_all()
#
# def test_end(task_name,class_name,url):
#     pyfile = __import__("cnpiec.spider_thread." + task_name, fromlist=True)
#     e = getattr(pyfile, class_name)
#
#     nm = name_manager.Name_Manager(task_name + "_test")
#     e(nm).test(url)

class A(threading.Thread):
    def __init__(self, stopevt=None, name='subthread', Type='event'):
        threading.Thread.__init__(self)
        self.stopevt = stopevt
        self.name = name
        self.Type = Type
        self.is_run=True

    def run(self):
        while(self.is_run):
            time.sleep(1)
            print(self.is_run)
            print("AAAAAAAAA")

        print("=======")


    def Eventrun(self):
        print("a stop!")
        self.is_run=False
        print(self.is_run)
        exit(0)


class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.a=None


    def run(self):
        print("------------")
        c=self.C(self.get,"c",1)
        c.setDaemon(True)
        c.start()
        c.join(1)
        print("++++++++++++",self.a)
        if c.is_alive():
            print("alive")
        else:
            print("dead",c.get_result())

        c = self.C(self.get, "cb", 2)
        c.setDaemon(True)
        c.start()
        c.join(1)
        print("++++++++++++", self.a)
        if c.is_alive():
            print("alive")
        else:
            print("dead", c.get_result())

        while (True):
            time.sleep(1)
            print(self.a)

    def use(self,a):
        print("aaaaaaaaa"+a)
        self.a = a

        while(True):
            time.sleep(2)
            self.a = a
            print("============",)
    def get(self,a):
        print("---------",a)
        self.use(a)

    class C(threading.Thread):
        def __init__(self, fun, args,version):
            threading.Thread.__init__(self)
            self.fun = fun
            self.args = args
            self.version=version
            self.result=None

        def run(self):
            self.fun(self.args)
            self.result="r"

        def get_result(self):
            return self.result




def get_a(num):
    print("----------",num)
    return "a"+str(num)

if __name__ == '__main__':
    # b=B(get_a,("c",))
    # b.setDaemon(True)
    # b.start()
    B().start()
    #
    # b.join(2)
    # print("-------------")
    #
    # time.sleep(2)

    # t=threading.Thread(target=get_a,args=('ADF',))
    # t.setDaemon(True)
    # t.start()


    # stop=threading.Event()
    # a=A(stopevt=stop)
    # # a.setDaemon(True)
    # a.start()
    # time.sleep(3)
    # print("thread:",a.is_alive())
    # stop.set()
    # time.sleep(1)
    # print("thread:",a.is_alive())
    #
    # time.sleep(1)
    # print("thread:",a.is_alive())

    # print(str(None))
    # taskname="cnpiec_45_A"
    # classname="thrid"
    # url="http://new.zmctc.com/zjgcjy/InfoDetail/?InfoID=fdfb461b-86cd-49ca-8215-80737d9a9d03&CategoryNum=004001001"
    # test_end(taskname,classname,url)
    # start_time = time.time()
    # while(time.time()<start_time+3):
    #     time.sleep(1)
    #     print(time.time())




