# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from django.contrib.auth.models import User
from accounts.models import Wallet, UserInfo
from freebtc123.models import Nav, Classify, Site, Evaluate, Like, Favorite, Visit, Log
from baiduchengjiu.models import Scores

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from django.db.models import Q
from django.db.models import Count

from django.utils import simplejson
from django.core import serializers
from django.utils.encoding import smart_str
from django.forms.models import model_to_dict

import re
import sys
import json
import time
import random
import hashlib
import requests

from utils.utils import getNav, getRef, getSiteid, getErrorCode, usercheck, pwd2hash, get_referer_view, delCookie


TIME_OUT = 8


def getScoreGrade(u):
    re = requests.get('http://www.baidu.com/p/'+u+'?from=ur', timeout=TIME_OUT)
    _img = re.text.split('class=portrait-img src=\\x22')[1].split('?')[0].replace('\\', '')
    uDataUrl = re.text.split('urprincessindex')[1].split("');")[0]
    re = requests.get('http://www.baidu.com/ur/show/urprincessindex' + uDataUrl, timeout=TIME_OUT)
    _grade = re.text.split('{"curLevel":+"')[1].split('"')[0]
    _score = re.text.split('"curSco":+"')[1].split('"')[0]
    return _img, int(_score), int(_grade)


@shared_task
def _add(_uid):
    try:
        _img, _score, _grade = getScoreGrade(_uid)
        s = Scores(uid=_uid, img=_img, score=_score, grade=_grade)
    except:
        s = Scores(uid=_uid)
    s.save(using='baiduchengjiu')


@shared_task
def _update(_uid):
    print '>> test'
    try:
        _img, _score, _grade = getScoreGrade(_uid)
        s = Scores.objects.using('baiduchengjiu').get(uid=_uid)
        s.score = _score
        s.grade = _grade
        s.save()
    except:
        print sys.exc_info()[1]
