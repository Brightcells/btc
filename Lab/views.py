# Create your views here.
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from accounts.models import Wallet, UserInfo
from freebtc123.models import Nav, Classify, Site, Evaluate, Proof, Like, Favorite, Visit, Log
from Lab.models import Game2048

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
from django.utils import timezone

import re
import sys
import json
import time
import random
import hashlib
import requests

from utils.utils import *


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


def getScores(request):
    scoreSetList = Game2048.objects.all().order_by('-create_time')[:10]
    # sometimes same, deal with
    scores = []
    for scoreSet in scoreSetList:
        scoreDict = model_to_dict(scoreSet)
        hl = scoreDict['host'].split('.')
        if scoreSet.user:
            scoreDict['usr'] = scoreSet.user.username
        scoreDict['host'] = '%s.***.***.%s' %(hl[0], hl[-1])
        scoreDict['create_time'] = scoreSet.create_time
        scores.append(scoreDict)
    return scores


def getBestScore(request):
    _usr, _host = getUsrHost(request)
    uiSet = UserInfo.objects.filter(username=_usr)
    try:
        if uiSet.count():
            return Game2048.objects.filter(user=ui[0]).order_by('-score').values('score')[0]['score']
        else:
            return Game2048.objects.filter(host=_host).order_by('-score').values('score')[0]['score']
    except:
        return 0


def home(request):
    return render_to_response('Lab/lab.html')


def game_2048(request):
    reDict = {'usr': getUsr(request), 'scores': getScores(request), 'best': getBestScore(request)}
    return render_to_response('Lab/game-2048/game-2048.html', reDict)


def game_2048_left(request):
    reDict = {'usr': getUsr(request), 'scores': getScores(request), 'best': getBestScore(request)}
    return render_to_response('Lab/game-2048/game-2048-left.html', reDict)


def game_2048_right(request):
    reDict = {'usr': getUsr(request), 'scores': getScores(request), 'best': getBestScore(request)}
    return render_to_response('Lab/game-2048/game-2048-right.html', reDict)


def game_2048_pk(request):
    return render_to_response('Lab/game-2048/game-2048-pk.html')


def addRank(scores, _from):
    data = []
    for s in scores:
        temp = model_to_dict(s)
        temp['rank'] = _from
        hl = temp['host'].split('.')
        if s.user:
            temp['user'] = s.user.username
        temp['host'] = '%s.***.***.%s' %(hl[0], hl[-1])
        temp['create_time'] = s.create_time
        data.append(temp)
        _from += 1
    return data


def game_2048_rank(request, p=1):
    _p = int(p)
    _from = (_p-1)*100
    _to = _p*100
    _maxp = (Game2048.objects.all().count() + 100 - 1) / 100
    prev, next, showlist = getpnsl(_p, _maxp)
    scores = Game2048.objects.filter().order_by('-score')[_from: _to]
    reDict = {'nav': getNav(request), 'usr': getUsr(request), 'scores': addRank(scores, _from+1), 'prev': prev, 'cur': _p, 'next': next, 'showlist': showlist}
    return render_to_response('Lab/game-2048/game-2048-rank.html', reDict)


def game_2048_history(request, p=1):
    _p = int(p)
    _from = (_p-1)*100
    _to = _p*100
    _maxp = (Game2048.objects.all().count() + 100 - 1) / 100
    prev, next, showlist = getpnsl(_p, _maxp)
    scores = Game2048.objects.filter().order_by('-create_time')[_from: _to]
    reDict = {'nav': getNav(request), 'usr': getUsr(request), 'scores': addRank(scores, _from+1), 'prev': prev, 'cur': _p, 'next': next, 'showlist': showlist}
    return render_to_response('Lab/game-2048/game-2048-history.html', reDict)


def game_2048_score(request):
    try:
        _flag = request.POST.get('_flag', '')
        _score = request.POST.get('_score', '')
        _usr, _host = getUsrHost(request)
        ui = getUI(_usr)
        try:
            td = timezone.now() - Game2048.objects.filter(user=ui, host=_host, flag=('game-won' == _flag), score=_score).values('create_time')[0]['create_time']
            if int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6) < 3:
                pass
            else:
                g = Game2048.objects.create(user=ui, host=_host, flag=('game-won' == _flag), score=_score)
        except:
                g = Game2048.objects.create(user=ui, host=_host, flag=('game-won' == _flag), score=_score)
        return HttpResponse(json.dumps({'code': '200', 'msg': 'Record score success!'}))
    except:
        info = sys.exc_info()
        return HttpResponse(json.dumps({'code': '201', 'msg': str(info[1])}))
