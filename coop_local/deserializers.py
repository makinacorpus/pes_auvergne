from decimal import Decimal

from isodate import parse_date

from .models import (
    Contact,
    Location,
    Organization,
    Person,
)


def deserialize(obj, data, mapping):
    #print('%s %s deserialize' % (obj.__class__.__name__, data['uuid']))

    for field_name, setter in mapping.items():
        if field_name in data:
            value = data[field_name]

            if value is not None and setter:
                setter(obj, field_name, value)
            else:
                setattr(obj, field_name, value)

    return obj


def setter(func):
    def setter(obj, field_name, value):
        setattr(obj, field_name, func(value))
    return setter


def field_setter(source_field_name):
    def setter(obj, field_name, value):
        field = obj._meta.get_field(field_name)
        model = field.related.parent_model
        related_object = model.objects.get(**{source_field_name: value})
        setattr(obj, field_name, related_object)
    return setter


def field_list_setter(source_field_name):
    def setter(obj, field_name, values):
        field = obj._meta.get_field(field_name)
        model = field.related.parent_model
        related_objects = model.objects.filter(**{
            '%s__in' % source_field_name: values
        })
        setattr(obj, field_name, related_objects)
    return setter


def deserialize_contact(data):
    return deserialize(Contact(), data, {
        'uuid': None,
        'content': None,
        'details': None,
    })


def deserialize_location(data):
    return deserialize(Location(), data, {
        'uuid': None,
        'label': None,
        'adr1': None,
        'adr2': None,
        'zipcode': None,
        'city': None,
        'x_code': None,
        'country': None,
    })


def deserialize_person(data):
    person = Person()
    person.username = data['uuid']
    return deserialize(person, data, {
        'uuid': None,
        'first_name': None,
        'last_name': None,
    })


def deserialize_organization(data):
    return deserialize(Organization(), data, {
        'uuid': None,
        'title': None,
        'acronym': None,
        'short_description': None,
        'testimony': None,
        'annual_revenue': None,
        'workforce': setter(Decimal),
        'legal_status': field_setter('slug'),
        'birth': setter(parse_date),
        'web': None,
    })
