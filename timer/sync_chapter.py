#coding:utf-8
import time
import logging
import tornado.gen
from tornado.ioloop import IOLoop
from django.db import transaction
from database.models import Novel, Chapter
from lib.chapter_parser import ChapterParser
import constant

io_loop = IOLoop.instance()
logger = logging.getLogger('Robot.SyncChapterTimer')

class SyncChapterTimer:
    
    @tornado.gen.coroutine
    def start(self):
        '开启'

        self.query_set = Chapter.objects.filter(status__in=Chapter.WAITING_SYNC_STATUS)
        while True:
            self.chapter = self.query_set.order_by('createtime', 'updatetime').first()
            if self.chapter is None:
                yield tornado.gen.Task(io_loop.add_timeout, int(time.time()) + constant.CHAPTER_SYNC_INTERVAL)
                continue
            try:
                self._change_chapter_status(Chapter.ON_SYNC_STATUS)
                yield self._sync_chapter()
            except Exception as e:
                self._change_chapter_status(Chapter.UN_SYNC_STATUS)
                logger.error('sync novel error %s|' %(self.chapter.id), exc_info=1)
    
    def _change_chapter_status(self, status):
        '更新chapter status字段'

        self.chapter.status = status
        self.chapter.save()
    
    @transaction.commit_on_success
    @tornado.gen.coroutine
    def _sync_chapter(self):
        '更新chapter'

        parser =  ChapterParser(self.chapter)
        yield parser.execute() 
        self.chapter.save()
