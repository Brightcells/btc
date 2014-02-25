from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'btc.views.home', name='home'),
    # url(r'^btc/', include('btc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^', include('freebtc123.urls', namespace='freebtc123')),
    url(r'^freebtc123/', include('freebtc123.urls', namespace='freebtc123')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^freebtc/', include('freebtc.urls', namespace='freebtc')),
    url(r'^baiduchengjiu/', include('baiduchengjiu.urls', namespace='baiduchengjiu')),
)
