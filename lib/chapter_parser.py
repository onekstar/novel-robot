#coding:utf-8
import time
import lxml.html
import tornado.gen
from database.models import Chapter
from service.tieba import TiebaService
import constant

class ChapterParser:
    '章节解析器'

    def __init__(self, chapter):
        
        self.chapter = chapter 
        self.tieba_service = TiebaService()

    @tornado.gen.coroutine
    def execute(self):
        '解析'
        
        self.html = yield self._get_html()
        self.chapter.content = self._parse_html()
        self.chapter.status = Chapter.HAS_SYNC_STATUS
        self.chapter.updatetime = int(time.time())
        raise tornado.gen.Return(1)
    
    @tornado.gen.coroutine
    def _get_html(self):
        '获取html'

        request = self.tieba_service.get_text_page(self.chapter.pageid)
        response = yield TiebaService.async_fetch(request)
        raise tornado.gen.Return(response)
    
    def _parse_html(self):
        '解析html'

        doc = lxml.html.fromstring(self.html)
        divs = doc.find_class(constant.TIEBA_CHAPTER_CLASS)
        if len(divs) > 1:
            divs = filter(lambda x: len(x.text_content()) > 500, divs)
        divs = [lxml.html.tostring(div, encoding='utf-8').decode('utf-8') for div in divs]
        content = ''.join([div[div.find('>') + 1:-6].strip() for div in divs])
        return content
