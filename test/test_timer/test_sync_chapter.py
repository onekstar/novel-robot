#coding:utf-8
import tornado.testing
from test.base import BaseTestCase
from database.models import Novel, Chapter
from lib import base_util
from timer.sync_chapter import SyncChapterTimer 

class SyncChapterTimerTestCase(BaseTestCase):
    '章节同步定时器测试用例'

    @tornado.testing.gen_test(timeout=10)
    def test_sync_chapter(self):
        '测试_sync_chapter方法'

        timer = SyncChapterTimer()
        timer.chapter = Chapter(id=base_util.genid(), novel='xxxx', title=u'【择天记】第一卷 第一百三十三章 林海听涛（上）', pageid='3266502456')
        yield timer._sync_chapter()
        db_chapter = Chapter.objects.get(id=timer.chapter.id)
        self.assertTrue(db_chapter.content)
        self.assertEqual(db_chapter.status, Chapter.HAS_SYNC_STATUS)

if __name__ == '__main__':
    import unittest
    unittest.main()
