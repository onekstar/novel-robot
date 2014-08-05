#coding:utf-8
import time
import logging
from base import BaseHandler
from django.db import transaction
from database.models import Novel 

logger = logging.getLogger('Robot.Novel')

class NovelHandler(BaseHandler):
    '小说'
    
    SUPPORTED_METHODS = ['ADD']

    @transaction.commit_manually
    def add(self):
        '添加小说'
        
        name = self.get_argument('name')
        if Novel.objects.filter(name=name).exists():
            return self.finish({'result': 1, 'msg': u'已经创建'})
        try:
            Novel.objects.create(**{
                'id': self.gen_uuid(),
                'name': name,
                'create': int(time.time()),
                'status': 0
            })
        except:
            import traceback
            traceback.print_exc()
            logger.error('ADD NOVEL ERROR', exc_info=1)
            transaction.rollback()
            return self.finish({'result': -1, 'msg': u'novel 添加失败'})
        else:
            transaction.commit()
            return self.finish({'result': 0, 'msg': u''})
