# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('coop_local_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='dA9bPvbi2Qry2Ez8tzpoB7', max_length=50, null=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('adr1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('adr2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('x_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Area'], null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('geohash', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('is_ref_center', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('coop_local', ['Location'])

        # Adding M2M table for field sites on 'Location'
        db.create_table('coop_local_location_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm['coop_local.location'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_location_sites', ['location_id', 'site_id'])

        # Adding model 'Located'
        db.create_table('coop_local_located', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Location'], null=True, blank=True)),
            ('main_location', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_geo.LocationCategory'], null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('coop_local', ['Located'])

        # Adding model 'Area'
        db.create_table('coop_local_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='D9cphpnykCfL4Fo4bNTuxG', max_length=50, null=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('default_location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='associated_area', null=True, to=orm['coop_local.Location'])),
            ('area_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_geo.AreaType'])),
            ('polygon', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('update_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('coop_local', ['Area'])

        # Adding M2M table for field sites on 'Area'
        db.create_table('coop_local_area_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('area', models.ForeignKey(orm['coop_local.area'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_area_sites', ['area_id', 'site_id'])

        # Adding model 'DeletedURI'
        db.create_table('coop_local_deleteduri', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('rdf_type', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('coop_local', ['DeletedURI'])

        # Adding model 'LinkProperty'
        db.create_table('coop_local_linkproperty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('coop_local', ['LinkProperty'])

        # Adding model 'Link'
        db.create_table('coop_local_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('predicate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.LinkProperty'])),
            ('object_uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('coop_local', ['Link'])

        # Adding model 'Tag'
        db.create_table('coop_local_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='XjTKBBMNFyrndaRn4gnBFZ', max_length=50, null=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='fr', max_length=10)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Person'], null=True, blank=True)),
            ('person_uri', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('concept_uri', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('coop_local', ['Tag'])

        # Adding M2M table for field sites on 'Tag'
        db.create_table('coop_local_tag_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['coop_local.tag'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_tag_sites', ['tag_id', 'site_id'])

        # Adding model 'TaggedItem'
        db.create_table('coop_local_taggeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coop_local_taggeditem_items', to=orm['coop_local.Tag'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coop_local_taggeditem_taggeditem_items', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('coop_local', ['TaggedItem'])

        # Adding model 'PersonCategory'
        db.create_table('coop_local_personcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='label', overwrite=True)),
        ))
        db.send_create_signal('coop_local', ['PersonCategory'])

        # Adding model 'Person'
        db.create_table('coop_local_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='ChBcTvdziVSdrajiHdmxfE', max_length=50, null=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pref_email', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='preferred_email', null=True, on_delete=models.SET_NULL, to=orm['coop_local.Contact'])),
            ('structure', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Location'], null=True, blank=True)),
            ('location_display', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
        ))
        db.send_create_signal('coop_local', ['Person'])

        # Adding M2M table for field sites on 'Person'
        db.create_table('coop_local_person_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['coop_local.person'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_person_sites', ['person_id', 'site_id'])

        # Adding M2M table for field category on 'Person'
        db.create_table('coop_local_person_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['coop_local.person'], null=False)),
            ('personcategory', models.ForeignKey(orm['coop_local.personcategory'], null=False))
        ))
        db.create_unique('coop_local_person_category', ['person_id', 'personcategory_id'])

        # Adding model 'ContactMedium'
        db.create_table('coop_local_contactmedium', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('coop_local', ['ContactMedium'])

        # Adding model 'Contact'
        db.create_table('coop_local_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='NVhFAXpU5RZmKjjx8Z4SS6', max_length=50, null=True)),
            ('category', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('contact_medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.ContactMedium'], null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('display', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('coop_local', ['Contact'])

        # Adding M2M table for field sites on 'Contact'
        db.create_table('coop_local_contact_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['coop_local.contact'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_contact_sites', ['contact_id', 'site_id'])

        # Adding model 'RoleCategory'
        db.create_table('coop_local_rolecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='label', overwrite=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('coop_local', ['RoleCategory'])

        # Adding model 'Role'
        db.create_table('coop_local_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='DAT3RijfjBS8zZR2ETtM3g', max_length=50, null=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='label', unique_with=())),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.RoleCategory'], null=True, blank=True)),
        ))
        db.send_create_signal('coop_local', ['Role'])

        # Adding M2M table for field sites on 'Role'
        db.create_table('coop_local_role_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('role', models.ForeignKey(orm['coop_local.role'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_role_sites', ['role_id', 'site_id'])

        # Adding model 'Relation'
        db.create_table('coop_local_relation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source', to=orm['coop_local.Organization'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target', to=orm['coop_local.Organization'])),
            ('reltype', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('relation_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.OrgRelationType'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
        ))
        db.send_create_signal('coop_local', ['Relation'])

        # Adding model 'Engagement'
        db.create_table('coop_local_engagement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='ae2xcViTu6mai5F9k677NP', max_length=50, null=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='engagements', to=orm['coop_local.Person'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Organization'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Role'], null=True, blank=True)),
            ('role_detail', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('org_admin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('engagement_display', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('remote_person_uri', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('remote_person_label', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('remote_role_uri', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('remote_role_label', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('remote_organization_uri', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('remote_organization_label', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('coop_local', ['Engagement'])

        # Adding M2M table for field sites on 'Engagement'
        db.create_table('coop_local_engagement_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('engagement', models.ForeignKey(orm['coop_local.engagement'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_engagement_sites', ['engagement_id', 'site_id'])

        # Adding model 'OrgRelationType'
        db.create_table('coop_local_orgrelationtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('key_name', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('org_to_org', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('org_to_project', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('coop_local', ['OrgRelationType'])

        # Adding model 'OrganizationCategory'
        db.create_table('coop_local_organizationcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='label', overwrite=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('coop_local', ['OrganizationCategory'])

        # Adding model 'Organization'
        db.create_table('coop_local_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='yERmsZ6hhKnvUJMcdgYec8', max_length=50, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pref_label', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('logo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('email_sha1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('pref_email', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pref_email', null=True, on_delete=models.SET_NULL, to=orm['coop_local.Contact'])),
            ('pref_phone', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pref_phone', null=True, on_delete=models.SET_NULL, to=orm['coop_local.Contact'])),
            ('pref_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pref_address_org', null=True, on_delete=models.SET_NULL, to=orm['coop_local.Location'])),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('coop_local', ['Organization'])

        # Adding M2M table for field sites on 'Organization'
        db.create_table('coop_local_organization_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organization', models.ForeignKey(orm['coop_local.organization'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_organization_sites', ['organization_id', 'site_id'])

        # Adding M2M table for field category on 'Organization'
        db.create_table('coop_local_organization_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organization', models.ForeignKey(orm['coop_local.organization'], null=False)),
            ('organizationcategory', models.ForeignKey(orm['coop_local.organizationcategory'], null=False))
        ))
        db.create_unique('coop_local_organization_category', ['organization_id', 'organizationcategory_id'])

        # Adding model 'Exchange'
        db.create_table('coop_local_exchange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='RMjGFYnkLXBWVNKcvnnipB', max_length=50, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exchanges', null=True, to=orm['coop_local.Organization'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Person'], null=True, blank=True)),
            ('eway', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('etype', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('permanent', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('expiration', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=True)),
            ('remote_person_uri', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('remote_person_label', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('remote_organization_uri', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('remote_organization_label', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exchange_location', null=True, to=orm['coop_local.Location'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exchange_area', null=True, to=orm['coop_local.Area'])),
        ))
        db.send_create_signal('coop_local', ['Exchange'])

        # Adding M2M table for field sites on 'Exchange'
        db.create_table('coop_local_exchange_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exchange', models.ForeignKey(orm['coop_local.exchange'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_exchange_sites', ['exchange_id', 'site_id'])

        # Adding M2M table for field products on 'Exchange'
        db.create_table('coop_local_exchange_products', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exchange', models.ForeignKey(orm['coop_local.exchange'], null=False)),
            ('product', models.ForeignKey(orm['coop_local.product'], null=False))
        ))
        db.create_unique('coop_local_exchange_products', ['exchange_id', 'product_id'])

        # Adding M2M table for field methods on 'Exchange'
        db.create_table('coop_local_exchange_methods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exchange', models.ForeignKey(orm['coop_local.exchange'], null=False)),
            ('exchangemethod', models.ForeignKey(orm['coop_local.exchangemethod'], null=False))
        ))
        db.create_unique('coop_local_exchange_methods', ['exchange_id', 'exchangemethod_id'])

        # Adding model 'ExchangeMethod'
        db.create_table('coop_local_exchangemethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('etypes', self.gf('coop.utils.fields.MultiSelectField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('coop_local', ['ExchangeMethod'])

        # Adding model 'Product'
        db.create_table('coop_local_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='etu4WP28MaxSFpHmrAnjhJ', max_length=50, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='products', null=True, to=orm['coop_local.Organization'])),
            ('remote_organization_uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('remote_organization_label', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('coop_local', ['Product'])

        # Adding M2M table for field sites on 'Product'
        db.create_table('coop_local_product_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['coop_local.product'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_product_sites', ['product_id', 'site_id'])

        # Adding model 'Calendar'
        db.create_table('coop_local_calendar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='pzjFjyDtXEjeF65YCKGWRA', max_length=50, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
        ))
        db.send_create_signal('coop_local', ['Calendar'])

        # Adding M2M table for field sites on 'Calendar'
        db.create_table('coop_local_calendar_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('calendar', models.ForeignKey(orm['coop_local.calendar'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_calendar_sites', ['calendar_id', 'site_id'])

        # Adding model 'Event'
        db.create_table('coop_local_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uri_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='Xi7EqiEBVHqHn4zQDK9Go6', max_length=50, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_type', null=True, to=orm['coop_local.EventCategory'])),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Calendar'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'publisher organization', null=True, to=orm['coop_local.Organization'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Person'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Location'], null=True, blank=True)),
            ('remote_location_uri', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('remote_location_label', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('remote_person_uri', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('remote_person_label', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('remote_organization_uri', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('remote_organization_label', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('pref_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pref_address_event', null=True, on_delete=models.SET_NULL, to=orm['coop_local.Location'])),
        ))
        db.send_create_signal('coop_local', ['Event'])

        # Adding M2M table for field sites on 'Event'
        db.create_table('coop_local_event_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['coop_local.event'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('coop_local_event_sites', ['event_id', 'site_id'])

        # Adding M2M table for field category on 'Event'
        db.create_table('coop_local_event_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['coop_local.event'], null=False)),
            ('eventcategory', models.ForeignKey(orm['coop_local.eventcategory'], null=False))
        ))
        db.create_unique('coop_local_event_category', ['event_id', 'eventcategory_id'])

        # Adding M2M table for field organizations on 'Event'
        db.create_table('coop_local_event_organizations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['coop_local.event'], null=False)),
            ('organization', models.ForeignKey(orm['coop_local.organization'], null=False))
        ))
        db.create_unique('coop_local_event_organizations', ['event_id', 'organization_id'])

        # Adding model 'EventCategory'
        db.create_table('coop_local_eventcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='label', overwrite=False)),
        ))
        db.send_create_signal('coop_local', ['EventCategory'])

        # Adding model 'Occurrence'
        db.create_table('coop_local_occurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Event'])),
        ))
        db.send_create_signal('coop_local', ['Occurrence'])

        # Adding model 'Dated'
        db.create_table('coop_local_dated', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Event'], null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('coop_local', ['Dated'])

        # Adding model 'SitePrefs'
        db.create_table('coop_local_siteprefs', (
            ('preferences_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['preferences.Preferences'], unique=True, primary_key=True)),
            ('main_organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_org', null=True, to=orm['coop_local.Organization'])),
        ))
        db.send_create_signal('coop_local', ['SitePrefs'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table('coop_local_location')

        # Removing M2M table for field sites on 'Location'
        db.delete_table('coop_local_location_sites')

        # Deleting model 'Located'
        db.delete_table('coop_local_located')

        # Deleting model 'Area'
        db.delete_table('coop_local_area')

        # Removing M2M table for field sites on 'Area'
        db.delete_table('coop_local_area_sites')

        # Deleting model 'DeletedURI'
        db.delete_table('coop_local_deleteduri')

        # Deleting model 'LinkProperty'
        db.delete_table('coop_local_linkproperty')

        # Deleting model 'Link'
        db.delete_table('coop_local_link')

        # Deleting model 'Tag'
        db.delete_table('coop_local_tag')

        # Removing M2M table for field sites on 'Tag'
        db.delete_table('coop_local_tag_sites')

        # Deleting model 'TaggedItem'
        db.delete_table('coop_local_taggeditem')

        # Deleting model 'PersonCategory'
        db.delete_table('coop_local_personcategory')

        # Deleting model 'Person'
        db.delete_table('coop_local_person')

        # Removing M2M table for field sites on 'Person'
        db.delete_table('coop_local_person_sites')

        # Removing M2M table for field category on 'Person'
        db.delete_table('coop_local_person_category')

        # Deleting model 'ContactMedium'
        db.delete_table('coop_local_contactmedium')

        # Deleting model 'Contact'
        db.delete_table('coop_local_contact')

        # Removing M2M table for field sites on 'Contact'
        db.delete_table('coop_local_contact_sites')

        # Deleting model 'RoleCategory'
        db.delete_table('coop_local_rolecategory')

        # Deleting model 'Role'
        db.delete_table('coop_local_role')

        # Removing M2M table for field sites on 'Role'
        db.delete_table('coop_local_role_sites')

        # Deleting model 'Relation'
        db.delete_table('coop_local_relation')

        # Deleting model 'Engagement'
        db.delete_table('coop_local_engagement')

        # Removing M2M table for field sites on 'Engagement'
        db.delete_table('coop_local_engagement_sites')

        # Deleting model 'OrgRelationType'
        db.delete_table('coop_local_orgrelationtype')

        # Deleting model 'OrganizationCategory'
        db.delete_table('coop_local_organizationcategory')

        # Deleting model 'Organization'
        db.delete_table('coop_local_organization')

        # Removing M2M table for field sites on 'Organization'
        db.delete_table('coop_local_organization_sites')

        # Removing M2M table for field category on 'Organization'
        db.delete_table('coop_local_organization_category')

        # Deleting model 'Exchange'
        db.delete_table('coop_local_exchange')

        # Removing M2M table for field sites on 'Exchange'
        db.delete_table('coop_local_exchange_sites')

        # Removing M2M table for field products on 'Exchange'
        db.delete_table('coop_local_exchange_products')

        # Removing M2M table for field methods on 'Exchange'
        db.delete_table('coop_local_exchange_methods')

        # Deleting model 'ExchangeMethod'
        db.delete_table('coop_local_exchangemethod')

        # Deleting model 'Product'
        db.delete_table('coop_local_product')

        # Removing M2M table for field sites on 'Product'
        db.delete_table('coop_local_product_sites')

        # Deleting model 'Calendar'
        db.delete_table('coop_local_calendar')

        # Removing M2M table for field sites on 'Calendar'
        db.delete_table('coop_local_calendar_sites')

        # Deleting model 'Event'
        db.delete_table('coop_local_event')

        # Removing M2M table for field sites on 'Event'
        db.delete_table('coop_local_event_sites')

        # Removing M2M table for field category on 'Event'
        db.delete_table('coop_local_event_category')

        # Removing M2M table for field organizations on 'Event'
        db.delete_table('coop_local_event_organizations')

        # Deleting model 'EventCategory'
        db.delete_table('coop_local_eventcategory')

        # Deleting model 'Occurrence'
        db.delete_table('coop_local_occurrence')

        # Deleting model 'Dated'
        db.delete_table('coop_local_dated')

        # Deleting model 'SitePrefs'
        db.delete_table('coop_local_siteprefs')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'coop_geo.arealink': {
            'Meta': {'object_name': 'AreaLink'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Area']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'coop_geo.arearelations': {
            'Meta': {'object_name': 'AreaRelations'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_rels'", 'to': "orm['coop_local.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_rels'", 'to': "orm['coop_local.Area']"})
        },
        'coop_geo.areatype': {
            'Meta': {'object_name': 'AreaType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'txt_idx': ('django.db.models.fields.CharField', [], {'max_length': "'50'"})
        },
        'coop_geo.locationcategory': {
            'Meta': {'ordering': "['label']", 'object_name': 'LocationCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'label'", 'overwrite': 'False'})
        },
        'coop_local.area': {
            'Meta': {'object_name': 'Area'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'area_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_geo.AreaType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'default_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'associated_area'", 'null': 'True', 'to': "orm['coop_local.Location']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'related_areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.Area']", 'through': "orm['coop_geo.AreaRelations']", 'symmetrical': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'update_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'NTeQ6ucPUVwcyVYQebaLMQ'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'DC8cAPqGo7QgTPt8j8DY5'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.contact': {
            'Meta': {'ordering': "['category']", 'object_name': 'Contact'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'contact_medium': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.ContactMedium']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'display': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'vywNhhG37FYRC62abUQk6T'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.contactmedium': {
            'Meta': {'object_name': 'ContactMedium'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'coop_local.dated': {
            'Meta': {'object_name': 'Dated'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Event']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'coop_local.deleteduri': {
            'Meta': {'object_name': 'DeletedURI'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'rdf_type': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'})
        },
        'coop_local.engagement': {
            'Meta': {'object_name': 'Engagement'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'engagement_display': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'org_admin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'engagements'", 'to': "orm['coop_local.Person']"}),
            'remote_organization_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'remote_organization_uri': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remote_person_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'remote_person_uri': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remote_role_label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'remote_role_uri': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Role']", 'null': 'True', 'blank': 'True'}),
            'role_detail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'XjouR6snDzz42wFK22woim'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.event': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Event'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Calendar']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.EventCategory']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_type'", 'null': 'True', 'to': "orm['coop_local.EventCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Location']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'publisher organization'", 'null': 'True', 'to': "orm['coop_local.Organization']"}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'other organizations'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['coop_local.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Person']", 'null': 'True', 'blank': 'True'}),
            'pref_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pref_address_event'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Location']"}),
            'remote_location_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'remote_location_uri': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_organization_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'remote_organization_uri': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_person_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'remote_person_uri': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'jrSQo9rBGGw83qpFzvhypd'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.eventcategory': {
            'Meta': {'object_name': 'EventCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'label'", 'overwrite': 'False'})
        },
        'coop_local.exchange': {
            'Meta': {'ordering': "('-modified',)", 'object_name': 'Exchange'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exchange_area'", 'null': 'True', 'to': "orm['coop_local.Area']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'etype': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'eway': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'expiration': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exchange_location'", 'null': 'True', 'to': "orm['coop_local.Location']"}),
            'methods': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.ExchangeMethod']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exchanges'", 'null': 'True', 'to': "orm['coop_local.Organization']"}),
            'permanent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Person']", 'null': 'True', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.Product']", 'symmetrical': 'False'}),
            'remote_organization_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'remote_organization_uri': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_person_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'remote_person_uri': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'EpNmkfNcaj3HGU5c3Nvse3'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.exchangemethod': {
            'Meta': {'object_name': 'ExchangeMethod'},
            'etypes': ('coop.utils.fields.MultiSelectField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'coop_local.link': {
            'Meta': {'object_name': 'Link'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'predicate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.LinkProperty']"})
        },
        'coop_local.linkproperty': {
            'Meta': {'object_name': 'LinkProperty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'coop_local.located': {
            'Meta': {'object_name': 'Located'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_geo.LocationCategory']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Location']", 'null': 'True', 'blank': 'True'}),
            'main_location': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'coop_local.location': {
            'Meta': {'object_name': 'Location'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adr1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'adr2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Area']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'geohash': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ref_center': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'q7UaKKPemkCopUbMVjSzNY'", 'max_length': '50', 'null': 'True'}),
            'x_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        'coop_local.occurrence': {
            'Meta': {'ordering': "('start_time', 'end_time')", 'object_name': 'Occurrence'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'coop_local.organization': {
            'Meta': {'ordering': "['title']", 'object_name': 'Organization'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.OrganizationCategory']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_sha1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.Person']", 'through': "orm['coop_local.Engagement']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pref_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pref_address_org'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Location']"}),
            'pref_email': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pref_email'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Contact']"}),
            'pref_label': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'pref_phone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pref_phone'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Contact']"}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.Organization']", 'through': "orm['coop_local.Relation']", 'symmetrical': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'fM85ooVagjMP7hC6rY2y3B'", 'max_length': '50', 'null': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'coop_local.organizationcategory': {
            'Meta': {'object_name': 'OrganizationCategory'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'label'", 'overwrite': 'True'})
        },
        'coop_local.orgrelationtype': {
            'Meta': {'object_name': 'OrgRelationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'org_to_org': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'org_to_project': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'coop_local.person': {
            'Meta': {'object_name': 'Person'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.PersonCategory']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Location']", 'null': 'True', 'blank': 'True'}),
            'location_display': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pref_email': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'preferred_email'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Contact']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'structure': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'cLaTaP4N6wDjWGezsvjN6C'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.personcategory': {
            'Meta': {'object_name': 'PersonCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'label'", 'overwrite': 'True'})
        },
        'coop_local.product': {
            'Meta': {'ordering': "['-modified']", 'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['coop_local.Organization']"}),
            'remote_organization_label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'remote_organization_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'6Tk6zwEZBBD56pPEdrQm23'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.relation': {
            'Meta': {'object_name': 'Relation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'relation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.OrgRelationType']", 'null': 'True', 'blank': 'True'}),
            'reltype': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'to': "orm['coop_local.Organization']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target'", 'to': "orm['coop_local.Organization']"})
        },
        'coop_local.role': {
            'Meta': {'object_name': 'Role'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.RoleCategory']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'label'", 'unique_with': '()'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'NWnYqSaVgNjp6Hxi5BKBBT'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.rolecategory': {
            'Meta': {'ordering': "['label']", 'object_name': 'RoleCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'label'", 'overwrite': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'coop_local.siteprefs': {
            'Meta': {'object_name': 'SitePrefs'},
            'main_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_org'", 'null': 'True', 'to': "orm['coop_local.Organization']"}),
            'preferences_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['preferences.Preferences']", 'unique': 'True', 'primary_key': 'True'})
        },
        'coop_local.tag': {
            'Meta': {'object_name': 'Tag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'concept_uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'fr'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Person']", 'null': 'True', 'blank': 'True'}),
            'person_uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'e4UTPCQPRtsoc7RQ2n78xi'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coop_local_taggeditem_taggeditem_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coop_local_taggeditem_items'", 'to': "orm['coop_local.Tag']"})
        },
        'preferences.preferences': {
            'Meta': {'object_name': 'Preferences'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['coop_local']