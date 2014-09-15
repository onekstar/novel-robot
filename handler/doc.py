#coding:utf-8
from tornado.web import RequestHandler
from docs.api_define import APIS

class DocHandler(RequestHandler):
    'api文档'

    def get(self):
        '获取api文档'

        api_type = self.get_argument('type', '')
        apis = APIS
        if api_type:
            apis = filter(lambda x: str(x.get('type')) == api_type, apis) 
        self.render('doc.html', apis=apis, type=api_type)


