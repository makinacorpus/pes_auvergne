from datetime import datetime, date, time
from decimal import Decimal

from django.db import models


def get_uuid_or_slug_or_id(obj):
    if hasattr(obj, 'uuid'):
        return obj.uuid
    if hasattr(obj, 'slug'):
        return obj.slug
    if hasattr(obj, 'pk'):
        return obj.pk
    else:
        raise Exception('%s %s', type(obj), dir(obj))


def filter_fields(fields, include, inline):
    return [
        field
        for field in fields
        if field.name in include or field.name in inline
    ]


def serialize_local_field(field, value, handler=None):
    if value is None:
        return None
    elif isinstance(value, models.FileField):
        pass
    elif isinstance(value, (datetime, date, time)):
        return value.isoformat()
    elif isinstance(value, Decimal):
        return float(value)
    elif isinstance(field, models.ForeignKey):
        if handler:
            return handler(value)
        return get_uuid_or_slug_or_id(value)
    else:
        return value


def serialize(instance, include=None, inline=None):
    serialized = {}

    if include is None:
        include = instance._meta.get_all_field_names()

    if inline is None:
        inline = {}

    local_fields = filter_fields(instance._meta.local_fields,
                                 include,
                                 inline.keys())

    local_many_to_many = filter_fields(instance._meta.local_many_to_many,
                                       include,
                                       inline.keys())

    for field in local_fields:
        value = getattr(instance, field.name, None)
        handler = inline.get(field.name)
        serialized[field.name] = serialize_local_field(field, value, handler)

    for field in local_many_to_many:
        queryset = getattr(instance, field.name)
        if field.name in inline:
            handler = inline[field.name]
        else:
            handler = get_uuid_or_slug_or_id

        serialized[field.name] = [
            handler(related)
            for related in queryset.all()
        ]

    return serialized
