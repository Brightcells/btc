from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from accounts.models import Wallet, UserInfo


class Nav(models.Model):
    navName = models.CharField(_(u'navname'), max_length=255)
    navTitle = models.TextField(_(u'navtitle'), blank=True, null=True)
    navPosition = models.IntegerField(_(u'navposition'), blank=True, null=True, default=0)

    class Meta:
        db_table = u'nav'
        verbose_name = _(u'nav')
        verbose_name_plural = _(u'nav')

    def __unicode__(self):
        return self.navName


class Classify(models.Model):
    csyName = models.CharField(_(u'csyname'), max_length=255)
    csyDescription = models.TextField(_(u'csydescription'), blank=True, null=True)
    # csySiteNum = models.IntegerField(_(u'csysitenum'), blank=True, null=True, default=0)
    # csySiteClickNum = models.IntegerField(_(u'csysiteclicknum'), blank=True, null=True, default=0)
    nav = models.ForeignKey(Nav, verbose_name=_(u'nav'), blank=True, null=True)
    csyPosition = models.IntegerField(_(u'csyposition'), blank=True, null=True, default=0)

    class Meta:
        db_table = u'classify'
        verbose_name = _(u'classify')
        verbose_name_plural = _(u'classify')

    def __unicode__(self):
        return self.csyName


class Site(models.Model):
    siteName = models.CharField(_(u'sitename'), max_length=255)
    siteDescription = models.TextField(_(u'sitedescription'), blank=True, null=True)
    siteUrl = models.CharField(_(u'siteurl'), max_length=255, blank=True, null=True)
    siteClickNum = models.IntegerField(_(u'siteclicknum'), blank=True, null=True, default=0)
    siteEvaluateNum = models.IntegerField(_(u'siteevaluatenum'), blank=True, null=True, default=0)
    siteLikeNum = models.IntegerField(_(u'sitelikenum'), blank=True, null=True, default=0)
    siteUnlikeNum = models.IntegerField(_(u'siteunlikenum'), blank=True, null=True, default=0)
    siteFavNum = models.IntegerField(_(u'sitefavnum'), blank=True, null=True, default=0)
    siteDateTime = models.DateTimeField(_(u'sitedatetime'), blank=True, null=True,  auto_now_add=True)
    classify = models.ForeignKey(Classify, verbose_name=_(u'classify'), blank=True, null=True)

    class Meta:
        db_table = u'site'
        verbose_name = _(u'site')
        verbose_name_plural = _(u'site')

    def __unicode__(self):
        return self.siteName


class Evaluate(models.Model):
    site = models.ForeignKey(Site, verbose_name=_(u'site'), blank=True, null=True)
    evaContent = models.TextField(_(u'eavcontent'), blank=True, null=True)
    evaDateTime = models.DateTimeField(_(u'evadatetime'), blank=True, null=True,  auto_now_add=True)

    class Meta:
        db_table = u'evaluate'
        verbose_name = _(u'evaluate')
        verbose_name_plural = _(u'evaluate')

    def __unicode__(self):
        return self.evaContent


class Like(models.Model):
    site = models.ForeignKey(Site, verbose_name=_(u'site'), blank=True, null=True)
    user = models.ForeignKey(UserInfo, verbose_name=_(u'user'), blank=True, null=True)
    wallet = models.ForeignKey(Wallet, verbose_name=_(u'wallet'), blank=True, null=True)
    host = models.GenericIPAddressField(_('host'), max_length=20, blank=True, null=True)
    flag = models.BooleanField(_('flag'), default=True)
    likeTime = models.DateTimeField(_(u'liketime'), blank=True, null=True,  auto_now_add=True)

    class Meta:
        db_table = u'like'
        verbose_name = _(u'like')
        verbose_name_plural = _(u'like')

    def __unicode__(self):
        return unicode(self.id)


class Favorite(models.Model):
    site = models.ForeignKey(Site, verbose_name=_(u'site'), blank=True, null=True)
    user = models.ForeignKey(UserInfo, verbose_name=_(u'user'), blank=True, null=True)
    wallet = models.ForeignKey(Wallet, verbose_name=_(u'wallet'), blank=True, null=True)
    host = models.GenericIPAddressField(_('host'), max_length=20, blank=True, null=True)
    favoriteTime = models.DateTimeField(_(u'favoritetime'), blank=True, null=True,  auto_now_add=True)

    class Meta:
        db_table = u'favorite'
        verbose_name = _(u'favorite')
        verbose_name_plural = _(u'favorite')

    def __unicode__(self):
        return unicode(self.id)


class Visit(models.Model):
    site = models.ForeignKey(Site, verbose_name=_(u'site'), blank=True, null=True)
    user = models.ForeignKey(UserInfo, verbose_name=_(u'user'), blank=True, null=True)
    wallet = models.ForeignKey(Wallet, verbose_name=_(u'wallet'), blank=True, null=True)
    host = models.GenericIPAddressField(_('host'), max_length=20, blank=True, null=True)
    visitTime = models.DateTimeField(_(u'visittime'), blank=True, null=True,  auto_now_add=True)

    class Meta:
        db_table = u'visit'
        verbose_name = _(u'visit')
        verbose_name_plural = _(u'visit')

    def __unicode__(self):
        return unicode(self.id)


class Log(models.Model):
    site = models.ForeignKey(Site, verbose_name=_(u'site'), blank=True, null=True)
    user = models.ForeignKey(UserInfo, verbose_name=_(u'user'), blank=True, null=True)
    wallet = models.ForeignKey(Wallet, verbose_name=_(u'wallet'), blank=True, null=True)
    host = models.GenericIPAddressField(_('host'), max_length=20, blank=True, null=True)
    descr = models.TextField(_('description'), blank=True, null=True)
    logTime = models.DateTimeField(_(u'logtime'), blank=True, null=True,  auto_now_add=True)

    class Meta:
        db_table = u'log'
        verbose_name = _(u'log')
        verbose_name_plural = _(u'log')

    def __unicode__(self):
        return unicode(self.id)
