#coding:utf-8
from test.base import BaseTestCase 
from database.models import Novel

class NovelHandlerTestCase(BaseTestCase):
    'novel 接口测试用例'

    def setUp(self):
        
        BaseTestCase.setUp(self)

    def test_add(self):
        '测试add方法'

        params = {'name': '测试', 'rule': u'【择天记】.+', '_method': 'add'}
        result = self.common_json_request('/novel', params=params, method='POST')
        self.assertEqual(result['result'], 0)
    
    def test_add_when_exist(self):
        '测试add方法，当已经存在'

        name = u'测试'
        novel = self.add_novel(name)
        params = {'name': name, '_method': 'add'}
        result = self.common_json_request('/novel', params=params, method='POST')
        self.assertEqual(result['result'], 1)
    
    def test_update_when_not_exist(self):
        '测试update方法，当novel不存在'

        params = {'id': '1', '_method': 'update'}
        result = self.common_json_request('/novel', params=params, method='POST')
        self.assertEqual(result['result'], 1)
    
    def test_update_when_status_param_error(self):
        '测试update方法，当status参数非法'

        novel = self.add_novel(u'测试')
        params = {'id': novel.id, '_method': 'update', 'status': 9999} 
        result = self.common_json_request('/novel', params=params, method='POST')
        self.assertEqual(result['result'], 2)
    
    def test_update(self):
        '测试update方法'

        novel = self.add_novel(u'测试')
        params = {'id': novel.id, '_method': 'update', 'status': Novel.SERIAL_STATUS, 'rule': u'【择天记】.+'} 
        result = self.common_json_request('/novel', params=params, method='POST')
        self.assertEqual(result['result'], 0)

if __name__ == '__main__': 
    import unittest
    unittest.main()
