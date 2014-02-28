#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   ##  Copyright (c) 2014 - huangqimin <huangqimin@baidu.com>

   ##  This is used to fetch use's score of baiduchengjiu and fill into sqlite db named baiduchengjiu!!!
   ##
"""


import os
import sqlite3
import requests


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_PATH = os.path.join(PROJECT_DIR, 'baiduchengjiu.db3')


def getScoreGrade(u):
    re = requests.get('http://www.baidu.com/p/'+u+'?from=ur')
    _img = re.text.split('class=portrait-img src=\\x22')[1].split('?')[0].replace('\\', '')
    uDataUrl = re.text.split('urprincessindex')[1].split("');")[0]
    re = requests.get('http://www.baidu.com/ur/show/urprincessindex' + uDataUrl)
    _grade = re.text.split('{"curLevel":+"')[1].split('"')[0]
    _score = re.text.split('"curSco":+"')[1].split('"')[0]
    return _img, int(_score), int(_grade)


def _connect():
    """
       ##  连接数据库、设置游标
    """
    cx = sqlite3.connect(SQLITE_PATH)   # Connect SQLite Database File
    #print cx
    #cx.text_factory = str
    cur = cx.cursor()   # Set a youbiao
    #print cur
    return cx, cur


def _close(cx, cur):
    """
       ##  将更新写进数据库， 关闭数据库连接
    """
    cx.commit()  # 将更新从内存写入文件数据库， http://docs.python.org/release/2.6/library/sqlite3.html， 要学会看文档啊...
    cur.close()
    cx.close()


def _update(num_list):
    cx, cur = _connect()
    for _id in num_list:
        try:
            _uid = cur.execute(iSQL, (_id, )).fetchone()[1]
            _img, _score, _grade = getScoreGrade(_uid)
            print _id, _uid, _score, _grade, _img

            cur.execute('update scores set img=?, score=?, grade=? where uid = ?', (_img, _score, _grade, _uid))
        except:
            pass
    _close(cx, cur)


'''
iSQL = 'create table scores (id integer primary key , uid varchar(255) unique, score integer, grade integer)'
try:
    cur.execute(iSQL)
except:
    pass
'''


iSQL = 'select count(*) from scores'
cx, cur = _connect()
all_user_num = int(cur.execute(iSQL).fetchone()[0])
_close(cx, cur)


iSQL = 'select * from scores where id = ?'
flag = True
num = 0
while flag:
    _from = num*10+1
    _to = (num+1)*10+1
    _update(range(_from, _to))
    num += 1
    if _to >= all_user_num:
        flag = False

'''
cx.text_factory = lambda x: unicode(x, "utf-8", "ignore")
cur.execute("INSERT INTO Events values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?, ?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?, ?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (row_list, u'1340964359740', 1, 1, 0, 1, unicode(CourseInfoList[1],"gbk"), unicode(CourseInfoList[5],"gbk"), None, None, None, 0, 1, int((RemindTimeStamp)*1000), int((RemindTimeStamp+90*60)*1000), u'Asia/Shanghai', None, 0, 0, 0, 1, 0, None, None, None, None, None, None, None, None, int((RemindTimeStamp+90*60)*1000), 1, 0, 1, 1, u'Phone', 0, None, None, None, None, None, None, None, None, None, None, None))
'''
