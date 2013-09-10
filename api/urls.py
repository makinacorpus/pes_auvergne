# -*- coding:utf-8 -*-
from django.conf.urls.defaults import (
    patterns,
    url,
)
from django.views.decorators.csrf import csrf_exempt

from .views import (
    OrganizationDetailView,
    OrganizationListView,
    PersonDetailView,
    PersonListView,
    RoleListView,
)

urlpatterns = patterns(
    '',
    url(r'^organizations/$', OrganizationListView.as_view()),
    url(r'^organizations/(?P<uuid>\w+)/',
        csrf_exempt(OrganizationDetailView.as_view())),
    url(r'^persons/$', PersonListView.as_view()),
    url(r'^persons/(?P<uuid>\w+)/',
        csrf_exempt(PersonDetailView.as_view())),
    url(r'^roles/$', RoleListView.as_view()),
)
