#coding:utf-8
from base import BaseService, HTTPRequest

class TiebaService(BaseService):
    '贴吧'

    HOST = 'tieba.baidu.com'

    def get_catalog_page(self, name, pn):
        '获取目录页面'

        url = self.get_url('/f/good') 
        params = {
            'kw': name,
            'tab': 'good',
            'pn': pn 
        }
        return HTTPRequest(url, params=params, response_type='HTML', response_charset='gb18030')
    
    def get_text_page(self, pageid):
        '获取正文页面'

        url = self.get_url('/p/%s' %pageid)
        params = {
            'see_lz': 1
        }
        return HTTPRequest(url, params=params, response_type='HTML', response_charset='gb18030')

if __name__ == '__main__':
    srv = TiebaService()
    req = srv.get_catalog_page(u'择天记', 0)
   #req = srv.get_text_page(3255459308)
    res = srv.sync_fetch(req)
    print res
