#coding:utf-8
import time
import logging
import tornado.gen
import tornado.ioloop
from database.models import Novel, Chapter
import constant
from tornado.ioloop import IOLoop
from lib.catalog_parser import CatalogParser
from django.db import transaction
from lib import base_util

io_loop = IOLoop.instance()

logger = logging.getLogger('Robot.SyncNovelTimer')

class SyncNovelTimer:
    '小说同步定时器'

    @tornado.gen.coroutine
    def start(self):
        '开启'

        self.query_set = Novel.objects.filter(status__in=Novel.WAITING_SYNC_STATUS)
        while True:
            Novel.objects.filter(status=Novel.ON_SYNC_STATUS, updatetime__lt=int(time.time())-constant.NOVEL_SYNC_TIMEOUT).update(status=Novel.SERIAL_STATUS) #重启超时的更新
            self.novel = self.query_set.filter(updatetime__lt=int(time.time())-constant.NOVEL_SYNC_INTERVAL).order_by('updatetime', 'createtime').first()
            if self.novel is None:
                yield tornado.gen.Task(io_loop.add_timeout, int(time.time()) + constant.NOVEL_SYNC_TIMER_INTERVAL)
                continue
            try:
                self._change_novel_status(Novel.ON_SYNC_STATUS)
                yield self._sync_novel()
            except Exception as e:
                self._change_novel_status(Novel.SERIAL_STATUS)
                logger.error('sync novel error %s|%s|' %(self.novel.id, self.novel.name), exc_info=1)
    
    def _change_novel_status(self, status):
        '修改novel状态'

        self.novel.status = status
        self.novel.save()
    
    @transaction.commit_on_success
    @tornado.gen.coroutine
    def _sync_novel(self):
        '同步novel'

        logger.info('start sync novel %s|%s' %(self.novel.id, self.novel.name))
        self.pageids = set(Chapter.objects.filter(novel=self.novel.id).values_list('pageid', flat=True))
        parser = CatalogParser(self.novel, 0)
        total_count = yield parser.get_total_count()
        offset = 0
        while True:
            if offset > total_count:
                break
            parser = CatalogParser(self.novel, offset)
            chapter_list = yield parser.execute()
            self._save_chapters(chapter_list)
            offset += 50
        self.novel.updatetime = int(time.time())
        self.novel.status = Novel.SERIAL_STATUS
        self.novel.save()
        logger.info('start sync novel %s|%s' %(self.novel.id, self.novel.name))
    
    def _save_chapters(self, chapter_list):
        '保存chapter'

        finished = False
        for chapter in chapter_list:
            if int(chapter.pageid) in self.pageids:
                continue 
            self.pageids.add(chapter.pageid)
            chapter.id = base_util.genid()
            chapter.createtime = int(time.time() * 1000)
            chapter.status = Chapter.UN_SYNC_STATUS 
            chapter.save()
