from .serialize import serialize
from .deserialize import deserialize


def serialize_contact(contact):
    return {
        'uuid': contact.uuid,
        'content': contact.content,
    }


def serialize_organization(organization):
    return serialize(organization, include=(
        'uuid',
        'title',
        'acronym',
        'short_description',
        'testimony',
        'annual_revenue',
        'workforce',
        'legal_status',
        'birth',
        'pref_phone',
        'pref_email',
        'pref_address',
        'web',
        #'transverse_themes',
        'members',
    ), inline={
        'contacts': serialize_contact,
    })


def serialize_person(person):
    return serialize(person, include=(
        'uuid',
        'first_name',
        'last_name',
        'pref_email',
    ), inline={
        'contacts': serialize_contact,
    })


def serialize_location(location):
    return serialize(location, {
        'uuid',
        'label',
        'adr1',
        'adr2',
        'zipcode',
        'city',
        'country',
    })


def deserialize_contact(content_object, contact, data):
    deserialize(contact, data, include=(
        'uuid',
        'content',
    ))

    contact.content_object = content_object


def deserialize_organization(organization, data):
    return deserialize(organization, data, include=(
        'uuid',
        'title',
        'acronym',
        'short_description',
        'testimony',
        'annual_revenue',
        'workforce',
        'birth',
        'web',
        'transverse_themes',
    ))


def deserialize_person(person, data):
    return deserialize(person, data, include=(
        'uuid',
        'first_name',
        'last_name',
    ))
