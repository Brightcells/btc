# -*- coding: utf-8 -*-

###
# ErrorCode: 100***, for userCheck
#     {'errorCode': 100200, 'errorString': 'User not exists, you can use it to register'}
#     {'errorCode': 100201, 'errorString': 'User already exists, pls change a username to register'}
# ErrorCode: 200***, for likeSite
#     {'errorCode': 200200, 'errorString': 'Like/Unlike the site success'}
#     {'errorCode': 200201, 'errorString': 'You have already like/unlike the site, don\'t hesitate'}
#     {'errorCode': 200202, 'errorString': 'Cancel like/unlike the site success'}
# ErrorCode: 300***, for Favorite
#     {'errorCode': 300200, 'errorString': 'Favorite the site success'}
#     {'errorCode': 300201, 'errorString': 'The parm of siteid not transmitted success'}
#     {'errorCode': 300202, 'errorString': 'Cancel favorite the site success'}
# ErrorCode: 400***, for Visit
#     {'errorCode': 400200, 'errorString': 'Record the visit success'}
#     {'errorCode': 400201, 'errorString': 'Record the visit failure'}
# ErrorCode: 500***, for
###

from django.contrib.auth.models import User
from freebtc123.models import Wallet, UserInfo, Nav, Classify, Site, Evaluate, Like, Favorite, Visit, Log

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


errorCodeDict = {
    'user_not_exists': {'errorCode': 100200, 'errorString': 'User not exists, you can use it to register'},
    'user_already_exists': {'errorCode': 100201, 'errorString': 'User already exists, pls change a username to register'},
    'like_unlike_success': {'errorCode': 200200, 'errorString': 'Like/Unlike the site success'},
    'already_like_unlike': {'errorCode': 200201, 'errorString': 'You have already like/unlike the site, don\'t hesitate'},
    'cancel_like_unlike_success': {'errorCode': 200202, 'errorString': 'Cancel like/unlike the site success'},
    'favorite_site_success': {'errorCode': 300200, 'errorString': 'Favorite the site success'},
    'site_id_not_exists': {'errorCode': 300201, 'errorString': 'The parm of siteid not transmitted success'},
    'cancel_favorite_success': {'errorCode': 300202, 'errorString': 'Cancel favorite the site success'},
    'record_visit_success': {'errorCode': 400200, 'errorString': 'Record the visit success'},
    'record_visit_fail': {'errorCode': 400201, 'errorString': 'Record the visit failure'},
}


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


def getRef(request):
    '''
        @function: get ref from cookies, and if not exists, set ref 'freebtc123:fav'
        @paras:
        @returns: ref string
    '''
    return request.COOKIES['ref'] if 'ref' in request.COOKIES else 'freebtc123:fav'


def getNav(request):
    '''
        @function: get all nav from table Nav
        @paras:
        @returns: nav dict query set
    '''
    return Nav.objects.all().order_by('navPosition')


def getErrorCode(_key):
    '''
        @function: general control error code, return error code by key
        @paras: _key
        @returns: error code dict
    '''
    return errorCodeDict[_key]


def pwd2hash(pwd):
    '''
        @function: change pwd 2 hash by use hashlib's md5 method
        @paras:
        @returns: hexdigest string
    '''
    hashpwd = hashlib.md5()
    hashpwd.update(pwd)
    return hashpwd.hexdigest()


def usercheck(request):
    '''
        @function: check whether user has already been registered
        @paras:
        @returns: errorCode json string
    '''
    _usr = request.POST.get('usr', '')
    if UserInfo.objects.filter(username=_usr).count() == 0:
        return HttpResponse(json.dumps(getErrorCode('user_not_exists')))
    else:
        return HttpResponse(json.dumps(getErrorCode('user_already_exists')))


# ref & modify: https://djangosnippets.org/snippets/1474/
def get_referer_view(request, default='freebtc123:fav'):
    '''
    Return the referer view of the current request

    Example:

        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    #if referer[0] != request.META.get('SERVER_NAME'):
    #    return default

    if referer[1] in ['accounts', ]:
        return getRef(request)

    if referer[1] in ['', 'index', 'home']:
        return default

    # add the slash at the relative path's view and finished
    if 2 == len(referer):
        referer = u'freebtc123:' + u':'.join(referer[1:])
    else:
        referer = u':'.join(referer[1:])

    return referer


def delCookie(request, response, key):
    '''
        @function: del cookie by key
        @paras:
            √ request -
            √ request -
            √ key - the key by which to del
        @returns: None
    '''
    if key in request.COOKIES:
        response.delete_cookie(key)
