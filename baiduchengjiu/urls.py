from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('baiduchengjiu.views',
    url(r'^$', 'scores', name='scores'),
    url(r'^index$', 'scores', name='scores'),
    url(r'^home$', 'scores', name='scores'),
    url(r'^scores$', 'scores', name='scores'),
    url(r'^scores/(?P<p>\d+)/$', 'scores', name='scores'),
    url(r'^update/(?P<_uid>[^/]+)/$', 'update', name='update'),
    url(r'^cjadmin$', 'cjadmin', name='cjadmin'),

    url(r'^getrank$', 'getrank', name='getrank'),
)
