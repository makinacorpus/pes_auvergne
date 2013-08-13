from operator import attrgetter


def serialize(item, mapping):
    result = {}

    for field_name, func in mapping.items():
        value = getattr(item, field_name)

        if value and func:
            result[field_name] = func(value)
        else:
            result[field_name] = value

    return result


def to_isoformat(value):
    return value.isoformat()


def mapper(func):
    return lambda value: map(func, value.all())


def serialize_contact(contact):
    serialized = serialize(contact, {
        'uuid': None,
        'content': None,
        'content_object': attrgetter('uuid'),
    })
    serialized['content_type'] = contact.content_object.__class__.__name__
    return serialized


def serialize_location(location):
    return serialize(location, {
        'uuid': None,
        'label': None,
        'adr1': None,
        'adr2': None,
        'zipcode': None,
        'city': None,
        'x_code': None,
        'country': None,
    })


def serialize_organization(organization):
    return serialize(organization, {
        'uuid': None,
        'title': None,
        'acronym': None,
        'short_description': None,
        'testimony': None,
        'annual_revenue': None,
        'workforce': float,
        'legal_status': attrgetter('slug'),
        'birth': to_isoformat,
        'pref_phone': attrgetter('uuid'),
        'pref_email': attrgetter('uuid'),
        'pref_address': attrgetter('uuid'),
        'web': None,
        'members': mapper(attrgetter('uuid')),
        'contacts': mapper(attrgetter('uuid')),
    })


def serialize_person(person):
    return serialize(person, {
        'uuid': None,
        'first_name': None,
        'last_name': None,
        'pref_email': attrgetter('uuid'),
        'contacts': mapper(attrgetter('uuid')),
    })
