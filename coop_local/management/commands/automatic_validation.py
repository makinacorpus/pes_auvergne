# -*- coding:utf-8 -*-
import sys
import time
import datetime
import logging
import re
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from coop_local.models import Person, PersonPreferences, Organization, Exchange, Occurrence
    
from ionyweb_plugins.page_coop_account.views import get_user_pref_matches
from ionyweb_plugins.page_coop_blog.models import CoopEntry

class Command(BaseCommand):
    #
    help = 'Automatic validation'

    def handle(self, *args, **options):
        # For each objects not validated (status = P), validate if date creation > settings.MODERATION_VALIDATION_DAYS

        today = datetime.date.today()

        organizations = Organization.objects.filter(status='P')
        for o in organizations:
            limit_validation = o.creation + relativedelta(days=+settings.MODERATION_VALIDATION_DAYS)
            if type(limit_validation) is datetime.datetime:
                limit_validation = limit_validation.date()
            if today > limit_validation:
                o.status = 'V'
                o.save()

        exchanges = Exchange.objects.filter(status='P')
        for e in exchanges:
            limit_validation = e.created + relativedelta(days=+settings.MODERATION_VALIDATION_DAYS)
            if type(limit_validation) is datetime.datetime:
                limit_validation = limit_validation.date()
            if today > limit_validation:
                e.status = 'V'
                e.save()
        
        occ = Occurrence.objects.filter(event__status='P')
        for o in occ:
            limit_validation = o.event.created + relativedelta(days=+settings.MODERATION_VALIDATION_DAYS)
            if type(limit_validation) is datetime.datetime:
                limit_validation = limit_validation.date()
            if today > limit_validation:
                o.event.status = 'V'
                o.event.save()
        
        entries = CoopEntry.objects.filter(status_moderation='P')
        for e in entries:
            limit_validation = e.creation_date + relativedelta(days=+settings.MODERATION_VALIDATION_DAYS)
            if type(limit_validation) is datetime.datetime:
                limit_validation = limit_validation.date()
            if today > limit_validation:
                e.status_moderation = 'V'
                e.save()
        
    
