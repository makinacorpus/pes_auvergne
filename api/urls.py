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
    TransverseThemeListView,
    LegalStatusListView,
    ActivityNomenclatureListView,
    EventCategoryListView,
    EventListView,
    CalendarListView,
    help_view,
)

urlpatterns = patterns(
    '',
    url(r'^$', help_view),
    url(r'^organizations/$', OrganizationListView.as_view()),
    url(r'^organizations/(?P<uuid>\w+)/',
        csrf_exempt(OrganizationDetailView.as_view())),
    url(r'^persons/$', PersonListView.as_view()),
    url(r'^persons/(?P<uuid>\w+)/',
        csrf_exempt(PersonDetailView.as_view())),
    url(r'^roles/$', RoleListView.as_view()),
    url(r'^transverse_themes/$', TransverseThemeListView.as_view()),
    url(r'^legal_statuses/$', LegalStatusListView.as_view()),
    url(r'^activity_nomenclatures/$', ActivityNomenclatureListView.as_view()),
    url(r'^event_categories/$', EventCategoryListView.as_view()),
    url(r'^events/$', EventListView.as_view()),
    url(r'^calendars/$', CalendarListView.as_view()),
)
