#coding:utf-8
import json

def pprint(data):
    
    print json.dumps(data, encoding='utf-8', ensure_ascii=False, indent=4) 
