# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TheatreMovie.qualifiers'
        db.delete_column(u'xmlparser_theatremovie', 'qualifiers')


    def backwards(self, orm):
        # Adding field 'TheatreMovie.qualifiers'
        db.add_column(u'xmlparser_theatremovie', 'qualifiers',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 5, 8, 0, 0), max_length=300),
                      keep_default=False)


    models = {
        u'xmlparser.movie': {
            'Meta': {'object_name': 'Movie'},
            'alt_film_id': ('django.db.models.fields.IntegerField', [], {}),
            'color_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'connect_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'original_audio_language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'program_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'root_id': ('django.db.models.fields.IntegerField', [], {}),
            'run_time': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tms_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'version_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'xmlparser.theatre': {
            'Meta': {'object_name': 'Theatre'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'chain': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'chain_code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geog': ('django.contrib.gis.db.models.fields.PointField', [], {'default': 'None', 'null': 'True', 'blank': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'default': "'0.0000'", 'max_digits': '6', 'decimal_places': '4'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'default': "'0.0000'", 'max_digits': '7', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tms_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'xmlparser.theatremovie': {
            'Meta': {'unique_together': "(('movie_id', 'theatre', 'date', 'time'),)", 'object_name': 'TheatreMovie', 'index_together': "[['movie_id', 'theatre', 'date', 'time']]"},
            'bargin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'theatre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xmlparser.Theatre']"}),
            'time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['xmlparser']