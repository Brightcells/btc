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
from django.utils import timezone

import re
import json
import time
import random
import hashlib
import requests

from utils.utils import getNav, getUsr, getIP, getUsrHost, getErrorCode


def getWallet(request):
    '''
        @function: get wallet if user in cookies, and if not exists, set wallet None
        @paras:
        @returns: wallet string
    '''
    if 'usr' in request.COOKIES:
        walletid = model_to_dict(UserInfo.objects.get(username=request.COOKIES['usr']))['wallet']
        wallet = model_to_dict(Wallet.objects.get(id=walletid))['walletUrl']
    else:
        wallet = None
    return wallet


def getLastVisitTime(request, siteid):
    '''
        @function: get the last time of whether usr and ip visit the site, and usr first
        @paras:
            siteid - the site.pk, unique identification the site
        @returns: True or False boolean
    '''
    if 'usr' in request.COOKIES:
        visitSetList = Visit.objects.filter(user__username=request.COOKIES['usr'], site__id=siteid).order_by('-visitTime')[:1]
    else:
        visitSetList = Visit.objects.filter(host=getIP(request), site__id=siteid).order_by('-visitTime')[:1]

    if visitSetList.count() == 0:
        return None, 0
    else:
        lvt = visitSetList.values('visitTime')[0]['visitTime']
        interval = Site.objects.get(id=siteid).interval
        # lt = interval - int((timezone.now() - lvt).total_seconds())/60
        # refer: http://docs.python.org/2/library/datetime.html#datetime.timedelta.total_seconds
        # total_seconds is New in version 2.7.
        # so we can use 'td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6' which equals to total_seconds
        td = (timezone.now() - lvt)
        lt = interval - int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6) / 60
        lt = lt if lt >= 0 else 0
        return lvt, lt


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
            sited - the site.pk, unique identification the site
        @returns: True or False boolean
    '''
    if 'usr' in request.COOKIES:
        return Favorite.objects.filter(user__username=request.COOKIES['usr'], site__id=siteid).count() != 0
    else:
        return Favorite.objects.filter(host=getIP(request), site__id=siteid).count() != 0


def getEvaNum(request, siteid):
    '''
        @function: get the num of site's evaluate
        @paras:
            sited - the site.pk, unique identification the site
        @returns: num int
    '''
    return Evaluate.objects.filter(site__id=siteid).count()


def getProofNum(request, siteid):
    '''
        @function: get the num of site's proof
        @paras:
            sited - the site.pk, unique identification the site
        @returns: num int
    '''
    return Proof.objects.filter(site__id=siteid).count()


def siteDictAdd(request, siteid, siteDict):
    siteDict['lastvisittime'], siteDict['lefttime'] = getLastVisitTime(request, siteid)
    siteDict['like'] = getLikeFlag(request, siteid, True)
    siteDict['unlike'] = getLikeFlag(request, siteid, False)
    siteDict['fav'] = getFavFlag(request, siteid)
    siteDict['siteEvaNum'] = getEvaNum(request, siteid)
    siteDict['siteProofNum'] = getProofNum(request, siteid)
    return siteDict


def sitePerfectInfo(request, siteSetList, flag):
    site = []
    for siteSet in siteSetList:
        siteid = siteSet.id if 0 == flag else siteSet.site_id
        siteDict = model_to_dict(siteSet) if 0 == flag else model_to_dict(siteSet.site)
        siteDict = siteDictAdd(request, siteid, siteDict)
        site.append(siteDict)
    return site


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
        siteSetList = csySet.site_set.filter(display=0).order_by('-siteDateTime') if 1 == _rank else csySet.site_set.filter(display=0).order_by('-siteClickNum')
        csyDict['siteSet'] = sitePerfectInfo(request, siteSetList, 0)
        csysite.append(csyDict)
    return csysite


def getFavSite(request):
    _usr, _host = getUsrHost(request)
    favSetList = Favorite.objects.filter(user__username=_usr, site__display=0).order_by('-site__siteClickNum') if 'usr' in request.COOKIES else Favorite.objects.filter(host=_host, site__display=0).order_by('-site__siteClickNum')
    return sitePerfectInfo(request, favSetList, 1)


def getProofSite(request):
    proofSetList = Site.objects.filter(display=0).exclude(siteProofNum=0).order_by('-siteProofNum')
    return sitePerfectInfo(request, proofSetList, 0)


def getLastestSite(request):
    lastSetList = Site.objects.filter(display=0).exclude(classify__in=[37, 27, 18, 6]).order_by('-siteDateTime')[:8]
    return sitePerfectInfo(request, lastSetList, 0)


def gethottestSite(request):
    hotSetList = Site.objects.filter(display=0).exclude(classify__in=[27, 18, 6]).order_by('-siteClickNum')[:8]
    return sitePerfectInfo(request, hotSetList, 0)


def getDustBin(request):
    dustbinSetList = Site.objects.filter(display=1)
    return sitePerfectInfo(request, dustbinSetList, 0)


def fav(request):
    reDict = {'nav': getNav(request), 'favsite': getFavSite(request), 'proofsite': getProofSite(request), 'lastest': getLastestSite(request), 'hottest': gethottestSite(request), 'usr': getUsr(request), 'wallet': getWallet(request)}
    return render_to_response('freebtc123/fav.html', reDict)


def getNumSite(request, num):
    qs = Site.objects.filter(classify__nav__navName='freebtc', display=0).exclude(classify__in=[36, 30, 27, 6, 5])
    try:
        return qs[num], num + 1
    except:
        return qs[0], 1


def getCsyNumSite(request, num, csyid):
    qs = Site.objects.filter(classify_id=csyid, display=0)
    try:
        return qs[num], num + 1
    except:
        return qs[0], 1


def next(request, num, csyid=-1):
    numsite, num = getNumSite(request, int(num)) if -1 == csyid else getCsyNumSite(request, int(num), int(csyid))
    reDict = {'nav': getNav(request), 'csyid': csyid, 'numsite': numsite, 'num': num, 'usr': getUsr(request)}
    reHtml = 'freebtc123/btcreaper.html' if -1 == csyid else 'freebtc123/csyreaper.html'
    return render_to_response(reHtml, reDict)


def btcreaper(request, csyid=-1):
    reDict = {'nav': getNav(request), 'csyid': csyid, 'numsite': -1, 'num': 0, 'usr': getUsr(request)}
    reHtml = 'freebtc123/btcreaper.html' if -1 == csyid else 'freebtc123/csyreaper.html'
    return render_to_response(reHtml, reDict)


def freebtc(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'freebtc', 0), 'usr': getUsr(request), 'wallet': getWallet(request)}
    return render_to_response('freebtc123/freebtc.html', reDict)


def altcoin(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'altcoin', 0), 'usr': getUsr(request), 'wallet': getWallet(request)}
    return render_to_response('freebtc123/altcoin.html', reDict)


def btcforum(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'btcforum', 0), 'usr': getUsr(request), 'wallet': getWallet(request)}
    return render_to_response('freebtc123/btcforum.html', reDict)


def btcwiki(request):
    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'btcwiki', 1), 'usr': getUsr(request), 'wallet': getWallet(request)}
    return render_to_response('freebtc123/btcwiki.html', reDict)


def submitsite(request):
    verify_url = 'http://www.google.com/recaptcha/api/verify'

    _name = request.POST.get('name', '')
    _description = request.POST.get('description', '')
    _url = request.POST.get('url', '')

    robots = False
    if _url == '':
        pass
    else:
        _recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field', '')
        _recaptcha_response_field = request.POST.get('recaptcha_response_field', '')
        data = {'privatekey': '6LfWhe0SAAAAAEkkiS0DD2w0u2xWA1gxpvFGt7YP', 'remoteip': getIP(request), 'challenge': _recaptcha_challenge_field, 'response': _recaptcha_response_field}
        re = requests.post(verify_url, data)

        if u'true' in re.text:
            csySet = Classify.objects.get(nav__navName='submitsite')
            Site.objects.create(siteName=_name, siteDescription=_description, siteUrl=_url, classify_id=csySet.id)
        else:
            robots = True

    reDict = {'nav': getNav(request), 'csysite': getCsySite(request, 'submitsite', 1), 'usr': getUsr(request), 'wallet': getWallet(request), 'robots': robots}
    return render_to_response('freebtc123/submitsite.html', reDict)


def dustbin(request):
    reDict = {'nav': getNav(request), 'dustbin': getDustBin(request)}
    return render_to_response('freebtc123/dustbin.html', reDict)


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
    siteDict = siteDictAdd(request, siteid, siteDict)
    eva = Evaluate.objects.filter(site__id=siteid).order_by('-evaDateTime')
    proof = Proof.objects.filter(site__id=siteid).order_by('-proofDateTime')
    reDict = {'nav': getNav(request), 'siteid': siteid, 'site': siteDict, 'eva': eva, 'proof': proof, 'usr': getUsr(request), 'wallet': getWallet(request)}
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
    response = render_to_response('freebtc123/evaluate.html', getEvaluateDict(request, siteid))
    response.set_cookie('siteid', siteid)
    return response


def proof(request, siteid):
    verify_url = 'http://www.google.com/recaptcha/api/verify'

    _proof = request.POST.get('proof', '')

    robots = False
    if _proof == '':
        print 'Just get Proofs!!!'
    else:
        _recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field', '')
        _recaptcha_response_field = request.POST.get('recaptcha_response_field', '')
        data = {'privatekey': '6LfWhe0SAAAAAEkkiS0DD2w0u2xWA1gxpvFGt7YP', 'remoteip': getIP(request), 'challenge': _recaptcha_challenge_field, 'response': _recaptcha_response_field}
        re = requests.post(verify_url, data)

        if u'true' in re.text:
            s = Site.objects.get(id=siteid)
            s.siteProofNum = s.siteProofNum + 1
            s.save()
            Proof.objects.create(site_id=siteid, proofContent=_proof)
        else:
            robots = True
    print robots

    reDict = dict(robots=robots, **getEvaluateDict(request, siteid))
    return render_to_response('freebtc123/evaluate.html', reDict)


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


def about(request):
    reDict = {'nav': getNav(request), 'usr': getUsr(request), 'wallet': getWallet(request)}
    return render_to_response('freebtc123/about.html', reDict)


def newtobtc(request):
    reDict = {'nav': getNav(request), 'usr': getUsr(request), 'wallet': getWallet(request)}
    return render_to_response('freebtc123/newtobtc.html', reDict)
