#coding:utf-8
import os

DEBUG = False
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) # 项目路径（绝对地址）
LOCAL_LOG_DIR = '/opt/logs/tornado/tudou' # 本地日志路径
LOCAL_LOG_FLUSH_INTERVAL = 3 # 本地日志写入间隔（秒)
COOKIE_SECRET = 'xl*0./*(_+()#@M<'

#尝试导入本地配置
try:
    from local_constant import *
except:
    pass
