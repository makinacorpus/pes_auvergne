# -*- coding:utf-8 -*-
from django.conf.urls.defaults import (
    include,
    patterns,
    url,
)
from django.contrib import admin

from . import utils

# # https://code.djangoproject.com/ticket/10405#comment:11
# from django.db.models.loading import cache as model_cache
# if not model_cache.loaded:
#     model_cache.get_models()

admin.autodiscover()

# Add you own URLs here
urlpatterns = patterns(
    '',
    url(r'^api/', include('api.urls')),
    url(r'^mailto/', utils.mail_to_friend, name='mail_to_friend'),
    
    #url(r'^accounts/', include('registration.auth_urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    
)

from coop.default_project_urls import urlpatterns as default_project_urls
urlpatterns += default_project_urls


