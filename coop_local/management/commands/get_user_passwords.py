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


class Command(BaseCommand):
    #args = '<import_file>'
    help = 'Encrypt user passwords'

    def handle(self, *args, **options):

        #u = User.objects.get(username__exact="test")
        for u in User.objects.all():
            if u.password.startswith('pbkdf2_sha256$') or u.password.startswith('sha1$'):
                # do nothing
                print "%s - nothing" % (u.username)
            else:
                #print "%s - changed" % (u.username)
                u.set_password(u.password)
                u.save()
        
        #nathalie.marin  Nathalie    Marin   enfant.parents.et.campagnie63@orange.fr DcyTwCbZhj        
        #caroline.barot / 79ykhxx
    
