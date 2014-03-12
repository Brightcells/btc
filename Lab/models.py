# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from accounts.models import UserInfo


class Game2048(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name=_(u'user'), blank=True, null=True)
    host = models.GenericIPAddressField(_('host'), max_length=20, blank=True, null=True)
    flag = models.BooleanField(_('flag'), default=True)
    score = models.IntegerField(_(u'score'), blank=True, null=True, default=0)
    create_time = models.DateTimeField(_(u'createtime'), auto_now_add=True, editable=True)
    modify_time = models.DateTimeField(_(u'modifytime'), auto_now=True, editable=True)

    class Meta:
        db_table = u'game2048'
        verbose_name = _(u'game2048')
        verbose_name_plural = _(u'game2048')

    def __unicode__(self):
        return unicode(self.id)
