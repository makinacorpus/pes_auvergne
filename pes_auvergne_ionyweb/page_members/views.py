# -*- coding: utf-8 -*-

from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view

from coop_local.models import Organization
from django.conf import settings

from django.shortcuts import get_object_or_404

from ionyweb.website.rendering.medias import CSSMedia

MEDIAS = (
    CSSMedia('page_members.css'),
    )

def index_view(request, page_app):
    if page_app.type != "":
        organizations = Organization.objects.filter(category__label=page_app.type)
    else:
        organizations = Organization.objects.all()
            
    base_url = u'%sp/' % (page_app.get_absolute_url())
    
    direct_link = False
    if page_app.type == settings.COOP_PARTENAIRE_LABEL:
        direct_link = True
    
    return render_view('page_members/index.html',
                       { 'object': page_app, 'members': organizations, 'media_path': settings.MEDIA_URL, 'base_url': base_url, 'direct_link': direct_link},
                       MEDIAS,
                       context_instance=RequestContext(request))


def detail_view(request, page_app, pk):
    member = get_object_or_404(Organization, pk=pk)
    return render_view('page_members/detail.html',
                       { 'member':  member, 'media_path': settings.MEDIA_URL },
                       MEDIAS,
                       context_instance=RequestContext(request))