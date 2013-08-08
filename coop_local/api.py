import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from .models import Organization
from .serializers import (
    #serialize_contact,
    #serialize_location,
    serialize_organization,
    #serialize_person,
)


class ApiListView(BaseListView):

    def render_to_response(self, context):
        content = map(self.serialize, context['object_list'])
        return HttpResponse(json.dumps(content, indent=2),
                            content_type="application/json")


class ApiDetailView(BaseDetailView):

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid', '')
        return get_object_or_404(self.model, uuid=uuid)

    def render_to_response(self, context):
        content = self.serialize(context['object'])
        return HttpResponse(json.dumps(content, indent=2),
                            content_type="application/json")


class OrganizationListView(ApiListView):
    model = Organization
    serialize = staticmethod(serialize_organization)


class OrganizationDetailView(ApiDetailView):
    model = Organization
    serialize = staticmethod(serialize_organization)
