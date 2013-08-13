# -*- coding:utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from .api import (
    ContactDetailView,
    ContactListView,
    LocationDetailView,
    LocationListView,
    OrganizationDetailView,
    OrganizationListView,
    PersonDetailView,
    PersonListView,
)

# # https://code.djangoproject.com/ticket/10405#comment:11
# from django.db.models.loading import cache as model_cache
# if not model_cache.loaded:
#     model_cache.get_models()

admin.autodiscover()


# Add you own URLs here
urlpatterns = patterns(
    '',
    url(r'^api/organizations/$',
        OrganizationListView.as_view(),
        name="organization_list"),
    url(r'^api/organizations/(?P<uuid>.+)/$',
        OrganizationDetailView.as_view(),
        name="organization_detail"),

    url(r'^api/persons/$',
        PersonListView.as_view(),
        name="person_list"),
    url(r'^api/persons/(?P<uuid>.+)/$',
        PersonDetailView.as_view(),
        name="person_detail"),

    url(r'^api/locations/$',
        LocationListView.as_view(),
        name="location_list"),
    url(r'^api/locations/(?P<uuid>.+)/$',
        LocationDetailView.as_view(),
        name="location_detail"),

    url(r'^api/contacts/$',
        ContactListView.as_view(),
        name="organization_contact_list"),
    url(r'^api/contacts/(?P<uuid>.+)$',
        ContactDetailView.as_view(),
        name="organization_contact_list"),
)


from coop.default_project_urls import urlpatterns as default_project_urls
urlpatterns += default_project_urls
