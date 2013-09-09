import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView
)

from coop_local.models import (
    Contact,
    Organization,
    Person,
)

from .serializers import (
    deserialize_contact,
    deserialize_organization,
    deserialize_person,
    serialize_organization,
    serialize_person,
)


def json_response(content):
    return HttpResponse(json.dumps(content), content_type='application/json')


def get_or_create_object(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return model(**kwargs)


class BaseListView(ListView):

    def render_to_response(self, context):
        content = [
            self.serialize(instance)
            for instance in context['object_list']
        ]
        return json_response(content)


class BaseDetailView(DetailView):
    def update_contact(self, content_object, data):
        contact = get_or_create_object(Contact, uuid=data['uuid'])

        if contact.content_object and contact.content_object != content_object:
            raise Exception('Contact %s do not belong to %s %s' % (
                contact.uuid, type(content_object), content_object.uuid
            ))

        deserialize_contact(content_object, contact, data)
        contact.save()
        return contact

    def update_contacts(self, content_object, data):
        for contact_data in data:
            self.update_contact(content_object, contact_data)

    def is_old_contact(self, content_object, contact, contact_uuids):
        return (
            contact.uuid not in contact_uuids
            and contact.content_object == content_object
        )

    def delete_old_contacts(self, content_object, data):
        contact_uuids = [
            contact_data['uuid']
            for contact_data in data
        ]

        for contact in content_object.contacts.all():
            if self.is_old_contact(content_object, contact, contact_uuids):
                contact.delete()

    def update_pref(self, content_object, name, data):
        uuid = data.get(name)
        if uuid:
            contact = Contact.objects.get(uuid=uuid)
        else:
            contact = None
        setattr(content_object, name, contact)

    def get_object(self):
        uuid = self.kwargs.get('uuid', None)
        return get_object_or_404(self.model, uuid=uuid)

    def get_or_create_object(self):
        uuid = self.kwargs.get('uuid', None)
        return get_or_create_object(self.model, uuid=uuid)

    def render_to_response(self, context):
        content = self.serialize(context['object'])
        return json_response(content)


class OrganizationView(object):
    model = Organization
    serialize = staticmethod(serialize_organization)


class OrganizationListView(OrganizationView, BaseListView):
    pass


class OrganizationDetailView(OrganizationView, BaseDetailView):

    def update_organization(self, organization, data):
        deserialize_organization(organization, data)
        organization.save()
        self.update_contacts(organization, data.get('contacts', []))
        self.update_pref(organization, 'pref_email', data)
        self.update_pref(organization, 'pref_phone', data)

        organization.save()

    def create(self, organization, data):
        self.update_organization(organization, data)

    def update(self, organization, data):
        self.update_organization(organization, data)
        self.delete_old_contacts(organization, data.get('contacts', []))

    def put(self, request, *args, **kwargs):
        self.object = self.get_or_create_object()
        data = json.loads(self.request.body)
        if self.object.pk:
            self.update(self.object, data)
        else:
            self.create(self.object, data)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PersonView(object):
    model = Person
    serialize = staticmethod(serialize_person)


class PersonListView(PersonView, BaseListView):
    pass


class PersonDetailView(PersonView, BaseDetailView):

    def update_person(self, person, data):
        deserialize_person(person, data)
        person.save()
        self.update_contacts(person, data.get('contacts', []))
        self.update_pref(person, 'pref_email', data)

        person.save()

    def create(self, person, data):
        self.update_person(person, data)

    def update(self, person, data):
        self.update_person(person, data)
        self.delete_old_contacts(person, data.get('contacts', []))

    def put(self, request, *args, **kwargs):
        self.object = self.get_or_create_object()
        data = json.loads(self.request.body)
        if self.object.pk:
            self.update(self.object, data)
        else:
            self.create(self.object, data)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
