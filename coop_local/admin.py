# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.conf.urls.defaults import patterns
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.admin import AdminSite
from django.template import RequestContext
from django.shortcuts import render_to_response
from coop_local.models import Organization
from django.utils.translation import ugettext_lazy as _
from coop.org.admin import OrganizationAdminForm
from tinymce.widgets import AdminTinyMCE
from coop.exchange.admin import ExchangeInline
from coop_geo.admin import LocatedInline
from coop.org.admin import ContactInline, EngagementInline, RelationInline, OfferInline, DocumentInline, ReferenceInline


try:
    from coop.base_admin import *
except ImportError, exp:
    raise ImproperlyConfigured("Unable to find coop/base_admin.py file")


class MyOrganizationAdminForm(OrganizationAdminForm):
    description = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 60}), required=False, label=u'Présentation générale')
    description2 = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 60}), required=False, label=u'En savoir plus')


admin.site.unregister(Organization)
class MyOrganizationAdmin(OrganizationAdmin):
    form = MyOrganizationAdminForm
    list_display = ('logo_list_display', 'label', 'id', 'active', 'has_description', 'has_location')
    fieldsets = (
        ('Identité', {
            'fields': ('is_project', 'logo', 'title', ('acronym', 'pref_label'), 'birth', 'active',
                        'web', 'crowdfunding')
            }),
        ('Description', {
            'fields': ('short_description', 'description', 'description2', 'category', 'tags', ('legal_status', 'secteur_fse'), ('siret', 'naf'), 'transverse_themes')
            }),
        (_(u'Economic info'), {
            'fields': [('annual_revenue', 'workforce')]
            }),
        (_(u'Management'), {
            'fields': ['creation', 'modification', 'status', 'correspondence', 'transmission',
                       'transmission_date', 'authors', 'validation', 'source_info']
            }),
        ('Préférences', {
            #'classes': ('collapse',),
            'fields': ('pref_email', 'pref_phone', 'pref_address', 'notes',)
            }),
        (_(u'Testimony'), {
            'fields': ['testimony',]
            }),
        (_(u'Guaranties'), {
            'fields': ['guaranties']
            }),
    )
    inlines = [
        ContactInline,
        EngagementInline,
        ExchangeInline,
        RelationInline,
        LocatedInline,
        OfferInline,
        DocumentInline,
        ReferenceInline,
    ]

admin.site.register(Organization, MyOrganizationAdmin)


# Obect validation view
def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^objects_to_validate/$', admin.site.admin_view(objects_to_validate))
        )
        return my_urls + urls
    return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls

def objects_to_validate(request):
    # list all objects that are waiting for a validation
    organizations_list = []
    exchanges_list = []
    occ_list = []
    projects_list = []
    entries_list = []

    # List all organizations
    organizations = Organization.objects.filter(is_project=False).exclude(status='V').order_by("-modified")
    for o in organizations:
        # automatic association of the user to this organization
        first_name = ''
        last_name = ''
        email = ''
        engagement = Engagement.objects.filter(organization=o)
        if engagement:
            if engagement.person:
                first_name = person.first_name
                last_name = person.last_name
                email = person.email
        url = "%sp/member_edit/%s" % (settings.COOP_MEMBER_ORGANIZATIONS_URL, o.pk)
        organizations_list.append({'title': o.title, 'first_name': first_name, 'last_name': last_name, 'email': email, 'url': url, 'status': o.get_status_display})
    
    # Exchanges
    exchanges = Exchange.objects.exclude(status='V').order_by("-modified")
    for e in exchanges:
        first_name = ''
        last_name = ''
        email = ''
        url = "%sp/exchange_edit/%s" % (settings.COOP_EXCHANGE_EXCHANGES_URL, e.pk)
        first_name = e.person.first_name
        last_name = e.person.last_name
        email = e.person.email
        exchanges_list.append({'title': e.title, 'first_name': first_name, 'last_name': last_name, 'email': email, 'url': url, 'status': e.get_status_display})
    
    # List all events
    occ = Occurrence.objects.exclude(event__status='V').order_by("start_time")
    for o in occ:
        first_name = ''
        last_name = ''
        email = ''
        url = "%sp/event_edit/%s" % (settings.COOP_AGENDA_URL, o.pk)
        if o.event.person:
            first_name = o.event.person.first_name
            last_name = o.event.person.last_name
            email = o.event.person.email
        occ_list.append({'title': o.title, 'first_name': first_name, 'last_name': last_name, 'email': email, 'url': url, 'status': o.event.get_status_display})

    
    # List all projects
    projects = Organization.objects.filter(is_project=True).exclude(status='V').order_by("-modified")
    for p in projects:
        # automatic association of the user to this organization
        first_name = ''
        last_name = ''
        email = ''
        engagement = Engagement.objects.filter(organization=p)
        if engagement:
            if engagement.person:
                first_name = person.first_name
                last_name = person.last_name
                email = person.email
        url = "%sp/project_edit/%s" % (settings.COOP_MEMBER_PROJECTS_URL, p.pk)
        projects_list.append({'title': p.title, 'first_name': first_name, 'last_name': last_name, 'email': email, 'url': url, 'status': p.get_status_display})

    # List all entries
    entries = CoopEntry.objects.exclude(status_moderation='V').order_by('-modification_date')
    for e in entries:
        first_name = ''
        last_name = ''
        email = ''
        url = "%sp/entry_edit/%s" % (settings.COOP_BLOG_URL, e.pk)
        first_name = e.author.first_name
        last_name = e.author.last_name
        email = e.author.email
        entries_list.append({'title': e.title, 'first_name': first_name, 'last_name': last_name, 'email': email, 'url': url, 'status': e.get_status_moderation_display})

    context = {'exchanges': exchanges_list, 'occ': occ_list, 'organizations': organizations_list, 'projects': projects_list, 'entries': entries_list}
    return render_to_response('admin/moderation.html', context, RequestContext(request))                       

