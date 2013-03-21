# -*- coding: utf-8 -*-

from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view

from coop_local.models import Event, EventCategory, Calendar, Occurrence
from django.conf import settings

from django.shortcuts import get_object_or_404

from ionyweb.website.rendering.medias import CSSMedia
from datetime import datetime

MEDIAS = (
    CSSMedia('page_coop_agenda.css'),
    )

def index_view(request, page_app):
    
    base_url = u'%sp/' % (page_app.get_absolute_url())

    agenda = get_object_or_404(Calendar, sites__id=settings.SITE_ID)
    categories = {}
    
    for cat in EventCategory.objects.all():
        occ = Occurrence.objects.filter(
                            end_time__gt=datetime.now(),
                            event__active=True,
                            event__calendar=agenda,
                            event__category=cat
                            ).order_by("start_time")
        if occ.exists():
            categories[cat] = occ

    rdict = {'agenda': agenda, 'events_by_categories': categories, 'object': page_app, 'base_url': base_url}
    
    return render_view('page_coop_agenda/index.html',
                       rdict,
                       MEDIAS,
                       context_instance=RequestContext(request))


def detail_view(request, page_app, pk):
    event = get_object_or_404(Event, pk=pk)
    base_url = u'%sp/' % (page_app.get_absolute_url())
    rdict = {'object': page_app, 'e': event, 'media_path': settings.MEDIA_URL, 'base_url': base_url}
    return render_view('page_coop_agenda/detail.html',
                       rdict,
                       MEDIAS,
                       context_instance=RequestContext(request))                              