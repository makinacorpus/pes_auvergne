# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from coop_local.models import Organization
from django.utils.translation import ugettext_lazy as _

try:
    from coop.base_admin import *
except ImportError, exp:
    raise ImproperlyConfigured("Unable to find coop/base_admin.py file")

admin.site.unregister(Organization)
class MyOrganizationAdmin(OrganizationAdmin):
    list_display = ('logo_list_display', 'label', 'id', 'active', 'has_description', 'has_location')
    fieldsets = (
        ('Identité', {
            'fields': ('is_project', 'logo', 'title', ('acronym', 'pref_label'), 'subtitle', ('birth', 'active',),
                        'web')
            }),
        ('Description', {
            'fields': ('short_description', 'description', 'category', 'tags', ('statut', 'secteur_fse'), ('siret', 'naf'), 'transverse_themes')
            }),

        ('Préférences', {
            #'classes': ('collapse',),
            'fields': ('pref_email', 'pref_phone', 'pref_address', 'notes',)
            }),
        (_(u'Testimony'), {
            'fields': ['testimony',]
            }),
    )

admin.site.register(Organization, MyOrganizationAdmin)

