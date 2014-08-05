#coding:utf-8
from django.db import models


class Novel(models.Model):
    '小说'

    INIT_STATUS = 0
    SERIAL_STATUS = 1
    COMPLETE_STATUS = 2

    id = models.CharField(u'id', max_length=32, primary_key=True) 
    name = models.CharField(u'名称', max_length=255, unique=True) 
    create = models.PositiveIntegerField(u'创建时间', default=0) 
    update = models.PositiveIntegerField(u'更新时间', default=0)
    status = models.SmallIntegerField(u'状态', default=0)

    class Meta(object):
        db_table = 'Novel' 

class Chapter(models.Model):
    '小说章节'

    id = models.CharField(u'id', max_length=32, primary_key=True) 
    title = models.CharField(u'名称', max_length=255, unique=True)
    create = models.PositiveIntegerField(u'创建时间', default=0) 
    update = models.PositiveIntegerField(u'更新时间', default=0)
    status = models.SmallIntegerField(u'状态', default=0)

    class Meta(object):
        db_table = 'Chapter' 
