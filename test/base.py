#coding:utf-8
import constant
import os, sys
sys.path.insert(0, constant.PROJECT_DIR)
import tornado.web
from tornado.testing import AsyncHTTPTestCase
import server
from urllib import urlencode
from tornado.escape import utf8
from tornado.httpclient import HTTPRequest as TornadoHTTPRequest
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.escape import json_decode
import tornado.ioloop
from service.base import HTTPRequest
from lib import base_util
import copy
import tornado.gen
import urllib

class BaseTestCase(AsyncHTTPTestCase):
    '测试基类'
    
    def setUp(self):
        
        AsyncHTTPTestCase.setUp(self)
    
    def get_app(self):

        return server.Application()
    
    def get_new_ioloop(self):
        
        return tornado.ioloop.IOLoop.instance()
    
    def get_http_client(self):
        
        return SimpleAsyncHTTPClient(self.io_loop)
    
    def common_internal_request(self, path, params={}, body=None, headers={}, method='GET', timeout=10):
        '通用的内部接口请求'
        
        _params = copy.deepcopy(params)
        _headers = copy.deepcopy(headers)
        url = '%s?%s' %(self.get_url(path), urllib.urlencode({'pid': 'testcase', 'guid': 'test'}))
        request = HTTPRequest(url, params=_params, headers=_headers, body=body, method=method, request_timeout=timeout)
        self.http_client.fetch(request, self.stop)
        response = self.wait(timeout=timeout)
        return response
    
    def common_json_request(self, path, params={}, body=None, headers={}, method='GET', timeout=10):
        'response为json的请求'
        
        response = self.common_internal_request(path, params=params, body=body, headers=headers, method=method, timeout=timeout)
        self.assertEqual(response.code, 200)
        return json_decode(response.body)

    def pprint(self, data):
        base_util.pprint(data)
