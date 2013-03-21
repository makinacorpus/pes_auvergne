# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.page.models import AbstractPageApp

class PageApp_Members(AbstractPageApp):
    
    # Define your fields here
    type = models.CharField(_(u'type'), max_length=75)
    
    def __unicode__(self):
        return u'Members #%d' % (self.pk)

    class Meta:
        verbose_name = _(u"Members")
        
