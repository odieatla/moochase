# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Theatre'
        db.create_table(u'xmlparser_theatre', (
            ('tms_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('chain', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('chain_code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(default='0.0000', max_digits=6, decimal_places=4)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(default='0.0000', max_digits=7, decimal_places=4)),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PointField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'xmlparser', ['Theatre'])


    def backwards(self, orm):
        # Deleting model 'Theatre'
        db.delete_table(u'xmlparser_theatre')


    models = {
        u'xmlparser.theatre': {
            'Meta': {'object_name': 'Theatre'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'chain': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'chain_code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'default': "'0.0000'", 'max_digits': '6', 'decimal_places': '4'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'default': "'0.0000'", 'max_digits': '7', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tms_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['xmlparser']