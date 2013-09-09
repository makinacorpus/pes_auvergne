import json
from uuid import uuid4

from unittest import TestCase, main

import requests


class TestMixin(object):
    organizations_url = 'http://localhost:8000/api/organizations/%s/'
    persons_url = 'http://localhost:8000/api/persons/%s/'

    def assertAreListOf(self, obj, keys, type_):
        for key in keys:
            for value in obj[key]:
                self.assertIsInstance(value, type_)

    def assertAreInstances(self, obj, keys, type_):
        for key in keys:
            self.assertIsInstance(obj[key], type_)

    def assertAreInstancesOrNone(self, obj, keys, type_):
        for key in keys:
            if not obj[key] is None:
                self.assertIsInstance(obj[key], type_)

    def assertValidOrganization(self, organization):
        self.assertAreInstances(organization, [
            'uuid',
            'title',
            'short_description',
            'testimony',
        ], basestring)

        self.assertAreInstancesOrNone(organization, [
            'web',
            'acronym',
            'birth',
            'legal_status',
        ], basestring)

        self.assertAreInstancesOrNone(organization, [
            'annual_revenue',
        ], int)

        self.assertAreInstancesOrNone(organization, [
            'workforce',
        ], float)

        self.assertAreListOf(organization, [
            'members',
        ], basestring)

        self.assertAreListOfValid(organization, [
            'contacts',
        ], self.assertValidContact)

        #self.assertAreListOf(organization, [
        #    'transverse_themes',
        #], int)

    def assertValidPerson(self, person):
        self.assertAreInstances(person, [
            'uuid',
            'first_name',
            'last_name',
        ], basestring)

        self.assertAreInstancesOrNone(person, [
            'pref_email'
        ], basestring)

        self.assertAreListOfValid(person, [
            'contacts',
        ], self.assertValidContact)

    def assertAreListOfValid(self, obj, keys, validator):
        for key in keys:
            for item in obj[key]:
                validator(item)

    def assertValidContact(self, contact):
        self.assertAreInstances(contact, [
            'uuid',
            'content',
        ], basestring)

    def put(self, url, data):
        content = json.dumps(data)

        response = requests.put(url, content)
        try:
            response.raise_for_status()
        except Exception as e:
            with open('%s.html' % self.output_name, 'w') as output:
                output.write(response.text)
            raise(e)

        with open('%s.json' % self.output_name, 'w') as output:
            json.dump(response.json(), output, indent=4)

        return response.json()

    def put_person(self, uuid, data):
        return self.put(self.persons_url % uuid, data)

    def put_organization(self, uuid, data):
        return self.put(self.organizations_url % uuid, data)

    def make_person(self, updates=None):
        person = {
            'first_name': uuid4().hex,
            'last_name': uuid4().hex,
            'pref_email': None,
            'contacts': [],
        }
        if updates:
            person.update(updates)
        return person

    def create_person(self, updates=None):
        uuid = uuid4().hex
        person = self.make_person(updates)
        return self.put_person(uuid, person)

    def make_organization(self, updates=None):
        organization = {
            'web': None,
            'annual_revenue': None,
            'contacts': [],
            'acronym': '',
            'pref_email': None,
            'title': 'Test',
            'birth': None,
            'workforce': None,
            'testimony': '',
            'legal_status': None,
            'pref_phone': None,
            'pref_address': None,
            #'transverse_themes': [],
            'short_description': '',
            'members': []
        }
        if updates:
            organization.update(updates)
        return organization

    def create_organization(self, updates=None):
        uuid = uuid4().hex
        organization = self.make_organization(updates)
        return self.put_organization(uuid, organization)


class TestOrganizationList(TestMixin, TestCase):

    def setUp(self):
        response = requests.get('http://localhost:8000/api/organizations/')
        try:
            response.raise_for_status()
        except Exception as e:
            with open('organization_listing.html', 'w') as output:
                output.write(response.text)
            raise(e)

        self.organizations = response.json()

        with open('organization_listing.json', 'w') as output:
            json.dump(response.json(), output, indent=4)

    def test_organizations_are_valid(self):
        for organization in self.organizations:
            self.assertValidOrganization(organization)


