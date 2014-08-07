from django.db import transaction, connection
#from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.conf import settings
from decimal import *
from utils.util import load_xml_tree, load_to_csv, retrieve_from_ftp, decompress_gz, get_ftp_file_name, get_file_path
from utils.db import create_temp_table, copy_csv_to_tmp,update_t1_from_t2, insert_t1_from_t2, delete_t1_from_t2, delete_all
import re, sys



# model manager
class MovieManager(models.Manager):
    def get_db_table(self):
        return self.model._meta.db_table

    def get_copy_fields(self):
        return [field.name for field in self.model._meta.fields]

    def get_pk(self):
        return self.model._meta.pk.name

    def download_data(self):
        fgz = get_ftp_file_name(settings.MOVIE_XML_GZ_PATTERN)
        target = retrieve_from_ftp(fgz)
        decompress_gz(target)

    def import_data(self):
        programs = load_xml_tree(get_file_path(settings.MOVIE_XML_PATTERN), './programs')

        out = settings.MOVIE_CSV_PATH
        out_data = []

        for program in programs:
            pline = []
            tms_id = program.get('TMSId')
            mv = re.search("^MV", tms_id)
            #if program is not a movie, skip
            if mv is None:
                continue
            pline.append(tms_id)
            pline.append(program.get('altFilmId'))
            pline.append(program.get('rootId'))
            pline.append(program.get('versionId'))
            pline.append(program.get('connectorId'))
            pline.append(program.findtext('runTime'))
            pline.append(program.findtext('progType'))
            pline.append(program.findtext('colorCode'))
            pline.append(program.findtext('origAudioLang'))
            pline.append(program.findtext("./titles/title[@size='10']"))
            pline.append(program.findtext("./titles/title[@size='20']"))
            pline.append(program.findtext("./titles/title[@size='40']"))
            pline.append(program.findtext("./titles/title[@size='120']"))
            out_data.append(pline)
        print "finish xml, writing file..."
        load_to_csv(out, out_data)

        tablename = self.get_db_table()
        copy_columns = self.get_copy_fields()
        pk = [self.get_pk()]

        #ETL
        print "ETL"
        try:
            with transaction.atomic():
                cursor = connection.cursor()
                tmp_table = create_temp_table(cursor, tablename)
                copy_csv_to_tmp(cursor, out, tmp_table, copy_columns)
                update_t1_from_t2(cursor, tablename, tmp_table, copy_columns, pk)
                insert_t1_from_t2(cursor, tablename, tmp_table, 'tms_id')
                delete_t1_from_t2(cursor, tablename, tmp_table, 'tms_id')
        except:
            print "error:", sys.exc_info()[0]
            print "error:", sys.exc_info()[1]
            print "roll back"

        print "Done"

class TheatreMovieManager(models.Manager):
    def get_db_table(self):
        return self.model._meta.db_table

    def download_data(self):
        fgz = get_ftp_file_name(settings.SHOWTIME_XML_GZ_PATTERN)
        target = retrieve_from_ftp(fgz)
        decompress_gz(target)

    def import_data(self):
        showtimes = load_xml_tree(get_file_path(settings.SHOWTIME_XML_PATTERN), './schedules')

        out = settings.SHOWTIME_CSV_PATH
        out_data = []

        #TODO: only import movie data, or add a column for movie/event
        for showtime in showtimes:
            for event in showtime.findall('event'):
                for t in event.findall('./times/time'):
                    sline = []
                    sline.append(event.get('TMSId'))
                    sline.append(event.get('date'))
                    sline.append(showtime.get('theatreId'))
                    sline.append(t.findtext('.'))
                    if t.get('barg') == 'true':
                        sline.append(True)
                    else:
                        sline.append(False)
                    sline.append(event.findtext('quals'))
                    sline.append("{0} {1}".format(event.get('date'), t.findtext('.')))

                    out_data.append(sline)
        print "finish xml, writing file..."
        load_to_csv(out, out_data)

        tablename = self.get_db_table()
        copy_columns = ['movie_id', 'date', 'theatre_id', 'time', 'bargin', 'qualifiers', 'showtime']
        pk = ['movie_id', 'date', 'theatre_id', 'time']

        #ETL
        print "ETL"
        try:
            with transaction.atomic():
                cursor = connection.cursor()
                tmp_table = create_temp_table(cursor, tablename)
                copy_csv_to_tmp(cursor, out, tmp_table, copy_columns)
                delete_all(cursor, tablename)
                insert_t1_from_t2(cursor, tablename, tmp_table)
        except:
            print "error:", sys.exc_info()[0]
            print "error:", sys.exc_info()[1]
            print "roll back"

        print "Done"

