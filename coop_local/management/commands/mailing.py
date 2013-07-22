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
from django.template.loader import get_template
from django.template import Context

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

                title = "Rejoindre la plate-forme d'échanges solidaires en Auvergne"
                #content_text = "Ceci est un test de mail"
                #content_html = "<h1>Ceci est un test de mail<h1>"
                sender = "contact@echanges-solidaires-auvergne.fr"
                dest = row[u'email'].strip()
                
                login = row[u'username'].strip()
                password = row[u'password'].strip()

                
                plaintext = get_template('email.txt')
                htmly     = get_template('email.html')

                d = Context({ 'login': login , 'password': password})

                subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
                #text_content = plaintext.render(d)
                text_content = "test"
                html_content = htmly.render(d)

                msg = EmailMultiAlternatives(title, text_content, sender, [dest])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                