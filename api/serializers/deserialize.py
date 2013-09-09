import dateutil

from django.db import models

from .common import (
    has_type_handler,
    get_type_handler,
)


def datetime_handler(instance, field, value):
    if value:
        setattr(instance, field.name, dateutil.parser.parse(value))
    else:
        setattr(instance, field.name, None)


def date_handler(instance, field, value):
    if value:
        setattr(instance, field.name, dateutil.parser.parse(value).date())
    else:
        setattr(instance, field.name, None)


def time_handler(instance, field, value):
    if value:
        setattr(instance, field.name, dateutil.parser.parse(value).time())
    else:
        setattr(instance, field.name, None)


field_type_handlers = {
    models.DateTimeField: datetime_handler,
    models.DateField: date_handler,
    models.TimeField: time_handler,
}


def deserialize(instance, data, include):
    included = [
        (key, value)
        for key, value in data.items()
        if key in include
    ]

    for key, value in included:
        field, _, _, _ = instance._meta.get_field_by_name(key)

        if has_type_handler(field, field_type_handlers):
            handler = get_type_handler(field, field_type_handlers)
            handler(instance, field, value)
        else:
            setattr(instance, key, value)
