# Create your views here.
# -*- coding: utf-8 -*-

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


def getpnsl(p, maxp):
    '''
        @function: get prev, next, showlist
        @paras:
            √ p - current page
            √ maxp - max page
        @returns: (prev, next, showlist) tuple
    '''
    prev = p-1 if maxp != 1 and p != 1 else -1
    next = p+1 if maxp != 1 and p != maxp else -1
    if p-2 >= 1 and p+3 <= maxp+1:
        start = p-2
        end = p+3
    elif p-2 < 1:
        start = 1
        end = 6 if 6 <= maxp+1 else maxp+1
    elif p+3 > maxp+1:
        start = maxp-4 if maxp-4>1 else 1
        end = maxp+1
    showlist = range(start, end)
    return prev, next, showlist


def addRank(scores, _from):
    data = []
    for s in scores:
        temp = model_to_dict(s)
        temp['rank'] = _from
        data.append(temp)
        _from += 1
    return data


def scores(request, p=1):
    _p = int(p)
    _from = (_p-1)*100
    _to = _p*100
    _maxp = (Scores.objects.using('baiduchengjiu').all().count() + 100 - 1) / 100
    prev, next, showlist = getpnsl(_p, _maxp)
    scores = Scores.objects.using('baiduchengjiu').filter().order_by('-score')[_from: _to]
    reDict = {'nav': getNav(request), 'scores': addRank(scores, _from+1), 'prev': prev, 'cur': _p, 'next': next, 'showlist': showlist}
    return render_to_response('baiduchengjiu/scores.html', reDict)


def getScoreGrade(u):
    re = requests.get('http://www.baidu.com/p/'+u+'?from=ur')
    _img = re.text.split('class=portrait-img src=\\x22')[1].split('?')[0].replace('\\', '')
    uDataUrl = re.text.split('urprincessindex')[1].split("');")[0]
    re = requests.get('http://www.baidu.com/ur/show/urprincessindex' + uDataUrl)
    _grade = re.text.split('{"curLevel":+"')[1].split('"')[0]
    _score = re.text.split('"curSco":+"')[1].split('"')[0]
    return _img, int(_score), int(_grade)


def cjadmin(request):
    reDict = {'nav': getNav(request)}
    if request.method == 'GET':
        pass
    else:
        _uid = request.POST.get('usr', '')
        if 1 == Scores.objects.using('baiduchengjiu').filter(uid=_uid).count():
            reDict['exists'] = True
        else:
            try:
                _img, _score, _grade = getScoreGrade(_uid)
                s = Scores(uid=_uid, img=_img, score=_score, grade=_grade)
            except:
                s = Scores(uid=_uid)
            s.save(using='baiduchengjiu')
    return render_to_response('baiduchengjiu/cjadmin.html', reDict)


def getrank(request):
    _bdname = request.POST.get('bdname', '')
    try:
        uinfo = model_to_dict(Scores.objects.using('baiduchengjiu').get(uid=_bdname))
        rank = Scores.objects.using('baiduchengjiu').filter(score__gt=uinfo['score']).count() + 1
        return HttpResponse(json.dumps({'code': '200', 'msg': uinfo, 'rank': rank}))
    except:
        info=sys.exc_info()
        #print info[0],":",info[1]
        return HttpResponse(json.dumps({'code': '404', 'msg': str(info[1])}))