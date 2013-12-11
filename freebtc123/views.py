# Create your views here.
# -*- coding: utf-8 -*-

###
# ErrorCode: 100***, for userCheck
#     {'errorCode': 100200, 'errorString': 'User not exists, you can use it to register'}
#     {'errorCode': 100201, 'errorString': 'User already exists, pls change a username to register'}
# ErrorCode: 200***, for likeSite
#     {'errorCode': 200200, 'errorString': 'Like/Unlike the site success'}
#     {'errorCode': 200201, 'errorString': 'You have already like/unlike the site, don\'t hesitate'}
# ErrorCode: 300***, for Favorite
#     {'errorCode': 300200, 'errorString': 'Favorite the site success'}
#     {'errorCode': 300201, 'errorString': 'The parm of siteid not transmitted success'}
# ErrorCode: 400***, for
# ErrorCode: 500***, for
###

from django.contrib.auth.models import User
from freebtc123.models import Wallet, UserInfo, Nav, Classify, Site, Evaluate, Like, Favorite, Visit

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

import json
import time
import random
import hashlib


def getUsr(request):
    '''
        @function: get usr from cookies, and if not exists, set usr None
        @paras:
        @returns: usr string
    '''
    return request.COOKIES['usr'] if 'usr' in request.COOKIES else None


def getIP(request):
    '''
        @function: get current ip for the desktop which visit from
        @paras:
        @returns: ip string
    '''
    return request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']


def getUsrHost(request):
    '''
        @function: get usr and ip together
        @paras:
        @returns: (usr, ip) tuple
    '''
    return getUsr(request), getIP(request)


def getLikeFlag(request, siteid, _flag):
    '''
        @function: get the flag of whether usr and ip liked the site, and usr first
        @paras:
            siteid - the site.pk, unique identification the site
            _flag - Like:True, Unlike:False
        @returns: True or False boolean
    '''
    if 'usr' in request.COOKIES:
        return Like.objects.filter(user__username=request.COOKIES['usr'], flag=_flag, site__id=siteid).count() != 0
    else:
        return Like.objects.filter(host=getIP(request), flag=_flag, site__id=siteid).count() != 0


def getFavFlag(request, siteid):
    '''
        @function: get the flag of whether usr and ip favorite the, and usr first
        @paras:
            sited - the site.pk, unique identification the table
        @returns: True or False boolean
    '''
    if 'usr' in request.COOKIES:
        return Favorite.objects.filter(user__username=request.COOKIES['usr'], site__id=siteid).count() != 0
    else:
        return Favorite.objects.filter(host=getIP(request), site__id=siteid).count() != 0


def getCsySite(request, _nav):
    '''
        @function: get site list for different classify in a certain nav
        @paras:
            _nav - the certain nav for which to get csy site
        @returns: csysite dict
    '''
    csySetList = Classify.objects.filter(nav__navName=_nav).order_by('csyPosition')
    csysite = []
    for csySet in csySetList:
        csyDict = model_to_dict(csySet)
        siteSetList = csySet.site_set.filter()
        site = []
        for siteSet in siteSetList:
            siteDict = model_to_dict(siteSet)
            siteDict['like'] = getLikeFlag(request, siteSet.id, True)
            siteDict['unlike'] = getLikeFlag(request, siteSet.id, False)
            siteDict['fav'] = getFavFlag(request, siteSet.id)
            site.append(siteDict)
        csyDict['siteSet'] = site
        csysite.append(csyDict)
    return csysite


def getNav(request):
    '''
        @function: get all nav from table Nav
        @paras:
        @returns: nav dict query set
    '''
    return Nav.objects.all().order_by('navPosition')


def getFavSite(request):
    _usr, _host = getUsrHost(request)
    favSetList = Favorite.objects.filter(user__username=_usr) if 'usr' in request.COOKIES else Favorite.objects.filter(host=_host)
    favsite = []
    for siteSet in favSetList:
        siteDict = model_to_dict(siteSet.site)
        siteDict['like'] = getLikeFlag(request, siteSet.site_id, True)
        siteDict['unlike'] = getLikeFlag(request, siteSet.site_id, False)
        siteDict['fav'] = getFavFlag(request, siteSet.site_id)
        favsite.append(siteDict)
    return favsite


def fav(request):
    reDict = {'nav': getNav(request), 'favsite': getFavSite(request), 'usr': getUsr(request)}
    return render_to_response('freebtc123/fav.html', reDict)


def freebtc(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'freebtc'), 'usr': getUsr(request)}
    return render_to_response('freebtc123/freebtc.html', reDict)


def altcoin(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'altcoin'), 'usr': getUsr(request)}
    return render_to_response('freebtc123/altcoin.html', reDict)


def btcforum(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'btcforum'), 'usr': getUsr(request)}
    return render_to_response('freebtc123/btcforum.html', reDict)


def btcwiki(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'btcwiki'), 'usr': getUsr(request)}
    return render_to_response('freebtc123/btcwiki.html', reDict)


def submitsite(request):
    _name = request.POST.get('name', '')
    _description = request.POST.get('description', '')
    _url = request.POST.get('url', '')
    if _url == '':
        print 'error'
    else:
        csySet = Classify.objects.get(nav__navName='submitsite')
        Site.objects.create(siteName=_name, siteDescription=_description, siteUrl=_url, classify_id=csySet.id)
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'altcoin'), 'usr': getUsr(request)}
    return render_to_response('freebtc123/submitsite.html', reDict)


