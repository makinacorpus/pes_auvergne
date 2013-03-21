# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.plugin.models import AbstractPlugin


class Plugin_CoopAgenda(AbstractPlugin):
    
    # Define your fields here
    agenda_url = models.CharField(_('Agenda url'), blank=True, max_length=250)
    
    category =  models.CharField(_('Category'), blank=True, max_length=100)

    def __unicode__(self):
        return u'CoopAgenda #%d' % (self.pk)

    class Meta:
        verbose_name = _(u"CoopAgenda")