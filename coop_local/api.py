import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from .models import (
    Contact,
    Engagement,
    Location,
    Organization,
    Person,
)
from .serializers import (
    serialize_contact,
    serialize_location,
    serialize_organization,
    serialize_person,
)
from .deserializers import (
    deserialize_contact,
    deserialize_location,
    deserialize_organization,
    deserialize_person,
)


class ApiListView(BaseListView):

    def render_to_response(self, context):
        content = map(self.serialize, context['object_list'])
        return HttpResponse(json.dumps(content, indent=2),
                            content_type="application/json")

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if 'uuid' in data and self.model.objects.get(uuid=data['uuid']):
            raise Exception('UUID %s alredy exists' % data['uuid'])

        obj = self.deserialize(self.model(), data)
        content = self.serialize(obj)
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

    def deserialize(self, obj, data):
        obj = deserialize_organization(obj, data)

        if data.get('pref_email'):
            obj.pref_email = Contact.objects.get(
                uuid=data['pref_email']
            )

        if data.get('pref_phone'):
            obj.pref_phone = Contact.objects.get(
                uuid=data['pref_phone']
            )

        obj.save()

        members = Person.objects.filter(uuid__in=data['members']).all()
        engagements = []
        for person in members:
            engagements.append(Engagement(
                organization=obj,
                person=person
            ))
        Engagement.objects.bulk_create(engagements)

        return obj


class OrganizationDetailView(ApiDetailView):
    model = Organization
    serialize = staticmethod(serialize_organization)


class ContactListView(ApiListView):
    model = Contact
    serialize = staticmethod(serialize_contact)
    content_types = {
        'Person': Person,
        'Organization': Organization
    }

    def deserialize(self, obj, data):
        obj = deserialize_contact(obj, data)
        content_type_model = self.content_types[data['content_type']]
        content_object = content_type_model.objects.get(
            uuid=data['content_object']
        )
        obj.content_object = content_object

        obj.save()
        return obj


class ContactDetailView(ApiDetailView):
    model = Contact
    serialize = staticmethod(serialize_contact)


class PersonListView(ApiListView):
    model = Person
    serialize = staticmethod(serialize_person)

    def deserialize(self, obj, data):
        obj = deserialize_person(obj, data)

        if data.get('pref_email'):
            obj.pref_email = Contact.objects.filter(
                uuid=data['pref_email']
            ).get()

        obj.save()
        return obj


class PersonDetailView(ApiDetailView):
    model = Person
    serialize = staticmethod(serialize_person)


class LocationListView(ApiListView):
    model = Location
    serialize = staticmethod(serialize_location)

    def deserialize(self, obj, data):
        obj = deserialize_location(obj, data)
        obj.save()
        return obj


class LocationDetailView(ApiDetailView):
    model = Location
    serialize = staticmethod(serialize_location)
