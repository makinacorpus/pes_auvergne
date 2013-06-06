# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from coop_local.models import Organization
from django.utils.translation import ugettext_lazy as _
from coop.org.admin import OrganizationAdminForm
from tinymce.widgets import AdminTinyMCE

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
                       'transmission_date', 'authors', 'validation']
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

admin.site.register(Organization, MyOrganizationAdmin)
