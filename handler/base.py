#coding:utf-8
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, HTTPError
import uuid
import logging
import constant
import functools
from django.db import connections

logger = logging.getLogger('Robot.BaseHandler')

class BaseHandler(RequestHandler):
    'handler基类'
    
    SUPPORTED_METHODS = ['GET', 'POST', 'DELETE', 'UPDATE']

    def finish(self, chunk=None):
        
        commit_db()
        RequestHandler.finish(self, chunk=chunk)
    
    def initialize(self):
        'Hook for subclass initialization'
        
        commit_db()
        self.uuid = self.gen_uuid() 
        self.request.uuid = self.uuid
        self.request.o_method = self.request.method
        method = self.get_argument('_method', None)
        if method is not None:
            self.request.method = str(method.upper())
        RequestHandler.initialize(self)
    
    def gen_uuid(self):
        '生成uuid'

        return uuid.uuid4().hex
    
class TestHandler(BaseHandler):
    
    def get(self):
        
        self.finish({'status': 'success'})

def commit_db():
    
    for c in connections.all():
        try:
            c._commit()
        except:
            pass
