#coding:utf-8
import time
import logging
import tornado.gen
import tornado.ioloop
import server
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
            self.novel = self.query_set.order_by('updatetime', 'createtime').first()
            if self.novel is None:
                continue
            try:
                self._change_novel_status(Novel.ON_SYNC_STATUS)
                yield self._sync_novel()
            except Exception as e:
                self._change_novel_status(Novel.SERIAL_STATUS)
                logger.error('sync novel error %s|%s|' %(self.novel.id, self.novel.name), exc_info=1)
            yield tornado.gen.Task(io_loop.add_timeout, int(time.time()) + constant.NOVEL_SYNC_INTERVAL)
    
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
            finished = self._save_chapters(chapter_list)
            if finished:
                break
            offset += 50
        self.novel.updatetime = int(time.time())
        self.novel.status = Novel.SERIAL_STATUS
        self.novel.save()
        logger.info('start sync novel %s|%s' %(self.novel.id, self.novel.name))
    
    def _save_chapters(self, chapter_list):
        '保存chapter'

        finished = False
        for chapter in chapter_list:
            if chapter.pageid in self.pageids:
                finished = True 
                break
            chapter.id = base_util.genid()
            chapter.createtime = int(time.time())
            chapter.status = Chapter.UN_SYNC_STATUS 
            chapter.save()
        return finished

if __name__ == '__main__':
    
    server.logger = logging.getLogger('Robot')
    stream_hd = logging.StreamHandler()
    stream_hd.setFormatter(server.log_format)
    server.logger.addHandler(stream_hd)
    server.logger.setLevel(logging.INFO)

    timer = SyncNovelTimer()
    timer.start()
    io_loop.start()
