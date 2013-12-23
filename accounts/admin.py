from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from freebtc123.models import Wallet, UserInfo


class WalletAdmin(admin.ModelAdmin):
    list_display = ('walletUrl',)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'wallet')


admin.site.register(Wallet, WalletAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
