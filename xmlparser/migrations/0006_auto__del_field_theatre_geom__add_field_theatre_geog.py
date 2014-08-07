# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Theatre.geom'
        db.delete_column(u'xmlparser_theatre', 'geom')

        # Adding field 'Theatre.geog'
        db.add_column(u'xmlparser_theatre', 'geog',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(default=None, null=True, blank=True, geography=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Theatre.geom'
        db.add_column(u'xmlparser_theatre', 'geom',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Theatre.geog'
        db.delete_column(u'xmlparser_theatre', 'geog')


    models = {
        u'xmlparser.theatre': {
            'Meta': {'object_name': 'Theatre'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'chain': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'chain_code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geog': ('django.contrib.gis.db.models.fields.PointField', [], {'default': 'None', 'null': 'True', 'blank': 'True', 'geography': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'default': "'0.0000'", 'max_digits': '6', 'decimal_places': '4'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'default': "'0.0000'", 'max_digits': '7', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tms_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['xmlparser']