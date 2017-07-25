#coding=utf8
'''
Created on 2017-6-6

@author: xuwei

@summary: 
'''
import MySQLdb
import traceback

class MySQLAccess:
    def __init__(self,host,user,pwd,db,charset="utf8"):
        self.conn = None
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.charset = charset
        self.init_sql()
        
    def init_sql(self):
        tryMax = 100
        for i in range(tryMax):
            try:
                self.conn = MySQLdb.connect(host = self.host, user = self.user, passwd = self.pwd, db = self.db, charset=self.charset)
                break
            except:
                traceback.print_exc()
                if i == tryMax - 1:
                    raise Exception('Try connect mysql filed.(%s %d times)'%(self.host, str(tryMax)))
    
    def select(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            self.conn.commit()
            return data
        except MySQLdb.OperationalError:
            self.init_sql()
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except Exception,error:
            cursor.close()
            raise Exception(str(error) +"\n"+str(sql))
    
    def execute(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            return True
        except MySQLdb.OperationalError:
            self.init_sql()
            cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception,error:
            self.conn.rollback()
            raise Exception(str(error) +"\n"+str(sql))
    
    def execute_many(self,sql,data):
        cursor = self.conn.cursor()
        try:
            cursor.executemany(sql,data)
            self.conn.commit()
            return True
        except MySQLdb.OperationalError:
            self.init_sql()
            cursor.executemany(sql,data)
            self.conn.commit()
            return True
        except Exception,error:
            self.conn.rollback()
            raise Exception(str(error) +"\n"+str(sql))
        
    def __del__(self):
        if self.conn:
            self.conn.close()
