# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClientTarget'
        db.create_table('coop_local_clienttarget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('coop_local', ['ClientTarget'])

        # Adding model 'Offer'
        db.create_table('coop_local_offer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.ActivityNomenclature'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('technical_means', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('workforce', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('practical_modalities', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_local.Organization'])),
        ))
        db.send_create_signal('coop_local', ['Offer'])

        # Adding M2M table for field targets on 'Offer'
        db.create_table('coop_local_offer_targets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['coop_local.offer'], null=False)),
            ('clienttarget', models.ForeignKey(orm['coop_local.clienttarget'], null=False))
        ))
        db.create_unique('coop_local_offer_targets', ['offer_id', 'clienttarget_id'])

        # Adding M2M table for field area on 'Offer'
        db.create_table('coop_local_offer_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['coop_local.offer'], null=False)),
            ('area', models.ForeignKey(orm['coop_local.area'], null=False))
        ))
        db.create_unique('coop_local_offer_area', ['offer_id', 'area_id'])

        # Adding field 'Organization.short_description'
        db.add_column('coop_local_organization', 'short_description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ClientTarget'
        db.delete_table('coop_local_clienttarget')

        # Deleting model 'Offer'
        db.delete_table('coop_local_offer')

        # Removing M2M table for field targets on 'Offer'
        db.delete_table('coop_local_offer_targets')

        # Removing M2M table for field area on 'Offer'
        db.delete_table('coop_local_offer_area')

        # Deleting field 'Organization.short_description'
        db.delete_column('coop_local_organization', 'short_description')


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
        'coop_local.activitynomenclature': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'unique_together': "(('label', 'parent'),)", 'object_name': 'ActivityNomenclature'},
            'avise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.ActivityNomenclatureAvise']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['coop_local.ActivityNomenclature']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '306'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'coop_local.activitynomenclatureavise': {
            'Meta': {'ordering': "['label']", 'object_name': 'ActivityNomenclatureAvise'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'moT7bXMGDuPi9ofRy9C5m4'", 'max_length': '50', 'null': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'e2yRxkkiwrZYYi9jrdszS4'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.clienttarget': {
            'Meta': {'ordering': "['label']", 'object_name': 'ClientTarget'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'RS4LK3wEMnguUZpc5CUYG7'", 'max_length': '50', 'null': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'TvJcU9nnTcJerfDPYbP8YB'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.event': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Event'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.ActivityNomenclature']", 'null': 'True', 'blank': 'True'}),
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Calendar']", 'on_delete': 'models.PROTECT'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.EventCategory']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_type'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['coop_local.EventCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Location']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'publisher organization'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['coop_local.Organization']"}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'other organizations'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['coop_local.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Person']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
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
            'transverse_themes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.TransverseTheme']", 'null': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'BnTVuGyqQTbZECE6DRbE9J'", 'max_length': '50', 'null': 'True'})
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
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.ActivityNomenclature']", 'null': 'True', 'blank': 'True'}),
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
            'transverse_themes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.TransverseTheme']", 'null': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'CaA5RKBYt7uabLTbUYVech'", 'max_length': '50', 'null': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'eW2aeWaaWyv9E5c2ES7REK'", 'max_length': '50', 'null': 'True'}),
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
        'coop_local.offer': {
            'Meta': {'object_name': 'Offer'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.ActivityNomenclature']"}),
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.Area']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'practical_modalities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.Organization']"}),
            'targets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.ClientTarget']", 'null': 'True', 'blank': 'True'}),
            'technical_means': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'workforce': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'coop_local.organization': {
            'Meta': {'object_name': 'Organization'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_local.ActivityNomenclature']", 'null': 'True', 'blank': 'True'}),
            'birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.OrganizationCategory']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_sha1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_project': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.Person']", 'through': "orm['coop_local.Engagement']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'naf': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pref_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pref_address_org'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Location']"}),
            'pref_email': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pref_email'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Contact']"}),
            'pref_label': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'pref_phone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pref_phone'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['coop_local.Contact']"}),
            'presage': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_local.Organization']", 'through': "orm['coop_local.Relation']", 'symmetrical': 'False'}),
            'secteur_fse': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'siret': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'True'}),
            'statut': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'transverse_themes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['coop_local.TransverseTheme']", 'null': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'JJbraQ4JZTFyBvMcyHuFNW'", 'max_length': '50', 'null': 'True'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'cxeihdugrSZ5wqKrYQsNoZ'", 'max_length': '50', 'null': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'y6QFxJWTHKcGitqjjThAZV'", 'max_length': '50', 'null': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'yzwdUz6JaqFqPbRk6k8rd5'", 'max_length': '50', 'null': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'AzMMFXSgo3TbxqkPVxtbx3'", 'max_length': '50', 'null': 'True'})
        },
        'coop_local.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coop_local_taggeditem_taggeditem_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coop_local_taggeditem_items'", 'to': "orm['coop_local.Tag']"})
        },
        'coop_local.transversetheme': {
            'Meta': {'object_name': 'TransverseTheme'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
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