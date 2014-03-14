from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from Lab.models import *


class Game2048Admin(admin.ModelAdmin):
    list_display = ('user', 'host', 'flag', 'score', 'videotape', 'create_time', 'modify_time')
    search_fields = ('user', 'host', 'flag', 'score')
    list_filter = ('user', )


admin.site.register(Game2048, Game2048Admin)
