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
    help = 'Trim user login'

    def handle(self, *args, **options):

        for u in User.objects.all():
            if u.username.endswith(".") and len(u.username) > 1:
                before = u.username
                u.username = before[:-1]
                print "Login: %s => %s" % (before, u.username)
                u.save()
        
    
