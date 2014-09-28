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
        params = {'id': chapter.id, '_method': 'get'}
        result = self.common_json_request('/chapter', params=params)
        self.assertEqual(result['code'], 0)
    
    def test_get_list_when_no_limit_and_offset(self):
        '测试get_list方法,当没有limit和offset'

        novel_id = 'aa'
        for i in range(10):
            self.add_chapter(novel_id, u'测试章节%s' %i, pageid=i)
        params = {'novel': novel_id, '_method': 'get_list'}
        result = self.common_json_request('/chapter', params=params)
        self.assertEqual(result['code'], 0)
        self.assertTrue(result['data'])

    def test_get_list_when_there_is_limit_and_offset(self):
        '测试get_list方法'

        novel_id = 'aa'
        for i in range(10):
            self.add_chapter(novel_id, u'测试章节%s' %i, pageid=i)
        limit, offset = 2, 5 
        params = {'novel': novel_id, '_method': 'get_list', 'limit': 2, 'offset': offset}
        result = self.common_json_request('/chapter', params=params)
        self.assertEqual(result['code'], 0)
        self.assertTrue(result['data'])
    
    def test_get_list_when_offset_out_of_max(self):
        '测试get_list方法，当offset超出最大范围'

        limit, offset = 2, 5 
        params = {'novel': 'aa', '_method': 'get_list', 'limit': 2, 'offset': offset}
        result = self.common_json_request('/chapter', params=params)
        self.assertEqual(result['code'], 0)
        self.assertFalse(result['data'])

if __name__ == '__main__':
    import unittest
    unittest.main()
