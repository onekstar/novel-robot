#coding:utf-8
NOVEL, CHAPTER = range(2)
APIS = [
    {
        'url': r'/novel',
        'name': u'添加小说',
        'params': [
            {'name': '_method', 'required': True, 'default': u'add', 'exam': 'add','desc': u'method', },
            {'name': 'name', 'required': True, 'default': u'', 'exam': '择天记', 'desc': u'小说名称', },
            {'name': 'rule', 'required': True, 'default': u'', 'exam': '^【择天记】.+第.+章.+$', 'desc': u'章节标题规则', },
        ],
        'desc': u'添加小说',
        'memo': u'',
        'method': 'POST',
        'type': NOVEL,
    },
    {
        'url': r'/novel',
        'name': u'修改小说',
        'params': [
            {'name': '_method', 'required': True, 'default': u'update', 'exam': 'update','desc': u'method', },
            {'name': 'id', 'required': True, 'default': u'', 'exam': '1', 'desc': u'小说id', },
            {'name': 'status', 'required': False, 'default': u'', 'exam': '', 'desc': u'章节标题规则', },
            {'name': 'rule', 'required': False, 'default': u'', 'exam': '', 'desc': u'小说状态', },
        ],
        'desc': u'修改小说',
        'memo': u'',
        'method': 'POST',
        'type': NOVEL,
    },
    {
        'url': r'/chapter',
        'name': u'获取单个章节',
        'params': [
            {'name': '_method', 'required': True, 'default': u'get', 'exam': 'get','desc': u'method', },
            {'name': 'id', 'required': True, 'default': u'', 'exam': '1', 'desc': u'章节id', },
        ],
        'desc': u'获取单个章节',
        'memo': u'',
        'method': 'POST',
        'type': CHAPTER,
    },
]
