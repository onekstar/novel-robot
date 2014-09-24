#coding:utf-8
from test.base import BaseTestCase

class ChapterHandlerTestCase(BaseTestCase):
    '/chapter接口测试用例'

    def test_get_when_chapter_not_exist(self):
        '测试get当chapter不存在'
        
        params = {'id': 'xx'}
        result = self.common_json_request('/chapter', params=params)
        self.assertEqual(result['code'], 1)
    
    def test_get_when_chapter_exist(self):
        '测试get当chapter存在'

        chapter = self.add_chapter('aa', u'测试', '3255459308')
        params = {'id': chapter.id}
        result = self.common_json_request('/chapter', params=params)
        self.assertEqual(result['code'], 0)

if __name__ == '__main__':
    import unittest
    unittest.main()
