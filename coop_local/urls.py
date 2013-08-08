# -*- coding:utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from .api import (
    OrganizationListView,
    OrganizationDetailView,
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
)


from coop.default_project_urls import urlpatterns as default_project_urls
urlpatterns += default_project_urls
