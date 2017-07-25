#coding=utf8
'''
Created on 2017-6-7

@author: xuwei

@summary: 
'''
import os
import time
import logging
import logging.handlers
import cStringIO
import traceback
from setting import LOGGER_LEVEL,LOG_BACKUP_COUNT,LOG_SIZE

class Logger(object):
    def __init__(self):
        self.levels = {'INFO':logging.INFO,'DEBUG':logging.DEBUG,
                       'WARN':logging.WARN,'ERROR':logging.ERROR}
        self.logger = None
        self.taskname = 'manager'
        self.init_logger()
    
    def get_log_file(self):
        project_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
        logs_path = os.path.join(project_path,'tasklogs')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        return os.path.join(logs_path,self.taskname + '.log')
    
    def init_logger(self):
        logfile = self.get_log_file()
        self.logger = logging.getLogger(self.taskname)
        # fh = logging.FileHandler(logfile)
        # logging.handlers.RotatingFileHandler inherits logging.FileHandler
        fh = logging.handlers.RotatingFileHandler(logfile,maxBytes = LOG_SIZE, 
                                                  backupCount = LOG_BACKUP_COUNT)
        # ch = logging.StreamHandler()
        formater = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s:\n%(message)s', 
                                     "%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formater)  
        # ch.setFormatter(formater)
        self.logger.addHandler(fh)
        # self.logger.addHandler(ch)
        self.logger.setLevel(self.levels[LOGGER_LEVEL.strip().upper()])
        
    def get_error_message(self):
        f = cStringIO.StringIO()
        traceback.print_exc( file = f )
        f.seek( 0 )
        errmsg = f.read()
        print errmsg
        return errmsg
    
    def recode_task_start(self):
        project_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
        recodes_path = os.path.join(project_path,'taskrecodes')
        if not os.path.exists(recodes_path):
            os.mkdir(recodes_path)
        filename = os.path.join(recodes_path,self.taskname + '.log')
        with open(filename,'ab') as fp:
            fp.write(time.strftime("[%Y-%m-%d %H:%M:%S]: " + self.taskname + ' start.') + '\r\n')
    
    def recode_task_end(self):
        project_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
        recodes_path = os.path.join(project_path,'taskrecodes')
        if not os.path.exists(recodes_path):
            os.mkdir(recodes_path)
        filename = os.path.join(recodes_path,self.taskname + '.log')
        with open(filename,'ab') as fp:
            fp.write(time.strftime("[%Y-%m-%d %H:%M:%S]: " + self.taskname + ' end.') + '\r\n')

if __name__ == "__main__":
    L = Logger()
    L.logger.error('Hello World!')
    