def visit(request, siteid):
    _usr, _host = getUsrHost(request)
    try:
        u = UserInfo.objects.get(username=_usr)
        Visit.objects.create(site_id=siteid, user=u, host=_host)
    except:
        Visit.objects.create(site_id=siteid, host=_host)
    s = Site.objects.get(id=siteid)
    s.siteClickNum = s.siteClickNum + 1
    s.save()
    return HttpResponseRedirect(s.siteUrl)


def evaluate(request, siteid):
    _content = request.POST.get('content', '')
    if _content == '':
        print 'error'
    else:
        s = Site.objects.get(id=siteid)
        s.siteEvaluateNum = s.siteEvaluateNum + 1
        s.save()
        Evaluate.objects.create(site_id=siteid, evaContent=_content)
    eva = Evaluate.objects.filter(site__id=siteid).order_by('-evaDateTime')
    reDict = {'nav': getNav(request), 'siteid': siteid, 'eva': eva}
    return render_to_response('freebtc123/evaluate.html', reDict)


def like(request):
    _flag = 'false' != request.POST.get('flag', '')
    _siteid = request.POST.get('siteid', '')
    _usr, _host = getUsrHost(request)
    try:
        u = UserInfo.objects.get(username=_usr)
        try:
            Like.objects.get(site_id=_siteid, user=u, flag=not _flag)
            errorCode = {'errorCode': 200201, 'errorString': 'You have already like/unlike the site, don\'t hesitate'}
            return HttpResponse(json.dumps(errorCode))
        except:
            Like.objects.create(site_id=_siteid, user=u, host=_host, flag=_flag)
    except:
        try:
            Like.objects.get(site_id=_siteid, host=_host, flag=not _flag)
            errorCode = {'errorCode': 200201, 'errorString': 'You have already like/unlike the site, don\'t hesitate'}
            return HttpResponse(json.dumps(errorCode))
        except:
            Like.objects.create(site_id=_siteid, host=_host, flag=_flag)
    s = Site.objects.get(id=_siteid)
    s.siteLikeNum = s.siteLikeNum + 1 if _flag else s.siteUnlikeNum + 1
    s.save()
    errorCode = {'errorCode': 200200, 'errorString': 'Like/Unlike the site success'}
    return HttpResponse(json.dumps(errorCode))


def favorite(request):
    _siteid = request.POST.get('siteid', '')
    if _siteid:
        _usr, _host = getUsrHost(request)
        u = UserInfo.objects.filter(username=_usr)
        if u.count() == 1:
            Favorite.objects.create(site_id=_siteid, user=u[0], host=_host)
        else:
            Favorite.objects.create(site_id=_siteid, host=_host)
        s = Site.objects.get(id=_siteid)
        s.siteFavNum = s.siteFavNum + 1
        s.save()
        errorCode = {'errorCode': 300200, 'errorString': 'Favorite the site success'}
        return HttpResponse(json.dumps(errorCode))
    else:
        errorCode = {'errorCode': 300201, 'errorString': 'The parm of siteid not transmitted success'}
        return HttpResponse(json.dumps(errorCode))


def pwd2hash(pwd):
    '''
        @function: change pwd 2 hash by use hashlib's md5 method
        @paras:
        @returns: hexdigest string
    '''
    hashpwd = hashlib.md5()
    hashpwd.update(pwd)
    return hashpwd.hexdigest()


def login(request):
    if request.method == 'GET':
        reDict = {'nav': getNav(request)}
        return render_to_response('freebtc123/login.html', reDict)
    else:
        _usr = request.POST.get('usr', '')
        _pwd = request.POST.get('pwd', '')
        userInfoList = UserInfo.objects.filter(username=_usr)
        if userInfoList.count() == 0:
            return render_to_response('freebtc123/login.html', {'notexists': True})
        else:
            if userInfoList[0].password == pwd2hash(_pwd):
                response = HttpResponseRedirect(reverse('freebtc123:fav'))
                response.set_cookie('usr', smart_str(_usr))
                return response
            else:
                print {'exists': True, 'pwderror': True}
                return render_to_response('freebtc123/login.html', {'notexists': False, 'pwderror': True})


def signup(request):
    if request.method == 'GET':
        reDict = {'nav': getNav(request)}
        return render_to_response('freebtc123/signup.html', reDict)
    else:
        _usr = request.POST.get('usr', '')
        _pwd = request.POST.get('pwd', '')
        _email = request.POST.get('email', '')
        _wallet = request.POST.get('wallet', '')
        if UserInfo.objects.filter(username=_usr).count() != 0:
            return render_to_response('freebtc123/signup.html', {'exists': True})
        else:
            w = Wallet.objects.create(walletUrl=_wallet)
            u = UserInfo.objects.create(username=_usr, password=pwd2hash(_pwd), email=_email, wallet=w)
            response = HttpResponseRedirect(reverse('freebtc123:fav'))
            response.set_cookie('usr', smart_str(_usr))
            return response


def logout(request):
    response = HttpResponseRedirect(reverse('freebtc123:fav'))
    if 'usr' in request.COOKIES:
        response.delete_cookie('usr')
    return response


def usercheck(request):
    '''
        @function: check whether user has already been registered
        @paras:
        @returns: errorCode json string
    '''
    _usr = request.POST.get('usr', '')
    if UserInfo.objects.filter(username=_usr).count() == 0:
        errorCode = {'errorCode': 100200, 'errorString': 'User not exists, you can use it to register'}
        return HttpResponse(json.dumps(errorCode))
    else:
        errorCode = {'errorCode': 100201, 'errorString': 'User already exists, pls change a username to register'}
        return HttpResponse(json.dumps(errorCode))
