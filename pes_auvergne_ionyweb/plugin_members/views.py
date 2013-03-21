# -*- coding: utf-8 -*-
from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view

from coop_local.models import Organization
from django.conf import settings

# from ionyweb.website.rendering.medias import CSSMedia, JSMedia, JSAdminMedia
MEDIAS = (
    # App CSS
    # CSSMedia('plugin_members.css'),
    # App JS
    # JSMedia('plugin_members.js'),
    # Actions JSAdmin
    # JSAdminMedia('plugin_members_actions.js'),
    )
from ionyweb.website.rendering.medias import CSSMedia
MEDIAS = (
    CSSMedia('plugin_members.css'),
    )
    
    
def index_view(request, plugin):
    
    organizations = Organization.objects.all()
    
    return render_view('plugin_members/index.html',
                       {'object': plugin, 'members': organizations, 'media_path': settings.MEDIA_URL},
                       MEDIAS,
                       context_instance=RequestContext(request))