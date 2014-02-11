from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('freebtc.views',
    url(r'^$', 'home', name='home'),
    url(r'^index$', 'home', name='home'),
    url(r'^home$', 'home', name='home'),
    url(r'^captcha$', 'captcha', name='captcha'),
    url(r'^verify$', 'verify', name='verify'),
)
