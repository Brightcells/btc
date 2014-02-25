from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from baiduchengjiu.models import Scores


class ScoresAdmin(admin.ModelAdmin):
    list_display = ('uid', 'img', 'score', 'grade')


admin.site.register(Scores, ScoresAdmin)
