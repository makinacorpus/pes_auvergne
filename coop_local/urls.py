# -*- coding:utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from .api import OrganistationListView, OrganistationDetailView

# # https://code.djangoproject.com/ticket/10405#comment:11
# from django.db.models.loading import cache as model_cache
# if not model_cache.loaded:
#     model_cache.get_models()

admin.autodiscover()


# Add you own URLs here
urlpatterns = patterns(
    '',
    url(r'^api/organisations/$',
        OrganistationListView.as_view(),
        name="organistations_list"),
    url(r'^api/organisations/(?P<uuid>.+)/$',
        csrf_exempt(OrganistationDetailView.as_view()),
        name="organistations_detail"),
)


from coop.default_project_urls import urlpatterns as default_project_urls
urlpatterns += default_project_urls
