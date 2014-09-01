#coding:utf-8
import tornado.testing
from test.base import BaseTestCase
from database.models import Chapter
from lib.chapter_parser import ChapterParser

class ChapterParserTestCase(BaseTestCase):
    '章节解析测试用例'

    @tornado.testing.gen_test
    def test_execute(self):
        '测试execute方法'

        chapter = Chapter(pageid='3255459308')
        parser = ChapterParser(chapter)
        yield parser.execute()
        self.assertTrue(chapter.content.startswith(u'第一百二十三章 燎原'))
    
    @tornado.testing.gen_test
    def test_execute_when_only_one_div(self):
        '测试execute方法，当页面只搜索到一个div'

        chapter = Chapter(pageid='3253316379')
        parser = ChapterParser(chapter)
        yield parser.execute()
        self.assertTrue(chapter.content.index(u'石昊是从一座巨城离开的'))

if __name__ == '__main__':
    import unittest
    unittest.main()
