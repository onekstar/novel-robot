#coding:utf-8
import lxml.html
import tornado.gen
from database.models import Chapter
from service.tieba import TiebaService
import constant

class ChapterParser:
    '章节解析器'

    def __init__(self, pageid):
        
        self.pageid = pageid 
        self.tieba_service = TiebaService()

    @tornado.gen.coroutine
    def execute(self):
        '解析'
        
        self.html = yield self._get_html()
        chapter = self._parse_html()
        raise tornado.gen.Return(chapter)
    
    @tornado.gen.coroutine
    def _get_html(self):
        '获取html'

        request = self.tieba_service.get_text_page(self.pageid)
        response = yield TiebaService.async_fetch(request)
        raise tornado.gen.Return(response)
    
    def _parse_html(self):
        '解析html'

        doc = lxml.html.fromstring(self.html)
        divs = doc.find_class(constant.TIEBA_CHAPTER_CLASS)
        if len(divs) > 1:
            divs = filter(lambda x: len(x.text_content()) > 500, divs)
        divs = [lxml.html.tostring(div, encoding='utf-8').decode('utf-8') for div in divs]
        return Chapter(content=''.join([div[div.find('>') + 1:-6].strip() for div in divs]))
