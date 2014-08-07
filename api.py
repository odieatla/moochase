from tastypie.resources import ModelResource
from tastypie.constants import ALL
from whatever.models import Whatever
from xmlparser.models import Theatre
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection


class WhateverResource(ModelResource):
    class Meta:
        queryset = Whatever.objects.all()
        resource_name = 'whatever'
        filtering = { "title" : ALL }
class TheatreResource(ModelResource):
    class Meta:
        #queryset = Theatre.objects.all()
        #lat = bundle.request.GET('lat')
        #lon = bundle.request.GET('lon')
        #queryset = Theatre.objects.filter(geog__dwithin=(GEOSGeometry('POINT(-97.309990 30.111199)'), D(m=5000)))
        #queryset = Theatre.objects.filter(geog__dwithin=(GEOSGeometry('POINT({0} {1})'.format(lon, lat)), D(m=5000)))
        #resource_name = 'theatre'
        filtering = {
            "lat" : "exact",
            "lon" : "exact"
        }
class TestResource(ModelResource):
    class Meta:
        queryset = Theatre.objects.all()
        #optional, if not provided, will be generated off the classname
        #resource_name = "test"
        allowed_methods = ['get']
        filtering = {
            "lat": "exact",
            "lon": "exact",
            "rang": "exact"
        }

    def dehydrate(self, bundle):
        response_data = {}
        response_data['showtimes'] = []
        lat = bundle.request.GET['lat']
        lon = bundle.request.GET['lon']
        rang = int(bundle.request.GET['range']) * 1600

        cursor = connection.cursor()
        cursor.execute("""
            select
                t.tms_id as theatre_id,
                t.name as theatre_name,
                m.tms_id as movie_id,
                m.name as movie_name,
                tm.showtime as showtime,
                ST_Distance(geog, ST_GeographyFromText('Point({0} {1})'))/1600 as distance
            from xmlparser_theatre t
            inner join xmlparser_theatremovie tm on t.tms_id = tm.theatre_id
            inner join xmlparser_movie m on m.tms_id = tm.movie_id
            where
                ST_DWithin(t.geog, ST_GeographyFromText('Point({0} {1})'), {2})
                and
                tm.showtime > timezone('PDT',now()) and tm.showtime < timezone('PDT', now()) + interval '3 hour'
            order by
                distance, tm.showtime
        """.format(lon, lat, rang))
        showtimes = cursor.fetchall()
        columns = ['theatre_id', 'theatre_name', 'movie_id', 'movie_name', 'showtime', 'distance']

        for showtime in showtimes:
            ss = {}
            for i, s in enumerate(showtime):
                if not isinstance(s, str):
                    s = str(s)
                    #ss.append(s)
                    ss[columns[i]] = s
            response_data['showtimes'].append(ss)
        return response_data['showtimes']
