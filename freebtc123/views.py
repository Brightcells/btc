# Create your views here.
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from accounts.models import Wallet, UserInfo
from freebtc123.models import Nav, Classify, Site, Evaluate, Proof, Like, Favorite, Visit, Log

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

from utils.utils import getNav, getUsr, getIP, getUsrHost, getErrorCode


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


def getCsySite(request, _nav, _rank):
    '''
        @function: get site list for different classify in a certain nav
        @paras:
            _nav - the certain nav for which to get csy site
            _rank - rank site by desc or asc, 1 for desc, 0 for asc
        @returns: csysite dict
    '''
    csySetList = Classify.objects.filter(nav__navName=_nav).order_by('csyPosition')
    csysite = []
    for csySet in csySetList:
        csyDict = model_to_dict(csySet)
        siteSetList = csySet.site_set.filter().order_by('-siteDateTime') if 1 == _rank else csySet.site_set.filter()
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


def getLastestSite(request):
    return Site.objects.all().order_by('-siteDateTime')[:8]


def fav(request):
    reDict = {'nav': getNav(request), 'favsite': getFavSite(request), 'lastest': getLastestSite(request), 'usr': getUsr(request)}
    return render_to_response('freebtc123/fav.html', reDict)


def getNumSite(request, num):
    qs = Site.objects.all().filter(classify__nav__navName='freebtc').exclude(classify__in=[36, 30, 27, 6, 5])
    try:
        return qs[num], num+1
    except:
        return qs[0], 1


def getCsyNumSite(request, num, csyid):
    qs = Site.objects.all().filter(classify_id=csyid)
    try:
        return qs[num], num+1
    except:
        return qs[0], 1


def next(request, num, csyid=-1):
    numsite, num = getNumSite(request, int(num)) if -1 == csyid else getCsyNumSite(request, int(num), int(csyid))
    reDict = {'nav': getNav(request), 'csyid': csyid, 'numsite': numsite, 'num': num, 'usr': getUsr(request)}
    reHtml = 'freebtc123/btcreaper.html' if -1 == csyid else 'freebtc123/csyreaper.html'
    return render_to_response(reHtml, reDict)


def btcreaper(request, csyid=-1):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'freebtc', 0), 'csyid': csyid, 'numsite': -1, 'num': 0, 'usr': getUsr(request)}
    reHtml = 'freebtc123/btcreaper.html' if -1 == csyid else 'freebtc123/csyreaper.html'
    return render_to_response(reHtml, reDict)


def freebtc(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'freebtc', 0), 'usr': getUsr(request)}
    return render_to_response('freebtc123/freebtc.html', reDict)


def altcoin(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'altcoin', 0), 'usr': getUsr(request)}
    return render_to_response('freebtc123/altcoin.html', reDict)


def btcforum(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'btcforum', 0), 'usr': getUsr(request)}
    return render_to_response('freebtc123/btcforum.html', reDict)


def btcwiki(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'btcwiki', 1), 'usr': getUsr(request)}
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
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'submitsite', 1), 'usr': getUsr(request)}
    return render_to_response('freebtc123/submitsite.html', reDict)


def visit(request):
    _siteid = request.POST.get('siteid', '')
    _usr, _host = getUsrHost(request)
    try:
        u = UserInfo.objects.get(username=_usr)
        Visit.objects.create(site_id=_siteid, user=u, host=_host)
    except:
        Visit.objects.create(site_id=_siteid, host=_host)
    s = Site.objects.get(id=_siteid)
    s.siteClickNum = s.siteClickNum + 1
    s.save()
    return HttpResponse(json.dumps(getErrorCode('record_visit_success')))


def getEvaluateDict(request, siteid):
    site = Site.objects.get(id=siteid)
    siteDict = model_to_dict(site)
    siteDict['like'] = getLikeFlag(request, siteid, True)
    siteDict['unlike'] = getLikeFlag(request, siteid, False)
    siteDict['fav'] = getFavFlag(request, siteid)
    eva = Evaluate.objects.filter(site__id=siteid).order_by('-evaDateTime')
    proof = Proof.objects.filter(site__id=siteid).order_by('-proofDateTime')
    reDict = {'nav': getNav(request), 'siteid': siteid, 'site': siteDict, 'eva': eva, 'proof': proof}
    return reDict


