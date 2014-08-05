#coding:utf-8
from test.base import BaseTestCase 

class NovelHandlerTestCase(BaseTestCase):
    'novel 接口测试用例'

    def test_add(self):
        '测试add方法'

        params = {'name': '择天记', '_method': 'add'}
        result = self.common_json_request('/novel', params=params, method='POST')
        self.assertEqual(result['result'], 0)

if __name__ == '__main__': 
    import unittest
    unittest.main()
