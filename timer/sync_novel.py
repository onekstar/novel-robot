#coding:utf-8
import tornado.gen
import tornado.ioloop
from database.models import Novel, Chapter
import constant

class SyncNovelTimer:
    '小说同步定时器'

    @tornado.gen.coroutine
    def start():
        '开启'

        query_set = Novel.objects.select_for_update().filter(status__in=[Novel.INIT_STATUS, Novel.SERIAL_STATUS], updatetime__lt = int(time.time()) - constant.SYNC_INTERVAL_TIME)[:1]
