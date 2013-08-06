import json

from isodate import parse_date

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.views.generic.list import BaseListView

from .models import Organization


def to_isoformat(value):
    if value:
        return value.isoformat()


def to_float(value):
    if value:
        return float(value)


def to_dict(item, fields):
    result = {}

    for field, converter in fields.items():
        value = getattr(item, field)

        if converter:
            result[field] = converter(value)
        else:
            result[field] = value

    return result


def from_dict(item, data, fields):
    for field, setter in fields.items():
        if field in data:
            value = data[field]

            if setter:
                setter(item, value)
            else:
                setattr(item, field, value)


def address_to_dict(address):
    if address:
        return to_dict(address, {
            'uuid': None,
            'label': None,
            'adr1': None,
            'adr2': None,
            'zipcode': None,
            'city': None,
            'x_code': None,
            'country': None,
        })


def contact_to_dict(contact):
    if contact:
        return to_dict(contact, {
            'uuid': None,
            'content': None,
            'details': None,
        })


def list_of(func):
    return lambda items: [
        func(item)
        for item in items.all()
    ]


def member_to_dict(member):
    if member:
        return to_dict(member, {
            'uuid': None,
            'first_name': None,
            'last_name': None,
            'pref_email': contact_to_dict,
            'contacts': list_of(contact_to_dict),
        })


def get_field(field_name):
    def getter(obj):
        return getattr(obj, field_name, None)
    return getter


def legal_status_to_dict(legal_status):
    if legal_status:
        return to_dict(legal_status, {
            'slug': None,
            'label': None,
            'description': None,
        })


def organisation_to_dict(organisation):
    return to_dict(organisation, {
        'uuid': None,
        'title': None,
        'acronym': None,
        'short_description': None,
        'testimony': None,
        'annual_revenue': None,
        'workforce': to_float,
        'legal_status': legal_status_to_dict,
        'birth': to_isoformat,
        'pref_phone': get_field('uuid'),
        'pref_email': get_field('uuid'),
        'pref_address': address_to_dict,
        'web': None,
        'members': list_of(member_to_dict),
        'contacts': list_of(contact_to_dict),
    })


def attr_setter(name, func):
    def setter(item, value):
        setattr(item, name, func(value))
    return setter


def organisation_from_dict(organisation, data):
    from_dict(organisation, data, {
        'title': None,
        'acronym': None,
        'short_description': None,
        'testimony': None,
        'annual_revenue': None,
        'workforce': None,
        #'legal_status': attr_setter('legal_status', TODO),
        'birth': attr_setter('birth', parse_date),
        #'pref_phone': attr_setter('pref_phone', TODO),
        #'pref_email': attr_setter('pref_email', TODO),
        #'pref_address': attr_setter('pref_address', TODO),
        'web': None,
        #'members': attr_setter('members', TODO),
        #'contacts': attr_setter('contacts', TODO),
    })


class OrganistationListView(BaseListView):
    model = Organization

    def render_to_response(self, context):
        content = [
            organisation_to_dict(organisation)
            for organisation in context['object_list']
        ]
        return HttpResponse(json.dumps(content, indent=2),
                            content_type="application/json")


class OrganistationDetailView(View):

    def render_to_response(self, organisation):
        content = organisation_to_dict(organisation)
        return HttpResponse(json.dumps(content, indent=2),
                            content_type="application/json")

    def get(self, request, uuid):
        organisation = get_object_or_404(Organization, uuid=uuid)
        return self.render_to_response(organisation)

    def put(self, request, uuid):
        try:
            organisation = Organization.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            organisation = Organization()

        organisation_from_dict(organisation,
                               json.loads(request.body))
        organisation.save()

        return self.render_to_response(organisation)
