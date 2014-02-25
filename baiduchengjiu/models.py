from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


class Scores(models.Model):
    uid = models.CharField(_(u'uid'), max_length=255, blank=True, null=True)
    img = models.CharField(_(u'img'), max_length=255, blank=True, null=True)
    score = models.IntegerField(_(u'score'), blank=True, null=True, default=0)
    grade = models.IntegerField(_(u'grade'), blank=True, null=True, default=0)

    class Meta:
        db_table = u'scores'
        verbose_name = _(u'scores')
        verbose_name_plural = _(u'scores')

    def __unicode__(self):
        return unicode(self.uid)
