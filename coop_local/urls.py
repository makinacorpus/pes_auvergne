# -*- coding:utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

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
        csrf_exempt(OrganizationListView.as_view()),
        name="organization_list"),
    url(r'^api/organizations/(?P<uuid>.+)/$',
        csrf_exempt(OrganizationDetailView.as_view()),
        name="organization_detail"),

    url(r'^api/persons/$',
        csrf_exempt(PersonListView.as_view()),
        name="person_list"),
    url(r'^api/persons/(?P<uuid>.+)/$',
        csrf_exempt(PersonDetailView.as_view()),
        name="person_detail"),

    url(r'^api/locations/$',
        csrf_exempt(LocationListView.as_view()),
        name="location_list"),
    url(r'^api/locations/(?P<uuid>.+)/$',
        csrf_exempt(LocationDetailView.as_view()),
        name="location_detail"),

    url(r'^api/contacts/$',
        csrf_exempt(ContactListView.as_view()),
        name="organization_contact_list"),
    url(r'^api/contacts/(?P<uuid>.+)$',
        csrf_exempt(ContactDetailView.as_view()),
        name="organization_contact_list"),
)


from coop.default_project_urls import urlpatterns as default_project_urls
urlpatterns += default_project_urls
