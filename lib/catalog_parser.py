#coding:utf-8
import re
import lxml.html
import tornado.gen
from database.models import Chapter
from service.tieba import TiebaService

class CatalogParser:
    
    def __init__(self, novel, pn):
        
        self.novel = novel
        self.pn = pn
        self.tieba_service = TiebaService()
    
    @tornado.gen.coroutine
    def execute(self):
        '执行解析'

        self.html = yield self._get_html()
        if not self.html:
            raise Exception('GET HTML PAGE ERROR|%s|%s' %(self.novel.id, self.novel.name))
        chapter_list = self._parse_html()
        raise tornado.gen.Return(chapter_list)
    
    @tornado.gen.coroutine
    def get_total_count(self):
        '获取帖子总数'

        self.html = yield self._get_html()
        doc = lxml.html.fromstring(self.html)
        div = doc.find_class('th_footer_l')[0]
        count = int(div.text_content().split(u'共有精品数', 1)[1][:-1])
        raise tornado.gen.Return(count)
    
    @tornado.gen.coroutine
    def _get_html(self):
        '获取html内容'

        request = self.tieba_service.get_catalog_page(self.novel.name, self.pn)
        response = yield TiebaService.async_fetch(request)
        raise tornado.gen.Return(response)
    
    def _parse_html(self):
        '解析html, 返回chapter对象列表'

        doc = lxml.html.fromstring(self.html)
        elements = doc.find_class('j_th_tit')
        elements = filter(lambda x: x.tag == 'a', elements)
        rule = re.compile(self.novel.rule)
        elements = filter(lambda x: rule.match(x.text), elements)
        chapter_list = []
        for ele in elements:
            pageid = ele.iterlinks().next()[2].strip('/p/')
            title = ele.text
            chapter_list.append(Chapter(novel=self.novel.id, title=title, pageid=pageid))
        return chapter_list
