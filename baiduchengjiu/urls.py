from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('baiduchengjiu.views',
    url(r'^$', 'scores', name='scores'),
    url(r'^index$', 'scores', name='scores'),
    url(r'^home$', 'scores', name='scores'),
    url(r'^cjadmin$', 'cjadmin', name='cjadmin'),
)