def evaluate(request, siteid):
    _content = request.POST.get('content', '')
    if _content == '':
        print 'Just get Evaluates!!!'
    else:
        s = Site.objects.get(id=siteid)
        s.siteEvaluateNum = s.siteEvaluateNum + 1
        s.save()
        Evaluate.objects.create(site_id=siteid, evaContent=_content)
    return render_to_response('freebtc123/evaluate.html', getEvaluateDict(request, siteid))


def proof(request, siteid):
    _proof = request.POST.get('proof', '')
    if _proof == '':
        print 'Just get Proofs!!!'
    else:
        Proof.objects.create(site_id=siteid, proofContent=_proof)
    return render_to_response('freebtc123/evaluate.html', getEvaluateDict(request, siteid))


def siteLikeChange(_siteid, _flag, _num):
    s = Site.objects.get(id=_siteid)
    s.siteLikeNum = s.siteLikeNum + _num if _flag else s.siteUnlikeNum + _num
    s.save()


def like(request):
    _flag = 'false' != request.POST.get('flag', '')
    _siteid = request.POST.get('siteid', '')
    _usr, _host = getUsrHost(request)
    try:
        u = UserInfo.objects.get(username=_usr)
        try:
            Like.objects.get(site_id=_siteid, user=u, flag=not _flag)
            return HttpResponse(json.dumps(getErrorCode('already_like_unlike')))
        except:
            try:
                Like.objects.get(site_id=_siteid, user=u, flag=_flag).delete()
                siteLikeChange(_siteid, _flag, -1)
                Log.objects.create(site_id=_siteid, user=u, host=_host, descr="Cancel like/unlike")
                return HttpResponse(json.dumps(getErrorCode('cancel_like_unlike_success')))
            except:
                Like.objects.create(site_id=_siteid, user=u, host=_host, flag=_flag)
                Log.objects.create(site_id=_siteid, user=u, host=_host, descr="Insert like/unlike")
    except:
        try:
            Like.objects.get(site_id=_siteid, host=_host, flag=not _flag)
            return HttpResponse(json.dumps(getErrorCode('already_like_unlike')))
        except:
            try:
                Like.objects.get(site_id=_siteid, host=_host, flag=_flag).delete()
                siteLikeChange(_siteid, _flag, -1)
                Log.objects.create(site_id=_siteid, host=_host, descr="Cancel like/unlike")
                return HttpResponse(json.dumps(getErrorCode('cancel_like_unlike_success')))
            except:
                Like.objects.create(site_id=_siteid, host=_host, flag=_flag)
                Log.objects.create(site_id=_siteid, host=_host, descr="Insert like/unlike")
    siteLikeChange(_siteid, _flag, 1)
    return HttpResponse(json.dumps(getErrorCode('like_unlike_success')))


def siteFavChange(_siteid, _num):
    s = Site.objects.get(id=_siteid)
    s.siteFavNum = s.siteFavNum + _num
    s.save()


def favorite(request):
    _siteid = request.POST.get('siteid', '')
    if _siteid:
        _usr, _host = getUsrHost(request)
        u = UserInfo.objects.filter(username=_usr)
        if u.count() == 1:
            try:
                Favorite.objects.get(site_id=_siteid, user=u[0], host=_host).delete()
                siteFavChange(_siteid, -1)
                Log.objects.create(site_id=_siteid, user=u[0], host=_host, descr="Cancel Favorite")
                return HttpResponse(json.dumps(getErrorCode('cancel_favorite_success')))
            except:
                Favorite.objects.create(site_id=_siteid, user=u[0], host=_host)
                Log.objects.create(site_id=_siteid, user=u[0], host=_host, descr="Inset Favorite")
        else:
            try:
                Favorite.objects.get(site_id=_siteid, host=_host).delete()
                siteFavChange(_siteid, -1)
                Log.objects.create(site_id=_siteid, host=_host, descr="Cancel Favorite")
                return HttpResponse(json.dumps(getErrorCode('cancel_favorite_success')))
            except:
                Favorite.objects.create(site_id=_siteid, host=_host)
                Log.objects.create(site_id=_siteid, host=_host, descr="Insert Favorite")
        siteFavChange(_siteid, 1)
        return HttpResponse(json.dumps(getErrorCode('favorite_site_success')))
    else:
        return HttpResponse(json.dumps(getErrorCode('site_id_not_exists')))


def login(request):
    return HttpResponseRedirect(reverse('accounts:login'))


def signup(request):
    return HttpResponseRedirect(reverse('accounts:signup'))


def logout(request):
    return HttpResponseRedirect(reverse('accounts:logout'))
