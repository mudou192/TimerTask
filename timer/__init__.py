#coding=utf8
'''
Created on 2017-5-17

@author: xuwei

@summary: 轮询调度任务
'''
import re
import os
import time
import platform
import threading

class Wheel(object):
    def __init__(self, call_timeout = None):
        # 超时警告回调方法
        self.call_timeout = call_timeout
        self.tasks = {}
        
    def add_task(self, module, taskname, **kwargs):
        Obj = getattr(module,'TaskServer')
        Task = Obj()
        Task.taskname = taskname
        Task.init_logger()
        Task.init_timer(kwargs)
        if self.tasks:
            maxid = max(self.tasks)
        else:
            maxid = -1
        self.tasks[maxid + 1] = Task
        
    def update_time(self, taskname, **kwargs):
        for tasknum in self.tasks:
            Task = self.tasks.get(tasknum)
            if Task.taskname == taskname:
                Task.init_timer(kwargs)
        
    def del_task(self, taskname):
        pass
    
    def warn_timeout(self, taskname):
        if self.warn_call:
            self.call_timeout('Timeout Warning: %s run timeout'%taskname) 
        
    def run(self):
        while 1:
            for task_id in self.tasks:
                nowtime = time.time()
                Task = self.tasks[task_id]
                if Task.stop or Task.runtime > nowtime:
                    continue
                if Task.running and nowtime - Task.starttime > Task.timeout and Task.timeout != 0:
                    self.warn_timeout(Task.taskname)
                    continue
                if not Task.running and nowtime > Task.runtime:
                    Task.start()
            time.sleep(0.1)
    
    def view_task(self):
        if 'win' in platform.system().lower():
            os.system('cls')
        else:
            os.system('clear')
        print "=" * 100
        print " TaskId" + ' ' * 2 + 'Running' + ' ' * 6 + 'Stop' + ' ' * 10 + 'Start time' + ' ' * 15 + 'Task name'
        print '-' * 100
        for task_id in self.tasks:
            Task = self.tasks[task_id]
            taskname = Task.taskname
            stop = Task.stop
            running = Task.running
            starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Task.starttime))
            print "- %3s %8s %12s %23s          %s"%(str(task_id),str(running),str(stop),
                                          starttime,
                                          str(taskname))
        print "=" * 100
        
    def start_task(self, taskid):
        if taskid not in self.tasks:
            print 'Please enter the correct task ID.'
        else:
            # reload task object
            obj = self.tasks.get(taskid)
            (taskname, interval, date, week, hour, minute, timeout) = (obj.taskname, obj.interval, obj.date, 
                                                                       obj.week, obj.hour, obj.minute, obj.timeout)
            module = __import__(taskname)
            reload(module)
            module.reload_modules()
            Obj = getattr(module, 'TaskServer')
            Task = Obj()
            (Task.taskname, Task.interval, Task.date, Task.week, 
             Task.hour, Task.minute, Task.timeout) = (taskname, interval, date, week, hour, minute, timeout)
            Task.init_logger()
            Task.cal_last_run_time()
            self.tasks[taskid] = Task
            
    def stop_task(self, taskid):
        if taskid not in self.tasks:
            print 'Please enter the correct task ID.'
        else:
            obj = self.tasks.get(taskid)
            obj.stop = True
    
    def command(self):
        cmd = raw_input('Command: [view] view task    [start taskid] start task    [stop taskid] stop task\n')
        cmd = cmd.strip().lower()
        while 1:
            if re.findall('start\s+(\d+)',cmd):
                taskid = re.findall('start\s+(\d+)',cmd)[0]
                self.start_task(int(taskid))
            elif re.findall('stop\s+(\d+)',cmd):
                taskid = re.findall('stop\s+(\d+)',cmd)[0]
                self.stop_task(int(taskid))
            elif cmd == 'view':
                self.view_task()
            cmd = raw_input('Command: [view] view task    [start taskid] start task    [stop taskid] stop task\n')
    
    def start(self):
        task_thread = threading.Thread(target=self.command)
        task_thread.setDaemon(True)
        task_thread.start()
        task_thread = threading.Thread(target=self.run)
        task_thread.setDaemon(True)
        task_thread.start()
