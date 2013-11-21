# encoding: utf-8

import json

from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied
)
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    render
)
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView,
    DetailView
)

from coop.exchange.models import (
    EWAY,
    ETYPE,
)

from coop_local.models import (
    DeletedURI,
    ActivityNomenclature,
    Calendar,
    Contact,
    ContactMedium,
    Engagement,
    Event,
    EventCategory,
    Exchange,
    ExchangeMethod,
    LegalStatus,
    Organization,
    Person,
    Product,
    Role,
    TransverseTheme,
)

from .serializers import (
    deserialize_calendar,
    deserialize_contact,
    deserialize_event,
    deserialize_exchange,
    deserialize_organization,
    deserialize_person,
    deserialize_product,
    serialize_activity_nomenclature,
    serialize_calendar,
    serialize_contact_medium,
    serialize_event,
    serialize_event_category,
    serialize_exchange,
    serialize_exchange_method,
    serialize_legal_status,
    serialize_organization,
    serialize_person,
    serialize_product,
    serialize_role,
    serialize_transverse_theme,
)

from .models import (
    ApiKey,
    ApiPermissions
)


def json_response(content, status=200):
    return HttpResponse(json.dumps(content),
                        content_type='application/json',
                        status=status)


def json_401_response(message):
    return HttpResponse(
        json.dumps({
            'error': message
        }),
        content_type='application/json',
        status=401)


def require_api_key(method):

    def wrapper(view, request, *args, **kwargs):
        api_key = request.REQUEST.get('api_key')
        if api_key is None:
            return json_401_response('No api_key provided')

        try:
            ApiKey.objects.get(key=api_key)
        except ObjectDoesNotExist:
            return json_401_response('Unknow api_key %s' % api_key)

        return method(view, request, *args, **kwargs)

    return wrapper


def create_api_permission(method):

    def wrapper(view, instance, data):
        method(view, instance, data)
        api_key = ApiKey.objects.get(key=view.request.REQUEST['api_key'])
        permission = ApiPermissions(object_type=str(type(instance)),
                                    object_id=instance.id,
                                    api_key=api_key)
        permission.save()

    return wrapper


def get_permision_or_deny(api_key, instance):
    try:
        return ApiPermissions.objects.get(
            object_type=str(type(instance)),
            object_id=instance.id,
            api_key__key=api_key
        )
    except ObjectDoesNotExist:
        raise PermissionDenied()


def require_api_permission(method):

    def wrapper(view, instance, data):
        if instance.pk:
            get_permision_or_deny(view.request.REQUEST['api_key'], instance)
        method(view, instance, data)

    return wrapper


