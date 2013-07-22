# -*- coding:utf-8 -*-
import csv
import sys
import time
import datetime
import logging
import re

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from coop_tag.settings import get_class
from coop_geo.models import LocationCategory
from coop.org.models import COMM_MEANS

from coop_local.models import (Organization, LegalStatus, OrganizationCategory,
    Contact, Location, ContactMedium, Located, ActivityNomenclature, Offer,
    TransverseTheme, Person, Engagement)


# The purpose of this script is to import human-made data (csv file) for CREDIS providers
# Columns are :
# 0 - Nom de l'organisation
# 1 - Sigle
# 2 - Préférence entre Sigle et Nom
# 3 - Date de création
# 4 - Statut juridique
# 5 - Type de structure ESS
# 6 - Description succincte
# 7 - Liste des produits et service
# 8 - Jour d’ouverture et horaire
# 9 - Présentation générale
# 10 - Adresse préférée
# 11 - Code postal
# 12 - Ville
# 13 - Personne
# 14 - Téléphone préféré
# 15 - Courriel préféré
# 16 - Site web
# 17 - Secteurs d'activité (1)
# 18 - Secteurs d'activité (2)
# 19 - Secteurs d'activité (3)
# 20 - Secteurs d'activité (4)
# 21 - Thématiques transversales (1)
# 22 - Thématiques transversales (2)
# 23 - Mots clés de la structure
# 24 - Garanties
# 25 - Garanties (1)
# 26 - Type de relation
# 27 - Organisation cible
# 28 - Source Info

current_time = datetime.datetime.now()
logging.basicConfig(filename='%(date)s_structure_migration.log' % {'date': current_time.strftime("%Y-%m-%d")},
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',)

Tag = get_class('tag')

class Command(BaseCommand):
    args = '<import_file>'
    help = 'Import organization file'

    def handle(self, *args, **options):

        for import_file in args:

            errors_array = []
            dest_file = csv.DictReader(open(import_file, 'rb'), delimiter=';', quotechar='"')

            for line, _row in enumerate(dest_file):

                row = {}
                for k, v in _row.iteritems():
                    row[k.decode('utf8')] = v.decode('utf8')

                title = row[u'Nom de l\'organisation']
                acronym = row[u'Sigle']

                person = row[u'Personne'].strip()
                tel = row[u'Téléphone préféré'].strip()
                email = row[u'Courriel préféré'].strip()
                source_info = row[u'Source Info']
                #members = models.ManyToManyField('coop_local.Person', through='coop_local.Engagement', verbose_name=_(u'members'))
                
                print line + 1, '-', title

                # Find organization
                try:
                    organization = Organization.objects.get(title=title, acronym=acronym);
                    
                    organization.source_info = source_info
                    if tel:
                        _save_contact(organization, tel, 'Téléphone', True, True, 'pref_phone')
                    if email:
                        _save_contact(organization, email, 'Email', False, True, 'pref_email')
                    
                    # Si person is empty but not email
                    #if person and len(person) == 0 and len(email) > 0:
                    if len(person) == 0 and len(email) > 0:
                        person = email[0:24]
                    
                    if person and len(person) > 0:
                        new_person = _save_person(person, title, email)
                        # TODO: check if it works
                        
                        try:
                            engagement = Engagement.objects.get(person=new_person,organization=organization)
                        except Engagement.DoesNotExist:
                            print "New engagement"
                            engagement = Engagement(person=new_person,organization=organization)
                            engagement.save()
                        

                    organization.save()    
                except Organization.DoesNotExist:
                    print "Organization not found: %s" % (title)
                

                
def _save_person(data, structure_name, email):
    names = data.split(" ")
    first_name = ""
    last_name = ""
    if len(names) > 0:
        first_name = names[0]
    if len(names) > 1:
        last_name = names[1]
    
    try:
        person = Person.objects.get(first_name=first_name, last_name=last_name, structure=structure_name, email=email)
    except Person.DoesNotExist:
        print "New  person created: %s" % (email)
        person = Person(first_name=first_name, last_name=last_name, structure=structure_name, email=email)
        person.save()
        
    try:
        u = User.objects.get(username=person.username, first_name=first_name, last_name=last_name, email=email, is_active=True)
    except User.DoesNotExist:
        print "User created"
        u = User(username=person.username, first_name=first_name, last_name=last_name, email=email, is_active=True, password=User.objects.make_random_password())
        u.save()
            
        person.user = u   
        person.save()

    return person


def _save_contact(provider, data, category, is_tel_number, set_provider_field=False, provider_field_name=None):

    if is_tel_number:
        data = _format_number_to_bd_check(_clean_tel(data))

    medium = ContactMedium.objects.get(label=category)
    
    contacts = Contact.objects.filter(contact_medium=medium, content=data)

    if (contacts.count() == 0):
        # get_or_create method cannot be called because of generic Contact model relation
        # so we try get, and create it manually if does not exists
        print "New  contact created"
        contact = Contact(content_object=provider,contact_medium=medium, content=data)
        contact.save()
    else:
        if (contacts.count() > 1):
            print "Contact has duplicated entries"
            #logging.warn("Contact > %(data)s < of category %(category)s has duplicated entries" 
            #            % {'data': data, 'category': category})
        contact = contacts[0]
        contact.content_object = provider
        contact.save()

    if set_provider_field:
        _set_attr_if_empty(provider, provider_field_name, contact)


# Save field only if there is no data
# to avoid overwriting client manual work on preprod
def _set_attr_if_empty(obj, field_name, data):

    field_value = getattr(obj, field_name)
    if ((field_value == None) or (field_value == '')):
        setattr(obj, field_name, data)


def _set_attr_m2m(obj, field_name, data):

    field_value = getattr(obj, field_name)
    field_value.add(data)


def _format_number_to_bd_check(data):

    return ".".join([data[0:2], data[2:4], data[4:6], data[6:8], data[8:10]])


def _is_valid(data):

    return (data != "")


def _clean_tel(data):

    data = re.sub(r'[^\d]', '', data)

    # Some tel number lacks first "0"
    if data[0] != '0':
        data = "0" + data

    return data


def _clean_int(data):
    
    if _is_valid(data):
        return int(data.replace(' ', ''))


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):

    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    return csv_reader


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
