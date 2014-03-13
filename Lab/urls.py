from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('Lab.views',
    url(r'^$', 'home', name='home'),
    url(r'^index$', 'home', name='home'),
    url(r'^home$', 'home', name='home'),

    url(r'^game-2048$', 'game_2048', name='game-2048'),
    url(r'^game-2048-left$', 'game_2048_left', name='game-2048-left'),
    url(r'^game-2048-right$', 'game_2048_right', name='game-2048-right'),
    url(r'^game-2048-score$', 'game_2048_score', name='game_2048-score'),
    url(r'^game-2048-pk$', 'game_2048_pk', name='game-2048-pk'),
    url(r'^game-2048-rank$', 'game_2048_rank', name='game-2048-rank'),
    url(r'^game-2048-rank/(?P<p>\d+)/$', 'game_2048_rank', name='game-2048-rank'),
    url(r'^game-2048-history$', 'game_2048_history', name='game-2048-history'),
    url(r'^game-2048-history/(?P<p>\d+)/$', 'game_2048_history', name='game-2048-history'),
)
