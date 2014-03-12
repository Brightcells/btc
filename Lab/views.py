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


def getScores(request):
    scoreSetList = Game2048.objects.all()[:20]
    # sometimes same, deal with
    for scoreSet in scoreSetList:
        pass
    return scoreSetList


def game_2048(request):
    reDict = {'scores': getScores(request)}
    return render_to_response('Lab/game-2048.html', reDict)


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
