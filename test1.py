
from pathlib import Path
import os
import subprocess
import threading
import time
import sys




class test1:

    class ag_class:
        def __init__(self) -> None:
            pass

    def __init__(self) -> None:
        print("ini")
        self.tmpdir=os.environ.get("HOME")+"/tmp"
        self.nagents=2
        self.ag_list=[]
        self.stopping=False
        pass

    def prc_sysclean(self):
        print("killing http.server ")
        cmd="kill $(pgrep -f \"http.server\")"
        subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd="ps -edf | grep python"
        subprocess.run(cmd, shell=True, text=True)

        pass
    def start_prc(self,ag):
        cmd= ["/usr/bin/python3", "-m", "http.server", ag.port ]
        ag.prc=subprocess.Popen(cmd,
                                cwd=ag.dir,
                                stdout=ag.stdout_txt,
                                stderr=ag.stderr_txt
                                )
        print(ag.prc.pid , "started")
        pass

    def start(self):

        for iagent in range(self.nagents):
            ag=self.ag_class()
            ag.dir=self.tmpdir+"/"+str(iagent)
            ag.dir_obj=Path(ag.dir)
            ag.dir_obj.mkdir(parents=True,exist_ok=True)
            ag.stdout_txt=open(ag.dir+ "/stdout.txt","w")
            ag.stderr_txt=open(ag.dir+ "/stderr.txt","w")
            ag.port=str(8080+iagent)

            self.start_prc(ag)
            self.ag_list.append(ag)
        self.stopping=False
        thr1=threading.Thread(target=self.monitor,daemon=True)
        thr1.start()

    def stop(self):
           self.stopping=True
           for ag in self.ag_list:
            print(f"terminating {ag.prc.pid} port {ag.port} ")

            ag.prc.terminate()
            ag.prc.wait()   #to avoid zombie

    def run(self):
        self.prc_sysclean()
        user_cmd=""
        while user_cmd != "end":
            user_cmd=input("==enter command : start/stop/end  \n")
            match user_cmd:
                case "start"|"s":
                    print("starting")
                    self.start()
                case "stop":
                    print("stopping")
                    self.stop()
                case "end":
                    print("ending  main ")
                    pass
                case _:
                    print("invalid ")

    def monitor(self):
        while True:
            time.sleep(5)
            print("checking")
            sys.stdout.flush()
            for ag in self.ag_list:
                print("pid", ag.prc.pid)
                if ag.prc.poll() is None :
                    print(f"live pid {ag.prc.pid} port {ag.port} ")
                else:
                    print(f"dead pid {ag.prc.pid} port {ag.port} ")
                    if self.stopping == False:
                        print(f"restarting ")
                        self.start_prc(ag)



if __name__ == "__main__" :

    t1=test1()
    t1.run()