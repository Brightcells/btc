#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   ##  Copyright (c) 2014 - huangqimin <huangqimin@baidu.com>

   ##  This is used to fill in sqlite db named baiduchengjiu!!!
   ##
"""


import os
import sqlite3
import requests


MAX_PAGE_NUM = 3700
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


for i in xrange(1, MAX_PAGE_NUM):
    rgurl = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=%B0%D9%B6%C8%B3%C9%BE%CD&pn='+str(i)
    print 'RequestGetUrl: ',  rgurl
    re = requests.get(rgurl)
    members = re.text.split('</a><span class="forum_level')[:-1]

    cx, cur = _connect()
    for m in members:
        mem = m.split('>')[-1]
        print 'MemberInfo: ', mem,
        try:
            _img, _score, _grade = getScoreGrade(mem)
            print _score, _grade, _img
            if cur.execute('select count(*) from scores where uid =?', (mem, )).fetchone()[0] > 0:
                print 'ErrorInfo: ', mem, 'has already exists!'
            else:
                cur.execute('insert into scores (uid, img, score, grade) values (?, ?, ?, ?)', (mem, _img, _score, _grade))
        except:
            print 'ErrorInfo: ', 'Insert ', mem, 'Into Table Scores Error'
    _close(cx, cur)
