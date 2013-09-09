import dateutil

from django.db import models

from coop_local.models import (
    Person,
    TransverseTheme,
)

from .common import (
    has_type_handler,
    get_type_handler,
)


def get_by_id(model, value):
    return model.objects.get(id=value)


def get_by_uuid(model, value):
    return model.objects.get(uuid=value)


many_to_many_handlers = {
    Person: get_by_uuid,
    TransverseTheme: get_by_id,
}


def many_to_many_handler(instance, field, values):
    model = field.related.parent_model
    handler = get_type_handler(model, many_to_many_handlers)
    values = []
    for value in values:
        values.append(handler(model, value))
    return values


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
    models.ManyToManyField: many_to_many_handler,
}


def deserialize(instance, data, include=None, handlers=None):
    included = [
        (key, value)
        for key, value in data.items()
        if key in include
    ]

    for key, value in included:
        field, _, _, _ = instance._meta.get_field_by_name(key)

        if handlers and field.name in handlers:
            handler = handlers[field.name]
            setattr(instance, key, handler(value))
        elif has_type_handler(field, field_type_handlers):
            type_handler = get_type_handler(field, field_type_handlers)
            type_handler(instance, field, value)
        else:
            setattr(instance, key, value)