def get_or_create_object(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return model(**kwargs)


def update_transverse_themes(instance, data):
    if 'transverse_themes' in data:
        ids = data['transverse_themes']
        manager = TransverseTheme.objects
        instance.transverse_themes = manager.filter(id__in=ids).all()


def help_view(request):
    return render(request, 'api/help.html', {
        'exchange_ways': [
            (eway_const, EWAY.CHOICES_DICT[eway_id])
            for eway_const, eway_id in EWAY.CHOICES_CONST_DICT.items()
        ],
        'exchange_types': [
            (etype_const, ETYPE.CHOICES_DICT[etype_id])
            for etype_const, etype_id in ETYPE.CHOICES_CONST_DICT.items()
        ],
    })


class BaseListView(ListView):

    def render_to_response(self, context):
        content = [
            self.serialize(instance)
            for instance in context['object_list']
        ]
        return json_response(content)


class HasContactsView(object):
    def update_contact(self, content_object, data):
        contact = get_or_create_object(Contact, uuid=data['uuid'])
        deserialize_contact(content_object, contact, data)
        contact.save()
        return contact

    def update_contacts(self, content_object, data):
        if 'contacts' in data:
            for contact_data in data['contacts']:
                self.update_contact(content_object, contact_data)

    def is_old_contact(self, content_object, contact, current_contacts_uuid):
        return (
            contact.uuid not in current_contacts_uuid
            and contact.content_object == content_object
        )

    def delete_all_contacts(self, content_object):
        self.object.contacts.filter().delete()

    def delete_old_contacts(self, content_object, data):
        current_contacts_uuid = [
            contact['uuid']
            for contact in data.get('contacts', [])
        ]

        for contact in content_object.contacts.all():
            if self.is_old_contact(content_object,
                                   contact,
                                   current_contacts_uuid):
                contact.delete()

    def update_pref(self, content_object, name, data):
        if name in data:
            uuid = data[name]
            if uuid:
                contact = Contact.objects.get(uuid=uuid)
            else:
                contact = None
            setattr(content_object, name, contact)


class BaseDetailView(DetailView):

    @classmethod
    def as_view(cls, **initkwargs):
        return csrf_exempt(super(BaseDetailView, cls).as_view(**initkwargs))

    def get_object(self):
        uuid = self.kwargs.get('uuid', None)
        return get_object_or_404(self.model, uuid=uuid)

    def get_or_create_object(self):
        uuid = self.kwargs.get('uuid', None)
        return get_or_create_object(self.model, uuid=uuid)

    def render_to_response(self, context):
        content = self.serialize(context['object'])
        return json_response(content)

    @require_api_key
    def put(self, request, *args, **kwargs):
        self.object = self.get_or_create_object()
        data = json.loads(self.request.body)
        if self.object.pk:
            self.update(self.object, data)
        else:
            self.create(self.object, data)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    @create_api_permission
    def create(self, instance, data):
        self._save(instance, data)

    @require_api_permission
    def update(self, instance, data):
        self._save(instance, data)
        self.after_update(instance, data)

    def after_update(self, instance, data):
        pass

    def before_delete(self, instance):
        pass

    @require_api_key
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        permission = get_permision_or_deny(request.REQUEST['api_key'],
                                           instance)

        self.before_delete(instance)
        DeletedURI.objects.filter(uuid=instance.uuid).delete()
        instance.delete()
        permission.delete()

        return json_response({})

    def _save(self, instance, data):
        self.deserialize(instance, data)
        instance.save()


class OrganizationView(HasContactsView):
    model = Organization
    serialize = staticmethod(serialize_organization)
    deserialize = staticmethod(deserialize_organization)


class OrganizationListView(OrganizationView, BaseListView):
    pass


class OrganizationDetailView(OrganizationView, BaseDetailView):

    def delete_old_engagements(self, organization):
        Engagement.objects.filter(organization=organization).delete()

    def create_engagement(self, organization, data):
        person = Person.objects.get(uuid=data['person'])
        role = Role.objects.get(uuid=data['role'])

        engagement = Engagement(organization=organization,
                                person=person,
                                role=role,
                                role_detail=data.get('role_detail', ''))
        engagement.save()

    def update_members(self, organization, data):
        if 'members' in data:
            self.delete_old_engagements(organization)

            for engagement_data in data['members']:
                self.create_engagement(organization, engagement_data)

    def _save(self, organization, data):
        self.deserialize(organization, data)
        organization.save()
        self.update_contacts(organization, data)
        self.update_pref(organization, 'pref_email', data)
        self.update_pref(organization, 'pref_phone', data)
        update_transverse_themes(organization, data)
        self.update_members(organization, data)
        organization.save()

    def after_update(self, organization, data):
        self.delete_old_contacts(organization, data)

    def before_delete(self, organization):
        self.delete_all_contacts(organization)


class PersonView(HasContactsView):
    model = Person
    serialize = staticmethod(serialize_person)
    deserialize = staticmethod(deserialize_person)


class PersonListView(PersonView, BaseListView):
    pass


class PersonDetailView(PersonView, BaseDetailView):

    def _save(self, person, data):
        self.deserialize(person, data)
        person.save()
        self.update_contacts(person, data)
        self.update_pref(person, 'pref_email', data)
        person.save()

    def after_update(self, person, data):
        self.delete_old_contacts(person, data)

    def before_delete(self, person):
        self.delete_all_contacts(person)


class RoleListView(BaseListView):
    model = Role
    serialize = staticmethod(serialize_role)


class TransverseThemeListView(BaseListView):
    model = TransverseTheme
    serialize = staticmethod(serialize_transverse_theme)


class LegalStatusListView(BaseListView):
    model = LegalStatus
    serialize = staticmethod(serialize_legal_status)


class ActivityNomenclatureListView(BaseListView):
    model = ActivityNomenclature
    serialize = staticmethod(serialize_activity_nomenclature)


class CalendarView(object):
    model = Calendar
    serialize = staticmethod(serialize_calendar)
    deserialize = staticmethod(deserialize_calendar)


class CalendarDetailView(CalendarView, BaseDetailView):
    pass


class CalendarListView(CalendarView, BaseListView):
    pass


class EventCategoryListView(BaseListView):
    model = EventCategory
    serialize = staticmethod(serialize_event_category)


class EventView(object):
    model = Event
    serialize = staticmethod(serialize_event)
    deserialize = staticmethod(deserialize_event)


class EventListView(EventView, BaseListView):
    pass


class EventDetailView(EventView, BaseDetailView):

    def set_calendar(self, event, data):
        if 'calendar' in data:
            event.calendar = Calendar.objects\
                .get(uuid=data['calendar'])

    def set_category(self, event, data):
        if 'category' in data:
            event.category = EventCategory.objects\
                .filter(slug__in=data['category']).all()

    def set_activity(self, event, data):
        if 'activity' in data:
            event.activity = ActivityNomenclature.objects\
                .get(id=data['activity'])

    def set_organization(self, event, data):
        if 'organization' in data:
            event.organization = Organization.objects\
                .get(uuid=data['organization'])

    def set_organizations(self, event, data):
        if 'organizations' in data:
            event.organizations = Organization.objects\
                .filter(uuid__in=data['organizations']).all()

    def _save(self, event, data):
        self.deserialize(event, data)
        self.set_calendar(event, data)
        event.save()
        self.set_category(event, data)
        self.set_activity(event, data)
        self.set_organization(event, data)
        self.set_organizations(event, data)
        update_transverse_themes(event, data)
        event.save()


class ContactMediumListView(BaseListView):
    model = ContactMedium
    serialize = staticmethod(serialize_contact_medium)


class ExchangeMethodListView(BaseListView):
    model = ExchangeMethod
    serialize = staticmethod(serialize_exchange_method)


class ExchangeView(object):
    model = Exchange
    serialize = staticmethod(serialize_exchange)
    deserialize = staticmethod(deserialize_exchange)


class ExchangeListView(ExchangeView, BaseListView):
    pass


class ExchangeDetailView(ExchangeView, BaseDetailView):

    def _save(self, exchange, data):
        self.deserialize(exchange, data)
        exchange.save()

        if 'products' in data:
            exchange.products = Product.objects\
                .filter(uuid__in=data['products']).all()

        if 'methods' in data:
            exchange.methods = ExchangeMethod.objects\
                .filter(id__in=data['methods']).all()

        if 'activity' in data:
            exchange.activity = ActivityNomenclature.objects\
                .get(id=data['activity'])

        if 'organization' in data:
            exchange.organization = Organization.objects\
                .get(uuid=data['organization'])

        if 'person' in data:
            exchange.person = Person.objects\
                .get(uuid=data['person'])

        exchange.save()


class ProductView(object):
    model = Product
    serialize = staticmethod(serialize_product)
    deserialize = staticmethod(deserialize_product)


class ProductListView(ProductView, BaseListView):
    pass


class ProductDetailView(ProductView, BaseDetailView):

    def _save(self, product, data):
        self.deserialize(product, data)

        if 'organization' in data:
            product.organization = Organization.objects\
                .get(uuid=data['organization'])

        product.save()
