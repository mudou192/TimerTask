#coding=utf8
'''
Created on 2017-6-6

@author: xuwei

@summary: 任务管理器
'''
import time
import tasks
from timer import Wheel
from timer.logger import Logger

class TaskManager(Logger):
    def __init__(self):
        Logger.__init__(self)
        self.tasks = {}
        self.Wheel = Wheel()
    
    def load_task(self):
        reload(tasks)
        for taskname in tasks.runtasks:
            if taskname not in self.tasks:
                try:
                    self.tasks[taskname] = tasks.runtasks[taskname]
                    module = __import__(taskname)
                    self.Wheel.add_task(module, taskname, **tasks.runtasks[taskname])
                except:
                    errmsg = self.get_error_message()
                    self.logger.error(errmsg)
                time.sleep(3)
            else:
                if self.tasks[taskname] != tasks.runtasks[taskname]:
                    try:
                        self.Wheel.update_time(taskname, **tasks.runtasks[taskname])
                    except:
                        errmsg = self.get_error_message()
                        self.logger.error(errmsg)
    
    def run(self):
        self.load_task()
        self.Wheel.start()
        time.sleep(10)
        while 1:
            try:
                self.load_task()
            except:
                errmsg = self.get_error_message()
                self.logger.error(errmsg)
            time.sleep(10)
        
if __name__ == "__main__":
    TS = TaskManager()
    TS.run()
    
