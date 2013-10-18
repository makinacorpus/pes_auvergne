# -*- coding:utf-8 -*-
import sys
import time
import datetime
import logging
import re

from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from coop_local.models import Person, PersonPreferences
    
from ionyweb_plugins.page_coop_account.views import get_user_pref_matches

class Command(BaseCommand):
    #
    help = 'User notifications'

    def handle(self, *args, **options):

        # For each user (person), check preferences
        # If notifications are enabled, send email of each content that have changed in the last few days
        persons = Person.objects.all()
        for person in persons:
            if person.prefs:
                user_pref = get_object_or_404(PersonPreferences, pk=person.prefs.pk)
                if user_pref.notification:
                    items = get_user_pref_matches(user_pref, settings.NOTIFICATION_MAIL_DELTA)
        
                    title = "PES Auvergne - Notifications selon vos préférences"
                    sender = "contact@echanges-solidaires-auvergne.fr"
                    dest = person.user.email
                    
                    plaintext = get_template('management/commands/notification_pes.txt')

                    exchanges_url = settings.COOP_EXCHANGE_EXCHANGES_URL
                    organizations_url = settings.COOP_MEMBER_ORGANIZATIONS_URL
                    agenda_url = settings.COOP_AGENDA_URL
                    blog_url = settings.COOP_BLOG_URL
                    d = Context({ 'items': items , 'nb_days': settings.NOTIFICATION_MAIL_DELTA, 'exchanges_url': exchanges_url, 'organizations_url': organizations_url, 'agenda_url': agenda_url, 'blog_url': blog_url})

                    text_content = plaintext.render(d)

                    msg = EmailMultiAlternatives(title, text_content, sender, [dest])
                    msg.send()
    
