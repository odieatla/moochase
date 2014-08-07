from django.db import transaction, connection
from django.db import models
from django.conf import settings
from decimal import *

import csv
#import lxml
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

# model manager
class TheatreManager(models.Manager):
    def import_data(self):
        tree = etree.parse(settings.THEATRE_XML_PATH)

        try:
            s = tree.find('sources')
            try:
                theatres = s.find('theatres')
            except:
                #no theatres
                print "no theatres"
        except:
            print "error no sources"
            #error no sources       print "error no theatres"
        tag_list = ['tms_id','code', 'name', 'chain', 'chain_code', 'lat', 'lon', 'active', 'zip']

        out = settings.THEATRE_CSV_PATH
        out_data = []
        out_data.append(tag_list[:])

        for theatre in theatres:
            tline = []
            tline.append(theatre.get('theatreId'))
            tline.append(theatre.get('aaCode'))
            tline.append(theatre.findtext('name'))
            tline.append(theatre.findtext('chain'))
            tline.append(theatre.find('chain').get('chainAaCode'))
            tline.append(theatre.findtext('latitude'))
            tline.append(theatre.findtext('longitude'))
            tline.append(theatre.findtext('active'))
            tline.append(theatre.findtext('.//address/postalCode'))

            out_data.append(tline)

        print "finished xml, writing file..."

        out_file  = open(out, "wb")
        csv_writer = csv.writer(out_file, quoting=csv.QUOTE_MINIMAL)

        for row in out_data:
            csv_writer.writerow(row)

        out_file.close()

        print "wrote %s" % out

        try:
            with transaction.atomic():
                #TODO: put xmlparser and theatre in setting.
                #Theatres.objects.raw('create temp table temp_theatre like xmlparser_theatre')
                #Theatre.objects.raw('copy temp_teatre from "' + out + '" DELIMITER "," CSV')
                #Theatre.objects.raw('update xmlparser_theatre x set x.* = y.* from tmp_theatre y where x.tms_id = y.tms_id')
                #Theatre.objects.raw('insert into xmlparser_theatre select * from temp_theatre where tms_id not in (select tms_id from xmlparser_theatre)')
                cursor = connection.cursor()
                cursor.execute('create temp table temp_theatre (like xmlparser_theatre INCLUDING DEFAULTS)')
                cursor.execute("copy temp_theatre from '" + out + "' DELIMITER ',' CSV HEADER")
                #cursor.execute('update xmlparser_theatre x set x.* = y.* from temp_theatre y where x.tms_id = y.tms_id')
                #cursor.execute('insert into xmlparser_theatre select * from temp_theatre where tms_id not in (select tms_id from xmlparser_theatre)')
        except:
            print "roll back"

# Create your models here.
class Theatres(models.Model):
    #TODO: set default values
    #TODO: add our own id for each theatre
    tms_id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    chain = models.CharField(max_length=200)
    chain_code = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=6, decimal_places=4, default=Decimal('0.0000'))
    lon = models.DecimalField(max_digits=7,decimal_places=4, default=Decimal('0.0000'))
    active = models.BooleanField()
    zip = models.CharField(max_length=5)

    objects = TheatreManager()

    def __unicode__(self):
        return self.tms_id + ":" + self.name

