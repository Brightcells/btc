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

from utils.utils import getNav, getRef, getSiteid, getErrorCode, usercheck, pwd2hash, get_referer_view, delCookie


def scores(request):
    scores = Scores.objects.using('baiduchengjiu').filter().order_by('-score')[:100]
    reDict = {'nav': getNav(request), 'scores': scores}
    return render_to_response('baiduchengjiu/scores.html', reDict)


def cjadmin(request):
    reDict = {'nav': getNav(request)}
    if request.method == 'GET':
        pass
    else:
        _uid = request.POST.get('usr', '')
        if 1 == Scores.objects.using('baiduchengjiu').filter(uid=_uid).count():
            reDict['exists'] = True
        else:
            s = Scores(uid=_uid)
            s.save(using='baiduchengjiu')
    return render_to_response('baiduchengjiu/cjadmin.html', reDict)


def getrank(request):
    _bdname = request.POST.get('bdname', '')
    try:
        uinfo = model_to_dict(Scores.objects.using('baiduchengjiu').get(uid=_bdname))
        rank = Scores.objects.using('baiduchengjiu').filter(score__gt=uinfo['score']).count()
        return HttpResponse(json.dumps({'code': '200', 'msg': uinfo, 'rank': rank}))
    except:
        info=sys.exc_info()
        #print info[0],":",info[1]
        return HttpResponse(json.dumps({'code': '404', 'msg': str(info[1])}))