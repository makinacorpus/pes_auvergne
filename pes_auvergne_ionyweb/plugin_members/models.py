# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.plugin.models import AbstractPlugin


class Plugin_Members(AbstractPlugin):
    
    # Define your fields here

    def __unicode__(self):
        return u'Members #%d' % (self.pk)

    class Meta:
        verbose_name = _(u"Members")