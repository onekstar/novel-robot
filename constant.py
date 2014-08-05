#coding:utf-8
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) # 项目路径（绝对地址）
#Django Settings
DEBUG = False 
TEMPLATE_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'novel',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
INSTALLED_APPS = (
    'database'
)
TIME_ZONE = 'Asia/Shanghai'
SECRET_KEY = ')_2!e1a%ut21294=z^-hh#js7nou3i0q8&8llk0r)loj%menf&'
#Django Settings end


LOCAL_LOG_DIR = '/opt/logs/tornado/tudou' # 本地日志路径
LOCAL_LOG_FLUSH_INTERVAL = 3 # 本地日志写入间隔（秒)
COOKIE_SECRET = 'xl*0./*(_+()#@M<'

#尝试导入本地配置
try:
    from local_constant import *
except:
    pass
