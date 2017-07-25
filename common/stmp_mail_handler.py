#coding=utf8
'''
Created on 2017-6-8

@author: xuwei

@summary: 
'''
import os
import time
import hashlib
import threading
import smtplib  
from email.header import Header  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from timer.logger import Logger
from setting import SMTP_SERVER,SMTP_USER,SMTP_NAME,SMTP_PWD,MAIL_INTERVAL


class SendMailHandler(Logger):
    def __init__(self):
        Logger.__init__(self)
        self.check_lock = threading.Lock()
        self.server = SMTP_SERVER
        self.sender = SMTP_USER
        self.sender_name = SMTP_NAME
        self.sender_pwd = SMTP_PWD
        self.interval = MAIL_INTERVAL
    
    def init_server(self):
        self.smtp = smtplib.SMTP()
        self.smtp.connect(self.server)
        self.smtp.login(self.sender,self.sender_pwd)  
    
    def get_mail(self):
        mail = MIMEMultipart()
        mail['From'] = ("%s<%s>") % (Header(self.sender_name,'utf-8'),self.sender)
        return mail
    
    def send_mail(self,mail,mail_to):
        maxTry = 50
        for i in range(maxTry):
            try:
                self.smtp.sendmail(mail['From'],mail_to,mail.as_string())
                break
            except:
                time.sleep(1)
                self.init_server()
                if i == maxTry - 1:
                    raise Exception('Try send mail failed,(%d times)'%maxTry)
    
    def get_hash_code(self,message):
        md5 = hashlib.md5()
        md5.update(message)
        return md5.hexdigest()
    
    def check_history(self,message):
        send_flag = True
        self.check_lock.acquire()
        try:
            nowtime = time.time()
            historys = []
            md5 = self.get_hash_code(message)
            mailfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'mail.rcd')
            if os.path.exists(mailfile):
                fp = open(mailfile,'rb')
                historys = map(lambda x:x.strip(),fp)
                fp.close()
            del_index = 0
            for index,data in enumerate(historys):
                old_md5,sendtime = data.split(',')
                if nowtime - int(sendtime) > MAIL_INTERVAL:
                    del_index = index + 1
                if md5 == old_md5 and nowtime - int(sendtime) <= MAIL_INTERVAL:
                    send_flag = False
            historys = historys[del_index:]
            if send_flag:
                historys.append(md5 + ',' + str(int(nowtime)))
            with open(mailfile,'wb') as fp:
                fp.write('\r\n'.join(historys))
        except:
            errmsg = self.get_error_message()
            self.logger.error(errmsg)
        finally:
            self.check_lock.release()
        return send_flag
            
    def __call__(self,subject,message,mail_to):
        if not self.check_history(message):
            # print "It is scarcely time for resend."
            return
        mail = self.get_mail()
        if isinstance(mail_to, list):
            mail_to = ','.join(mail_to)
        mail['To'] = mail_to
        mail['Subject'] = Header(subject,'utf-8') 
        message = MIMEText(message,'plain','utf-8')
        mail.attach(message)
        self.send_mail(mail, mail_to)

SendMail = SendMailHandler()
      
if __name__ == "__main__":
    SendMail('晚上加班','今天晚上加班啊','644501662@qq.com')    
