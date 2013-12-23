from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


class Wallet(models.Model):
    walletUrl = models.CharField(_(u'walleturl'), max_length=255)

    class Meta:
        db_table = u'wallet'
        verbose_name = _(u'wallet')
        verbose_name_plural = _(u'wallet')

    def __unicode__(self):
        return self.walletUrl


class UserInfo(models.Model):
    username = models.CharField(_(u'username'), max_length=255, blank=True, null=True)
    password = models.CharField(_(u'password'), max_length=255, blank=True, null=True)
    email = models.CharField(_(u'email'), max_length=255, blank=True, null=True)
    wallet = models.ForeignKey(Wallet, verbose_name=_(u'wallet'), blank=True, null=True)

    class Meta:
        db_table = u'userinfo'
        verbose_name = _(u'userinfo')
        verbose_name_plural = _(u'userinfo')

    def __unicode__(self):
        return unicode(self.id)
