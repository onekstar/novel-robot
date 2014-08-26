#coding:utf-8
import constant
import unittest
import os
import re
import importlib

def gen_suite():
    
    name_r = re.compile('^test_.*\.py$')
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader.loadTestsFromModule
    dirs = ('test_handler', 'test_lib')
    for dir in dirs:
        path = os.path.join(constant.PROJECT_DIR, 'test', dir)
        files = os.listdir(path)
        files = filter(name_r.search, os.listdir(path))
        file_names = map(lambda x: os.path.splitext(x)[0], files)
        for file_name in file_names:
            module = importlib.import_module('test.%s.%s' %(dir, file_name))
            suite.addTest(loader(module))
    return suite

if __name__ == '__main__':
    
    suite = gen_suite()
    unittest.TextTestRunner().run(suite)
