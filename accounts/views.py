# Create your views here.
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from accounts.models import Wallet, UserInfo
from freebtc123.models import Nav, Classify, Site, Evaluate, Like, Favorite, Visit, Log

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
import json
import time
import random
import hashlib

from utils.utils import getNav, getRef, getSiteid, getErrorCode, usercheck, pwd2hash, get_referer_view, delCookie


def login(request):
    if request.method == 'GET':
        reDict = {'nav': getNav(request)}
        response = render_to_response('accounts/login.html', reDict)
        ref = get_referer_view(request)
        response.set_cookie('ref', smart_str(ref))
        return response
    else:
        _usr = request.POST.get('usr', '')
        _pwd = request.POST.get('pwd', '')
        userInfoList = UserInfo.objects.filter(username=_usr)
        if userInfoList.count() == 0:
            reDict = {'nav': getNav(request), 'notexists': True}
            return render_to_response('accounts/login.html', reDict)
        else:
            if userInfoList[0].password == pwd2hash(_pwd):
                referer = getRef(request)
                _kwargs = {'siteid': getSiteid(request)} if u'freebtc123:evaluate' == referer else {}
                response = HttpResponseRedirect(reverse(referer, kwargs=_kwargs))
                delCookie(request, response, 'ref')
                response.set_cookie('usr', smart_str(_usr))
                return response
            else:
                reDict = {'nav': getNav(request), 'notexists': False, 'pwderror': True}
                return render_to_response('accounts/login.html', reDict)


def signup(request):
    if request.method == 'GET':
        reDict = {'nav': getNav(request)}
        response = render_to_response('accounts/signup.html', reDict)
        ref = get_referer_view(request)
        response.set_cookie('ref', smart_str(ref))
        return response
    else:
        _usr = request.POST.get('usr', '')
        _pwd = request.POST.get('pwd', '')
        _email = request.POST.get('email', '')
        _wallet = request.POST.get('wallet', '')
        if UserInfo.objects.filter(username=_usr).count() != 0:
            reDict = {'nav': getNav(request), 'exists': True}
            return render_to_response('accounts/signup.html', reDict)
        else:
            w = Wallet.objects.create(walletUrl=_wallet)
            u = UserInfo.objects.create(username=_usr, password=pwd2hash(_pwd), email=_email, wallet=w)
            referer = getRef(request)
            _kwargs = {'siteid': getSiteid(request)} if u'freebtc123:evaluate' == referer else {}
            response = HttpResponseRedirect(reverse(getRef(request), kwargs=_kwargs))
            delCookie(request, response, 'ref')
            response.set_cookie('usr', smart_str(_usr))
            return response


def logout(request):
    referer = get_referer_view(request)
    _kwargs = {'siteid': getSiteid(request)} if u'freebtc123:evaluate' == referer else {}
    response = HttpResponseRedirect(reverse(referer, kwargs=_kwargs))
    delCookie(request, response, 'usr')
    return response