class TheatreManager(models.Manager):
    def get_db_table(self):
        return self.model._meta.db_table

    def download_data(self):
        fgz = get_ftp_file_name(settings.THEATRE_XML_GZ_PATTERN)
        target = retrieve_from_ftp(fgz)
        decompress_gz(target)

    def import_data(self):
        theatres = load_xml_tree(get_file_path(settings.THEATRE_XML_PATTERN), './sources/theatres')

        out = settings.THEATRE_CSV_PATH
        out_data = []

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
        load_to_csv(out, out_data)

        tablename = self.get_db_table()
        copy_columns=['tms_id','code','name','chain','chain_code','lat','lon','active','zip']
        pk = copy_columns[0]

        #ETL
        print "ETL"
        try:
            with transaction.atomic():
                cursor = connection.cursor()
                tmp_table = create_temp_table(cursor, tablename)
                #cursor.execute("\copy temp_theatre(tms_id,code,name,chain,chain_code,lat,lon,active,zip) from '{0}' DELIMITER ',' CSV HEADER".format(out))
                copy_csv_to_tmp(cursor, out, tmp_table, copy_columns)
                update_t1_from_t2(cursor, tablename, tmp_table, copy_columns, pk)
                insert_t1_from_t2(cursor, tablename, tmp_table, pk)
                delete_t1_from_t2(cursor, tablename, tmp_table, pk)
                cursor.execute("update xmlparser_theatre set geom = ST_GeomFromText('POINT(' || lon || ' ' || lat || ')',4326)")
                cursor.execute("update xmlparser_theatre set geog = ST_GeogFromText('SRID=4326;POINT(' || lon || ' ' || lat || ')')")
        except:
            print "roll back"

        print "Done"

    def find_theatres(self, lon, lat, distance=5 ):
        #location = GEOSGeometry('POINT({0} {1})'.format(lon, lat))
        DISTANCE_LIMIT_METERS = distance * 1609

        input_point = Point(lon, lat, srid=4326)
        input_point.transform(900913)
        rst = Theatre.objects.filter(geom__dwithin=(input_point , D(m=DISTANCE_LIMIT_METERS)))

        #rst = Theatre.objects.filter(geom__dwithin=(location, D(m=DISTANCE_LIMIT_METERS)))
        print rst

# Create your models here.
class Theatre(models.Model):
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
    geom = models.PointField(srid=4326, blank=True, null=True, default=None)
    geog = models.PointField(srid=4326, blank=True, null=True, default=None, geography=True)
    objects = models.GeoManager()
    functions = TheatreManager()

    def __unicode__(self):
        return "{0} : {1}".format(self.tms_id, self.name)

class Movie(models.Model):
    tms_id = models.CharField(max_length=50, primary_key=True)
    alt_film_id = models.IntegerField()
    root_id = models.IntegerField()
    version_id = models.IntegerField()
    connect_id = models.CharField(max_length=50)
    run_time = models.CharField(max_length=50)
    program_type = models.CharField(max_length=200)
    color_code = models.CharField(max_length=50)
    original_audio_language = models.CharField(max_length=10)
    name10 = models.CharField(max_length=10, null=True)
    name20 = models.CharField(max_length=20, null=True)
    name40 = models.CharField(max_length=40, null=True)
    name = models.CharField(max_length=120, null=True) #default name field
    objects = models.GeoManager()
    functions = MovieManager()
 
class TheatreMovie(models.Model):
    movie_id = models.CharField(max_length=50)
    date = models.DateField()
    theatre = models.ForeignKey(Theatre)
    time = models.TimeField()
    bargin = models.BooleanField(default=False)
    qualifiers = models.CharField(max_length=300, null=True)
    showtime = models.DateTimeField(null=True)
    objects = models.GeoManager()
    functions = TheatreMovieManager()

    class Meta:
        #unique_together = ("movie_id", "theatre", "date", "time", "qualifiers")
        index_together = [
                            ["movie_id", "theatre", "date", "time", "qualifiers"],
                         ]   
    def __unicode__(self):
        return "{0}--{1}--{2}--{3}".format(self.movie_id, self.theatre_id, self.time)
   
