#coding:utf-8
import copy
import logging
import tornado.httpclient
from urllib import urlencode
from uuid import uuid4
from tornado.escape import json_decode
import tornado.gen
import json
from tornado.escape import utf8
from lib import base_util

logger = logging.getLogger('TudouTV.BaseService')

DEFAULT_HEADER_MAP = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'close',
    'User-Agent': 'Tudou Tv',
}

class HTTPRequest(tornado.httpclient.HTTPRequest):
    
    def __init__(self, url, method='GET', params={}, headers={}, body=None, response_type='JSON', response_charset='utf-8', request_timeout=3, **kwargs):
        '''
        response_type是响应body的类型，为JSON时会主动decode
        设置超时使用request_timeout参数(秒)
        '''

        _params = copy.copy(params)
        _headers = copy.copy(headers)
        self.id = uuid4().hex
        self.response_type = response_type
        self.response_charset = response_charset
        self.handle_headers(method, _headers)
        self.filter_params(_params)
        url = self.gen_url(url, method, _headers, _params)
        body = body or self.gen_body(method, _params, _headers)
        tornado.httpclient.HTTPRequest.__init__(self, url, method=method, headers=_headers, body=body, request_timeout=request_timeout, **kwargs)

    def filter_params(self, params):
        '过滤参数'
        
        for key, value in params.items():
            if value is None or value == '':
                params.pop(key)
                continue
            if type(value) in (int, float):
                params[key] = str(value)
                continue
            params[key] = utf8(value)

    def handle_headers(self, method, headers):
        '处理请求头'

        headers['X-Request-ID'] = self.id
        for key, value in DEFAULT_HEADER_MAP.iteritems():
            if key not in headers:
                headers[key] = value

    def gen_url(self, url, method, headers, params):
        '生成完整的url'

        if method == 'GET' and headers['Content-Type'] == 'application/x-www-form-urlencoded' and params:
            encoded_params = urlencode(params)
            if '?' in url:
                url = '%s&%s' %(url, encoded_params)
            else:
                url = '%s?%s' %(url, encoded_params)
        return url
                
    def gen_body(self, method, params, headers):
        '生成请求body'

        if params and method != 'GET':
            if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                return urlencode(params)
        return None 

    def __str__(self):
        '打印输出'

        return '|'.join((self.id, self.method, self.url, self.body or ''))

class BaseService:
    '第三方服务基类' 

    @classmethod
    def sync_fetch(cls, request):
        '同步请求'

        if not isinstance(request, HTTPRequest):
            return request
        response = tornado.httpclient.HTTPClient().fetch(request)
        body = BaseService.get_response_body(request, response)
        return BaseService.decode_body_if_need(request, body)

    @staticmethod
    def decode_body_if_need(request, body):
        '解码body（如果需要）'

        if request.response_type == 'JSON':
            body = BaseService.safe_json_decode(request, body)
        elif request.response_type == 'HTML':
            body = body.decode(request.response_charset)
        return body 

    @classmethod
    @tornado.gen.coroutine
    def async_fetch(cls, request):
        '异步请求'

        if not isinstance(request, HTTPRequest):
            raise tornado.gen.Return(copy.deepcopy(request))
        response = yield tornado.gen.Task(tornado.httpclient.AsyncHTTPClient().fetch, request)
        body = cls.get_response_body(request, response)
        if not cls.is_expected_response(response):
            logger.warn('RETRY FOR UNEXPECTED RESULT|%s' %(request))
            request.start_time = int(time.time())
            response = yield tornado.gen.Task(tornado.httpclient.AsyncHTTPClient().fetch, request)
            body = cls.get_response_body(request, response)
        body = BaseService.decode_body_if_need(request, body)
        raise tornado.gen.Return(body)
    
    @classmethod
    def is_expected_response(cls, response):
        '是否是预期的响应'

        return response.code < 500

    @classmethod
    def get_response_body(cls, request, response):
        '获取response body, 如果错误则返回空'

        if response.error:
            body = response.body  or ''
            logger.error('RESPONSE ERROR|%s|%s|%s|%s|%s' %(cls.__name__, request, response.request_time, response.error, body[:512]))
        else:
            body = response.body
            logger.info('RESPONSE OK|%s|%s|%s|%s|' %(cls.__name__, request, response.request_time, body[:512]))
        return body

    @staticmethod
    def safe_json_decode(request, data, default={}):
        '捕获异常的json decode'

        try:
            return json_decode(data)
        except:
            logger.error('JSON DECODE ERROR|%s|%s|' %(request, data[:512]), exc_info=1)
            return default 

    def get_url(self, path):
        '获取完整的url(轮询方式取host)'

        cls = self.__class__
        url = 'http://%s%s' %(cls.HOST, path)
        return url

    @staticmethod
    def pprint(response):
        
        base_util.pprint(response) 
