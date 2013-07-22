# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from coop_local.models import (Location, )
import urllib
import json
from django.utils.http import urlquote
import csv

from coop_local.models import Organization
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

# The purpose of this script is to import human-made data (csv file) for CREDIS providers
# Columns are :
# 0 - id
# 1 - username
# 2 - password
# 3 - email


class Command(BaseCommand):

    def handle(self, *args, **options):

        for import_file in args:
            errors_array = []
            dest_file = csv.DictReader(open(import_file, 'rb'), delimiter=';', quotechar='"')

            for line, _row in enumerate(dest_file):

                row = {}
                for k, v in _row.iteritems():
                    row[k.decode('utf8')] = v.decode('utf8')

                title = "Email de test"
                content_text = "Ceci est un test de mail"
                content_html = "<h1>Ceci est un test de mail<h1>"
                sender = "contact@echanges-solidaires-auvergne.fr"
                dest = row[u'email'].strip()
                
                #send_mail(title, content, sender, [dest], fail_silently=False)
                #for o in Organization.objects.filter(is_project=False).order_by('title'):
                #    print o.title

                msg = EmailMultiAlternatives(title, content_text, sender, [dest])
                msg.attach_alternative(content_html, "text/html")
                msg.send()
                