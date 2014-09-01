#coding:utf-8
import tornado.testing
from test.base import BaseTestCase
from database.models import Novel, Chapter
from lib import base_util
from timer.sync_novel import SyncNovelTimer

class SyncNovelTimerTestCase(BaseTestCase):
    '小说同步定时器测试用例'

    @tornado.testing.gen_test(timeout=300)
    def test_sync_novel(self):
        '测试_sync_novel方法'

        timer = SyncNovelTimer()
        timer.novel = Novel(id=base_util.genid(), name=u'择天记', rule=ur'^【择天记】.+第.+章.+$', status=0)
        yield timer._sync_novel()
        self.assertTrue(Chapter.objects.filter(novel=timer.novel.id).exists()) #章节入库
        db_novel = Novel.objects.get(id=timer.novel.id)
        self.assertEqual(db_novel.status, Novel.SERIAL_STATUS) #状态回置
    
    @tornado.testing.gen_test(timeout=30)
    def test_sync_novel_when_chapter_exist(self):
        '测试_sync_novel, 当已有章节'

        timer = SyncNovelTimer()
        timer.novel = Novel(id=base_util.genid(), name=u'择天记', rule=ur'^【择天记】.+第.+章.+$', status=0)
        chapter = Chapter(id=base_util.genid(), novel=timer.novel.id, title=u'【择天记】第一卷 第一百三十三章 林海听涛（上）', pageid='3266502456')
        chapter.save()
        yield timer._sync_novel()
        self.assertTrue(Chapter.objects.filter(novel=timer.novel.id).exists()) #章节入库
        db_novel = Novel.objects.get(id=timer.novel.id)
        self.assertEqual(db_novel.status, Novel.SERIAL_STATUS) #状态回置

if __name__ == '__main__':
    import unittest
    unittest.main()
