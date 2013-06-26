# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from coop_local.models import (Location, )
import urllib
import json
from django.utils.http import urlquote
from django.contrib.gis.geos import Point


def google_geocode(lieu):

    encoded = urlquote(lieu.encode('utf-8'))
    components = u'&components=country:FR'
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s%s&sensor=false' % (encoded, components)
    print url
    data_str = urllib.urlopen(url).read()
    data_json = json.loads(data_str, parse_float=str)
    try:
        lat  = data_json['results'][0]['geometry']['location']['lat']
        lng  = data_json['results'][0]['geometry']['location']['lng']
        return 'POINT(%s %s)' % (lng, lat)
    except IndexError:
        return None


class Command(BaseCommand):

    def handle(self, *args, **options):

        for location in Location.objects.filter(point__isnull=True):
            print '-' * 40
            print location
            point = google_geocode(location.adr1 + ', ' + location.city)
            if point:
                location.point = point
                location.save()

