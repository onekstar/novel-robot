#coding:utf-8
import time
import tornado.gen
from django.db import transaction
from database.models  import Chapter
from base import BaseHandler
from lib.chapter_parser import ChapterParser

class ChapterHandler(BaseHandler):
    
    @tornado.gen.coroutine
    @transaction.commit_on_success
    def get(self):
        '获取chapter信息, 如果content为空则主动获取'

        query_set = Chapter.objects.filter(id=self.get_argument('id')) 
        try:
            self.chapter = query_set.get()
        except:
            self.finish({'code': 1, 'msg': u'获取章节错误'})
            return
        yield self._parse_chapter_if_need()
        self.finish({'code': 0, 'data': query_set.values()[0]})
    
    @tornado.gen.coroutine
    def _parse_chapter_if_need(self):
        '解析chapter如果需要'

        if self.chapter.content:
            return
        parser = ChapterParser(self.chapter)
        yield parser.execute()
        self.chapter.save()
