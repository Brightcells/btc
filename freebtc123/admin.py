from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from freebtc123.models import Nav, Classify, Site, Evaluate, Like, Favorite, Visit, Log


class NavAdmin(admin.ModelAdmin):
    list_display = ('navName', 'navTitle', 'navPosition')


class ClassifyAdmin(admin.ModelAdmin):
    list_display = ('csyName', 'csyDescription', 'nav', 'csyPosition')
    search_fields = ('csyName', 'csyDescription', 'nav__navName')
    list_filter = ('nav__navName', )


class SiteAdmin(admin.ModelAdmin):
    list_display = ('siteName', 'siteDescription', 'siteUrl', 'siteClickNum', 'siteEvaluateNum', 'siteLikeNum', 'siteUnlikeNum', 'siteFavNum', 'siteDateTime', 'classify')
    search_fields = ('siteName', 'siteDescription', 'siteUrl', 'classify__csyName')
    list_filter = ('siteDateTime', 'classify')
    date_hierarchy = 'siteDateTime'


class EvaluateAdmin(admin.ModelAdmin):
    list_display = ('site', 'evaContent', 'evaDateTime')
    search_fields = ('site__siteName', 'evaContent')
    list_filter = ('evaDateTime', 'site__siteName')
    date_hierarchy = 'evaDateTime'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'wallet', 'host', 'flag', 'likeTime')
    search_fields = ('site__siteName', 'user__username')
    list_filter = ('likeTime', 'site__siteName')
    date_hierarchy = 'likeTime'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'wallet', 'host', 'favoriteTime')
    search_fields = ('site__siteName', 'user__username')
    list_filter = ('favoriteTime', 'site__siteName')
    date_hierarchy = 'favoriteTime'


class VisitAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'wallet', 'host', 'visitTime')
    search_fields = ('site__siteName', 'user__username')
    list_filter = ('visitTime', 'site__siteName')
    date_hierarchy = 'visitTime'


class LogAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'wallet', 'host', 'descr', 'logTime')
    search_fields = ('site__siteName', 'user__username')
    list_filter = ('logTime', 'site__siteName')
    date_hierarchy = 'logTime'


admin.site.register(Nav, NavAdmin)
admin.site.register(Classify, ClassifyAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Evaluate, EvaluateAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Log, LogAdmin)
