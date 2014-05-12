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


def home(request):
    return render_to_response('freebtc/home.html')


def captcha(request):
    _wallet = request.POST.get('wallet', '')
    reDict = {'wallet': _wallet, 'tips': False}
    response = render_to_response('freebtc/verify.html', reDict)
    response.set_cookie('wa', _wallet)
    return response


def verify(request):
    verify_url = 'http://www.google.com/recaptcha/api/verify'
    _wallet = request.COOKIES['wa']
    _recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field', '')
    _recaptcha_response_field = request.POST.get('recaptcha_response_field', '')
    data = {'privatekey': '6LfWhe0SAAAAAEkkiS0DD2w0u2xWA1gxpvFGt7YP', 'remoteip': getIP(request), 'challenge': _recaptcha_challenge_field, 'response': _recaptcha_response_field}
    re = requests.post(verify_url, data)
    reDict = {'wallet': _wallet, 'tips': True, 'success': u'true' in re.text}
    return render_to_response('freebtc/verify.html', reDict)