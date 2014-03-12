from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('Lab.views',
    #url(r'^$', 'home', name='home'),
    #url(r'^index$', 'home', name='home'),
    #url(r'^home$', 'home', name='home'),

    url(r'^game-2048$', 'game_2048', name='game-2048'),
    url(r'^game-2048-score$', 'game_2048_score', name='game-2048_score'),
)
