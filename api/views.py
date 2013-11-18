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
from django.views.generic import (
    ListView,
    DetailView
)

from coop_local.models import (
    ActivityNomenclature,
    Calendar,
    Contact,
    ContactMedium,
    Engagement,
    Event,
    EventCategory,
    LegalStatus,
    Organization,
    Person,
    Role,
    TransverseTheme,
)

from .serializers import (
    deserialize_contact,
    deserialize_event,
    deserialize_organization,
    deserialize_person,
    serialize_activity_nomenclature,
    serialize_calendar,
    serialize_contact_medium,
    serialize_event,
    serialize_event_category,
    serialize_legal_status,
    serialize_organization,
    serialize_person,
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
        permission = ApiPermissions(resource_key=instance.pk, api_key=api_key)
        permission.save()

    return wrapper


def require_api_permission(method):

    def wrapper(view, instance, data):
        api_key = view.request.REQUEST['api_key']
        if instance.pk:
            try:
                ApiPermissions.objects.get(resource_key=instance.pk,
                                           api_key__key=api_key)
            except ObjectDoesNotExist:
                raise PermissionDenied()
        method(view, instance, data)

    return wrapper


def get_or_create_object(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return model(**kwargs)


def help_view(request):
    return render(request, 'api/help.html')


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

    def is_old_contact(self, content_object, contact, contact_uuids):
        return (
            contact.uuid not in contact_uuids
            and contact.content_object == content_object
        )

    def delete_all_contacts(self, content_object):
        for contact in self.object.contacts.all():
            contact.delete()

    def delete_old_contacts(self, content_object, data):
        contact_uuids = [
            contact_data['uuid']
            for contact_data in data
        ]

        for contact in content_object.contacts.all():
            if self.is_old_contact(content_object, contact, contact_uuids):
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

    def get_object(self):
        uuid = self.kwargs.get('uuid', None)
        return get_object_or_404(self.model, uuid=uuid)

    def get_or_create_object(self):
        uuid = self.kwargs.get('uuid', None)
        return get_or_create_object(self.model, uuid=uuid)

    def render_to_response(self, context):
        content = self.serialize(context['object'])
        return json_response(content)

    def update_transverse_themes(self, instance, data):
        if 'transverse_themes' in data:
            transverse_themes = TransverseTheme.objects.filter(
                id__in=data['transverse_themes']
            )
            instance.transverse_themes = transverse_themes.all()

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
        self._create(instance, data)

    @require_api_permission
    def update(self, instance, data):
        self._update(instance, data)

    @require_api_key
    @require_api_permission
    def delete(self, request, *args, **kwargs):
        self._delete(self.get_object())
        return json_response({})


class OrganizationView(HasContactsView):
    model = Organization
    serialize = staticmethod(serialize_organization)


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
        deserialize_organization(organization, data)
        organization.save()
        self.update_contacts(organization, data)
        self.update_pref(organization, 'pref_email', data)
        self.update_pref(organization, 'pref_phone', data)
        self.update_transverse_themes(organization, data)
        self.update_members(organization, data)
        organization.save()

    def _create(self, organization, data):
        self._save(organization, data)

    def _update(self, organization, data):
        self._save(organization, data)
        self.delete_old_contacts(organization, data.get('contacts', []))

    def _delete(self, organization):
        self.delete_all_contacts(organization)
        organization.delete()


class PersonView(HasContactsView):
    model = Person
    serialize = staticmethod(serialize_person)


class PersonListView(PersonView, BaseListView):
    pass


class PersonDetailView(PersonView, BaseDetailView):

    def _save(self, person, data):
        deserialize_person(person, data)
        person.save()
        self.update_contacts(person, data)
        self.update_pref(person, 'pref_email', data)
        person.save()

    def _create(self, person, data):
        self._save(person, data)

    def _update(self, person, data):
        self._save(person, data)
        self.delete_old_contacts(person, data.get('contacts', []))

    def _delete(self, person):
        self.delete_all_contacts(person)
        person.delete()


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


class CalendarListView(BaseListView):
    model = Calendar
    serialize = staticmethod(serialize_calendar)


class EventCategoryListView(BaseListView):
    model = EventCategory
    serialize = staticmethod(serialize_event_category)


class EventView(object):
    model = Event
    serialize = staticmethod(serialize_event)


class EventListView(EventView, BaseListView):
    pass


class EventDetailView(EventView, BaseDetailView):

    def _save(self, event, data):
        deserialize_event(event, data)

        if 'calendar' in data:
            event.calendar = Calendar.objects\
                .get(uuid=data['calendar'])

        event.save()

        if 'category' in data:
            event.category = EventCategory.objects\
                .filter(slug__in=data['category']).all()

        if 'activity' in data:
            event.activity = ActivityNomenclature.objects\
                .get(id=data['activity'])

        if 'organization' in data:
            event.organization = Organization.objects\
                .get(uuid=data['organization'])

        if 'organizations' in data:
            event.organizations = Organization.objects\
                .filter(uuid__in=data['organizations']).all()

        self.update_transverse_themes(event, data)
        event.save()

    def _create(self, event, data):
        self._save(event, data)

    def _update(self, event, data):
        self._save(event, data)

    def _delete(self, event, data):
        event.delete()


class ContactMediumListView(BaseListView):
    model = ContactMedium
    serialize = staticmethod(serialize_contact_medium)
