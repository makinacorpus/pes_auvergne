# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.plugin.models import AbstractPlugin


class Plugin_CoopMembersIcons(AbstractPlugin):
    
    # Define your fields here
    type = models.CharField(_(u'type'), max_length=75)

    def __unicode__(self):
        return u'CoopMembersIcons #%d' % (self.pk)

    class Meta:
        verbose_name = _(u"CoopMembersIcons")