class TestOrganization(TestMixin, TestCase):

    def test_create_minimal_organization(self):
        self.output_name = 'minimal_organization'
        uuid = uuid4().hex
        data = self.make_organization()
        reponse = self.put_organization(uuid, data)
        self.assertValidOrganization(reponse)

    def test_update_organization(self):
        self.output_name = 'update_organization'
        data = self.create_organization()
        data['web'] = 'http://%s.local' % uuid4().hex
        reponse = self.put_organization(data['uuid'], data)
        self.assertEquals(reponse, data)

    def test_update_organization_with_only_new_data(self):
        self.output_name = 'update_organization_with_only_new_data'
        data = self.create_organization()
        data['web'] = 'http://%s.local' % uuid4().hex
        reponse = self.put_organization(data['uuid'], {
            'web': data['web']
        })
        self.assertEquals(reponse, data)

    def test_create_organization_with_owned_contacts(self):
        self.output_name = 'organization_with_owned_contacts'
        uuid = uuid4().hex
        pref_email = uuid4().hex
        pref_phone = uuid4().hex
        data = self.make_organization({
            'contacts': [
                {'uuid': pref_email, 'content': 'contact@test.local'},
                {'uuid': pref_phone, 'content': '00.00.00.00.00'},
            ],
            'pref_email': pref_email,
            'pref_phone': pref_phone,
        })
        reponse = self.put_organization(uuid, data)
        self.assertValidOrganization(reponse)

    def test_create_organization_with_member_pref_email_and_phone(self):
        self.output_name = 'organization_with_member_pref_email_and_phone'
        uuid = uuid4().hex
        pref_email = uuid4().hex
        pref_phone = uuid4().hex
        self.create_person({
            'contacts': [
                {'uuid': pref_email, 'content': 'contact@test.local'},
                {'uuid': pref_phone, 'content': '00.00.00.00.00'},
            ],
        })
        data = self.make_organization({
            'pref_email': pref_email,
            'pref_phone': pref_phone,
        })
        reponse = self.put_organization(uuid, data)
        self.assertValidOrganization(reponse)


class TestPersonList(TestMixin, TestCase):

    def setUp(self):
        response = requests.get('http://localhost:8000/api/persons/')
        try:
            response.raise_for_status()
        except Exception as e:
            with open('person_listing.html', 'w') as output:
                output.write(response.text)
            raise(e)

        self.persons = response.json()

        with open('person_listing.json', 'w') as output:
            json.dump(response.json(), output, indent=4)

    def test_persons_are_valid(self):
        for person in self.persons:
            self.assertValidPerson(person)


class TestPerson(TestMixin, TestCase):

    def test_create_minimal_person(self):
        self.output_name = 'minimal_person'
        uuid = uuid4().hex
        data = self.make_person()
        reponse = self.put_person(uuid, data)
        self.assertValidPerson(reponse)

    def test_update_person(self):
        self.output_name = 'update_person'
        data = self.create_person()
        data['first_name'] = uuid4().hex
        reponse = self.put_person(data['uuid'], data)
        self.assertEquals(reponse, data)

    def test_update_person_with_only_new_data(self):
        self.output_name = 'update_person_with_only_new_data'
        data = self.create_person()
        data['first_name'] = uuid4().hex
        reponse = self.put_person(data['uuid'], {
            'first_name': data['first_name']
        })
        self.assertEquals(reponse, data)

    def test_create_person_with_owned_contacts(self):
        self.output_name = 'person_with_owned_contacts'
        uuid = uuid4().hex
        pref_email = uuid4().hex
        data = self.make_person({
            'contacts': [
                {'uuid': pref_email, 'content': 'contact@test.local'},
            ],
            'pref_email': pref_email,
        })
        reponse = self.put_person(uuid, data)
        self.assertValidPerson(reponse)

    def test_create_person_with_organization_pref_email_and_phone(self):
        self.output_name = 'person_with_organization_pref_email_and_phone'
        uuid = uuid4().hex
        pref_email = uuid4().hex
        self.create_organization({
            'contacts': [
                {'uuid': pref_email, 'content': 'contact@test.local'},
            ],
        })
        data = self.make_person({
            'pref_email': pref_email,
        })
        reponse = self.put_person(uuid, data)
        self.assertValidPerson(reponse)


if __name__ == '__main__':
    main()
