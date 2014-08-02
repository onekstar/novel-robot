#coding:utf-8
import os
import datetime
import logging
import tornado.ioloop
logger = logging.getLogger('TudouTV.LocalLog')

class LocalLog(tornado.ioloop.PeriodicCallback):

    cache = []
    
    def __init__(self, callback_time, log_dir, port):
        self.log_dir = log_dir
        self.port = port
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        super(LocalLog, self).__init__(self.dump, callback_time)

    def dump(self):
        '把cache中的内容写入文件'

        cls = self.__class__
        if not cls.cache:
            return
        filename = os.path.join(self.log_dir, '%s.log' % (self.port))
        with open(filename, 'a') as f:
            try:
                f.writelines(cls.cache)
            except:
                print '++-LOG-++', cls.cache
                cls.cache = []
        cls.cache = []


    @classmethod
    def write(cls, s):
        '为logging提供的接口'

        cls.cache.append(s)
