#coding=utf8
'''
Created on 2017-6-7

@author: xuwei

@summary: system settings
'''
# Default config path
CONFIG_FILE = "setting.cnf"

# Log levels, sizes, and backup count
LOGGER_LEVEL = 'debug'
LOG_SIZE = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 5

# smtp mail server
SMTP_SERVER = 'smtp.163.com'
SMTP_USER = 'xxxxx@163.com'
SMTP_NAME = '接口任务'
SMTP_PWD = ''
# same mail interval(s)
MAIL_INTERVAL = 1800

# monitor info database
MYSQL_HOST = ''
MYSQL_USER = ''
MYSQL_PWD = ''
MYSQL_DB = ''
