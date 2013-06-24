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
from coop_tag.settings import get_class
from coop_geo.models import LocationCategory
from coop.org.models import COMM_MEANS

from coop_local.models import (Organization, LegalStatus, OrganizationCategory,
    Contact, Location, ContactMedium, Located, ActivityNomenclature, Offer,
    TransverseTheme)


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

                print line + 1, '-', title

                (provider, created) = Organization.objects.get_or_create(title=title, acronym=acronym);

                provider.pref_label = {'Nom': 1, 'Sigle': 2}[row[u'Préférence entre Sigle et Nom']]

                annee = row[u'Date de création']

                if annee:
                    provider.birth = annee + '-01-01'

                legal_status = row[u'Statut juridique']
                try:
                    provider.legal_status = LegalStatus.objects.get(label=legal_status)
                except LegalStatus.DoesNotExist:
                    logging.warn("Unknown Status : >" + legal_status + "<")

                ess_structures = row[u'Type de structure ESS']
                if ess_structures:
                    ess_structures_list = ess_structures.split(",")
                    for ess_structure in ess_structures_list:
                        try:
                            obj = OrganizationCategory.objects.get(slug=slugify(ess_structure))
                            provider.category.add(obj)
                        except Exception as e:
                            msg = "Unknown CategoryESS >%(ess_structure)s< for %(name)s" \
                                                % {'ess_structure': ess_structure, 'name': title}
                            logging.warn(msg)

                provider.short_description = row[u'Description succincte']
                provider.description = row[u'Présentation générale']

                # TODO
                offers = row[u'Liste des produits et service']

                if Located.objects.filter(organization=provider, main_location=True).exists():
                    located = Located.objects.filter(organization=provider, main_location=True)[0]
                else:
                    print 'located: not found'
                    located = Located(content_object=provider, main_location=True)
                    location = Location()
                    located.location = location
                    location.adr1 = row[u'Adresse préférée']
                    location.zipcode = row['Code postal']
                    location.city = row[u'Ville']
                    location.save()
                    located.location = location
                located.opening = row[u'Jour d’ouverture et horaire']

                provider.web = row[u'Site web']

                for i in range(1, 5):
                    if row[u'Secteurs d\'activité (%u)' % i]:
                        labels = [l.strip() for l in row[u'Secteurs d\'activité (%u)' % i].split('/')]
                        print 'labels:', labels
                        try:
                            activity = ActivityNomenclature.objects.get(level=2, label__iexact=labels[2])
                            print activity
                            if not provider.offer_set.filter(activity=activity).exists():
                                print 'ajout activity'
                                provider.offer_set.add(Offer(activity=activity))
                        except ActivityNomenclature.DoesNotExist:
                            print "Unknown ActivityNomenclature : >" + labels[2] + "<"
                            logging.warn("Unknown ActivityNomenclature : >" + labels[2] + "<")

                for i in range(1, 3):
                    if row[u'Thématiques transversales (%u)' % i]:
                        label = row[u'Thématiques transversales (%u)' % i]
                        print 'Thématiques:', labels
                        if not provider.transverse_themes.filter(name=label).exists():
                            print 'ajout theme'
                            theme, created = TransverseTheme.objects.get_or_create(name=label)
                            provider.transverse_themes.add(theme)

                keywords = row[u'Mots clés de la structure']
                if keywords:
                    tags_list = [t.strip() for t in keywords.split(",")]
                    for tag in tags_list:
                        slugified_tag = slugify(tag)
                        (obj, created) = Tag.objects.get_or_create(name=tag)
                        provider.tags.add(obj)


                provider.save()
                located.save()


def _save_contact(provider, data, category, is_tel_number, set_provider_field=False, provider_field_name=None):

    if is_tel_number:
        data = _format_number_to_bd_check(_clean_tel(data))

    contacts = Contact.objects.filter(category=category, content=data)

    if (contacts.count() == 0):
        # get_or_create method cannot be called because of generic Contact model relation
        # so we try get, and create it manually if does not exists
        medium = ContactMedium.objects.get(id=category)
        contact = Contact(content_object=provider, category=category, contact_medium=medium, content=data)
        contact.save()
    else:
        if (contacts.count() > 1):
            logging.warn("Contact > %(data)s < of category %(category)s has duplicated entries" 
                        % {'data': data, 'category': category})
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
