
from enum import Enum
import pprint,time,inspect
from datetime import datetime,date

import json
from shlex import split

import os
import threading
import subprocess

pp = pprint.PrettyPrinter(indent=4)
class cnt_list(Enum):
    CNT_DOCKER=1
    CNT_K8S=2
    CNT_XBENCH=3

class utz:

    compare_mode=False

    @staticmethod
    def logset(log_folder=""):
        utz.log_folder=log_folder
        utz.log_name=utz.log_folder+"/utz.log"
        utz.log=open(utz.log_name,"w")
        utz.test_result=None
        utz.test_cum_rc=0

    @staticmethod
    def print(*var):
        print(str(datetime.now()),*(x for x in var))
        if hasattr(utz,'log'):
            # common log
            print(str(datetime.now()),*(x for x in var),file=utz.log)
            utz.log.flush()
            # test result only inside of test
            if utz.test_result !=  None:
                print(*(x for x in var),file=utz.test_result)
                utz.test_result.flush()


    @staticmethod
    def enter(*var):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name
        the_thread = str(threading.get_native_id())
        str1=str(datetime.now()) + "enter ==" \
                +"thr" \
                +the_thread \
                +the_class  \
                +":" \
                +the_method
                # ,sys._getframe(1).f_code
                # ,sys._getframe(1).f_code.co_name
        utz.print("enter  : ",str1,*(x for x in var))


    @staticmethod
    def enter2(*var):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name
        #create result file
        if utz.log_folder != "":
           utz.test_result_fn= utz.log_folder + "/" + the_method + ".result"
           utz.test_result=open(utz.test_result_fn,"w")

        str1= the_class.ljust(8," ")+":::::::::::::: "+the_method
        utz.print("enter  : ",str1,*(x for x in var))

    @staticmethod
    def exit2(*var):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name
        str1= the_class.ljust(8," ")+":::::::::::::: "+the_method
        utz.print("exit  : ",str1,*(x for x in var))
        if utz.log_folder != "":
            utz.test_result.close()
            utz.test_result=None
            if utz.compare_mode==True:
                utz.test_result_base_fn=os.path.realpath(os.path.dirname(__file__))+"/suites/multi_node/r/"+the_method+".result"
                rc, _ =uos.uoscall_live_output(uos, "diff -s {} {}  ".format(utz.test_result_fn,utz.test_result_base_fn))
                utz.test_cum_rc=max(rc,utz.test_cum_rc)


    @staticmethod
    def pprint(*var):
        print(str(datetime.now()))
        pp.pprint(var)

    @staticmethod
    # help serialize
    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))

    @staticmethod
    # print json with special datatype (datetime)
    def jprint(var):
        var1=utz.jstring(var)
        utz.print(var1)


    @staticmethod
    # serialize
    def jstring(var):
        return json.dumps(var, indent=True,default=utz.json_serial)

    @staticmethod
    #sleep with explanation
    def sleep(n,txt=""):
        if txt=="" :
            txt="sleeping "
        utz.print(txt,n)
        time.sleep(n)


#os commands etc
class uos:

    def __init__(self):
        utz.print("init uos")
        self.rc=0

    #print stdout without accumaulation/wait
    def uoscall_live_output(self,cmd,gcloud_mixup=False,silent=False):

        if silent==False :
            utz.print("command ===", cmd)
        resp=subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        while True:
            # utz.print("call readlines on stdout blocking ")
            output = resp.stdout.readline().decode("utf-8")
            # output = resp.stderr.readline().decode("utf-8")
            if gcloud_mixup :
                output = resp.stderr.readline().decode("utf-8")
            if output != '' and "tar: Removing leading" not in output :
                #this happens on last line
                tmp1=output.strip()
                utz.print (output.strip())
                time.sleep(.05)
                # utz.print (output.strip()+" xxxxx")
                # utz.print ("ddddd\n")
            else:
                break
                # utz.print ("EOF on STDOUT")
                # pass
            #check if sub finished
        rc=resp.poll()
        stderr=""
        if rc != 0:
            stderr = resp.stderr.read().decode("utf-8")
            utz.print("rc = ",rc, "stderr = ", stderr)

        return rc, stderr


class UtzExc(BaseException):
    def __init__(self,code,txt,dbmstxt):
        self._code=code
        self._txt=txt
        self._dbmstxt=dbmstxt
    def show(self):
        utz.print("Utz exception!!!:\n code={}, \n text=<{}> \n dbmstext=<{}>".format(self._code, self._txt,self._dbmstxt))
