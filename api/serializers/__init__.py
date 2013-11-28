from coop.exchange.models import (
    EWAY,
    ETYPE,
)

from coop_local.models import (
    Engagement,
)

from .serialize import serialize
from .deserialize import deserialize


def serialize_contact(contact):
    return {
        'contact_medium': contact.contact_medium_id,
        'uuid': contact.uuid,
        'content': contact.content,
        'details': contact.details,
    }


def serialize_contact_medium(contact_medium):
    return {
        'id': contact_medium.id,
        'label': contact_medium.label,
    }


def serialize_organization(organization):
    serialized = serialize(organization, include=(
        'uuid',
        'title',
        'acronym',
        'short_description',
        'description',
        'testimony',
        'annual_revenue',
        'workforce',
        'legal_status',
        'birth',
        'pref_phone',
        'pref_email',
        'pref_address',
        'web',
        'transverse_themes',
    ), inline={
        'contacts': serialize_contact,
    })
    serialized['members'] = []
    for engagement in Engagement.objects.filter(organization=organization):
        serialized['members'].append({
            'person': engagement.person.uuid,
            'role': getattr(engagement.role, 'uuid', None),
            'role_detail': engagement.role_detail,
        })
    return serialized


def serialize_person(person):
    return serialize(person, include=(
        'uuid',
        'first_name',
        'last_name',
        'pref_email',
    ), inline={
        'contacts': serialize_contact,
    })


def serialize_role(role):
    return serialize(role, include=(
        'uuid',
        'slug',
        'label',
    ))


def serialize_transverse_theme(transverse_theme):
    return serialize(transverse_theme, include=(
        'id',
        'name',
    ))


def serialize_legal_status(legal_status):
    return serialize(legal_status, include=(
        'slug',
        'label',
    ))


def serialize_activity_nomenclature(activity_nomenclature):
    return serialize(activity_nomenclature, include=(
        'id',
        'label',
    ))


def serialize_calendar(calendar):
    return serialize(calendar, include=(
        'uuid',
        'title',
        'description',
    ))


def deserialize_calendar(calendar, data):
    deserialize(calendar, data, include=(
        'uuid',
        'title',
        'description',
    ))


def serialize_event_category(event_category):
    return serialize(event_category, include=(
        'id',
        'slug',
        'label',
    ))


def serialize_event(event):
    return serialize(event, include=(
        'uuid',
        'title',
        'description',
        'category',
        'calendar',
        'organization',
        'organizations',
        'other_organizations',
        'activity',
        'transverse_themes',
        'source_info',
        'zoom_on',
    ))


def deserialize_contact(content_object, contact, data):
    deserialize(contact, data, include=(
        'uuid',
        'content',
    ))

    contact.content_object = content_object


def deserialize_organization(organization, data):
    deserialize(organization, data, include=(
        'uuid',
        'title',
        'acronym',
        'short_description',
        'description',
        'testimony',
        'annual_revenue',
        'workforce',
        'birth',
        'web',
    ))


def deserialize_person(person, data):
    deserialize(person, data, include=(
        'uuid',
        'first_name',
        'last_name',
    ))


def deserialize_event(event, data):
    deserialize(event, data, include=(
        'uuid',
        'title',
        'description',
        'other_organizations',
        'source_info',
        'zoom_on',
    ))


def serialize_exchange_method(exchange_method):
    result = serialize(exchange_method, include=(
        'id',
        'label',
        'etypes',
    ))
    result['etypes'] = [
        ETYPE.REVERTED_CHOICES_CONST_DICT[int(etype)]
        for etype in exchange_method.etypes
    ]
    return result


def serialize_exchange(exchange):
    result = serialize(exchange, include=(
        'uuid',
        'title',
        'description',
        'organization',
        'person',
        'permanent',
        'expiration',
        'products',
        'activity',
    ))
    result['eway'] = EWAY.REVERTED_CHOICES_CONST_DICT[int(exchange.eway)]
    result['etype'] = ETYPE.REVERTED_CHOICES_CONST_DICT[exchange.etype]
    return result


def deserialize_exchange(exchange, data):
    deserialize(exchange, data, include=(
        'uuid',
        'title',
        'description',
        'eway',
        'etype',
        'permanent',
        'expiration',
    ))
    exchange.eway = EWAY.CHOICES_CONST_DICT[data['eway']]
    exchange.etype = ETYPE.CHOICES_CONST_DICT[data['etype']]


def serialize_product(product):
    result = serialize(product, include=(
        'uuid',
        'title',
        'description',
        'organization',
    ))
    return result


def deserialize_product(product, data):
    deserialize(product, data, include=(
        'uuid',
        'title',
        'description',
    ))
