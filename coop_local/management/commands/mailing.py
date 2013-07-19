# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from coop_local.models import (Location, )
import urllib
import json
from django.utils.http import urlquote

from coop_local.models import Organization
from django.core.mail import send_mail

class Command(BaseCommand):

    def handle(self, *args, **options):

        title = "Email de test"
        content = "Ceci est un test de mail"
        sender = "sylvain.beorchia@makina-corpus.com"
        dest = "sylvain.beorchia@makina-corpus.com"
        send_mail(title, content, sender, [dest], fail_silently=False)
        #for o in Organization.objects.filter(is_project=False).order_by('title'):
        #    print o.title

