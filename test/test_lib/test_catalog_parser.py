#coding:utf-8
#coding:utf-8
import tornado.testing
from test.base import BaseTestCase
from database.models import Novel 
from lib.catalog_parser import CatalogParser
import re

class CatalogParserTestCase(BaseTestCase):
    '目录解析测试用例'

    @tornado.testing.gen_test
    def test_execute(self):
        '测试execute方法'

        
        novel_list = [Novel(id='aaa', name=u'择天记', rule=ur'^【择天记】.+第.+章.+$'), Novel(id='bbb', name=u'完美世界小说', rule=ur'^完美世界 第.+章[^(山寨）)]+$')]
        for novel in novel_list:
            parser = CatalogParser(novel, 0) 
            c_list = yield parser.execute()
            self.assertTrue(c_list)
            rule = re.compile(novel.rule)
            for c in c_list:
                print c.title
                self.assertTrue(c.pageid)
                self.assertTrue(rule.match(c.title))
    
if __name__ == '__main__':
    import unittest
    unittest.main()
