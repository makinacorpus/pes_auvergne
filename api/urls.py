# -*- coding:utf-8 -*-
from django.conf.urls.defaults import (
    patterns,
    url,
)
from django.views.decorators.csrf import csrf_exempt

from .views import (
    ActivityNomenclatureListView,
    CalendarListView,
    ContactMediumListView,
    EventCategoryListView,
    EventDetailView,
    EventListView,
    ExchangeDetailView,
    ExchangeListView,
    ExchangeMethodListView,
    help_view,
    LegalStatusListView,
    OrganizationDetailView,
    OrganizationListView,
    PersonDetailView,
    PersonListView,
    ProductDetailView,
    ProductListView,
    RoleListView,
    TransverseThemeListView,
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
    url(r'^events/(?P<uuid>\w+)/',
        csrf_exempt(EventDetailView.as_view())),
    url(r'^calendars/$', CalendarListView.as_view()),
    url(r'^contact_medium/$', ContactMediumListView.as_view()),
    url(r'^exchange_methods/$', ExchangeMethodListView.as_view()),
    url(r'^exchanges/$', ExchangeListView.as_view()),
    url(r'^exchanges/(?P<uuid>\w+)/',
        csrf_exempt(ExchangeDetailView.as_view())),
    url(r'^products/$', ProductListView.as_view()),
    url(r'^products/(?P<uuid>\w+)/',
        csrf_exempt(ProductDetailView.as_view())),
)
