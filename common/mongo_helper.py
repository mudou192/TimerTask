#coding=utf8
'''
Created on 2017-6-8

@author: xuwei

@summary: 
'''
import traceback
import bson
import pymongo

class MongoAccess:
    def __init__(self,hosts,user,pwd,db,replicaSet,IS_PRIMARY = False):
        self.conn = None
        self.hosts = hosts
        self.user = user
        self.pwd = pwd
        self.db_name = db
        self.replicaSet = replicaSet
        self.IS_PRIMARY = IS_PRIMARY
        self.init_mongo()
        
    def init_mongo(self):
        tryMax = 100
        for i in  range(tryMax):
            try:
                self.conn = pymongo.MongoClient(self.hosts,replicaSet = self.replicaSet)
                if self.IS_PRIMARY:
                    read_preference = pymongo.ReadPreference.PRIMARY_PREFERRED
                else:
                    read_preference = pymongo.ReadPreference.SECONDARY_PREFERRED
                self.DB = self.conn.get_database(self.db_name,read_preference = read_preference)
                self.DB.authenticate(self.user,self.pwd)
                break
            except:
                traceback.print_exc()
                if i == tryMax - 1:
                    raise Exception('Try connect mongodb filed.(%s %d times)'%(self.hosts,str(tryMax)))
            
    def get_objectid( self, mongoId = None ):
        moduleObj = None
        if pymongo.__dict__.has_key("objectid"):
            moduleObj = getattr(pymongo,'objectid')
        elif bson.__dict__.has_key("objectid"):
            moduleObj = getattr(bson,'objectid')
        classObj = getattr(moduleObj,"ObjectId")
        return classObj( mongoId )     
    
    def __del__(self):
        if self.conn:
            self.conn.close() 
