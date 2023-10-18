
from pathlib import Path
import os
import subprocess
import time

class test1:

    def __init__(self) -> None:
        print("ini")
        self.tmpdir=os.environ.get("HOME")+"/tmp"
        self.nagents=2
        self.prc_list=[]
        pass

    def start(self):
        for iagent in range(self.nagents):
            ag_dir=self.tmpdir+"/"+str(iagent)
            ag_dir_obj=Path(ag_dir)
            ag_dir_obj.mkdir(parents=True,exist_ok=True)
            stdout_txt=open(ag_dir+ "/stdout.txt","w")
            stderr_txt=open(ag_dir+ "/stderr.txt","w")
            port=8080+iagent
            cmd= ["/usr/bin/python3", "-m", "http.server", str(port) ]
            prc=subprocess.Popen(cmd,
                                 cwd=ag_dir,
                                 stdout=stdout_txt,
                                 stderr=stderr_txt
                                 )
            self.prc_list.append(prc)

    def stop(self):
        for prc in self.prc_list:
            print("terminating ", prc)

            prc.terminate()

    def run(self):
        user_cmd=""
        while user_cmd != "end":
            user_cmd=input("==enter command : start/stop/end  \n")
            match user_cmd:
                case "start":
                    print("starting")
                    self.start()
                case "stop":
                    print("stopping")
                    self.stop()
                case "end":
                    pass


if __name__ == "__main__" :

    t1=test1()
    t1.run()