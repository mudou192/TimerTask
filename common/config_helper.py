#coding=utf8
'''
Created on 2017-6-6

@author: xuwei

@summary: 
'''
import os
from ConfigParser import ConfigParser
from setting import CONFIG_FILE
    
class DefaultConfig(object):
    def __init__(self):
        self.config = ConfigParser()
        path  = os.path.dirname(__file__)
        path = os.path.dirname(path)
        self.file_name = os.path.join(path, CONFIG_FILE)
        self.config.read(self.file_name)
    
    def get(self,section,option):
        ret = self.config.get(section, option)
        return ret
    
    def set(self,section,option,value):
        self.config.set(section, option,value)
        self.config.write(open(self.file_name,"w"))
    
    def getOptions(self,section):
        options = self.config.options(section)
        return options
    
class PrivateConfig(DefaultConfig):
    def __init__(self,cnf_file):
        self.file_name = cnf_file
        self.config = ConfigParser()
        self.config.read(self.file_name)
    
    def get(self,section,option):
        ret = self.config.get(section, option)
        return ret
    
    def set(self,section,option,value):
        self.config.set(section, option,value)
        self.config.write(open(self.file_name,"w"))
    
    def getOptions(self,section):
        options = self.config.options(section)
        return options
    
    
