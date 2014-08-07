from django.shortcuts import render
from django.db import transaction, connection
import json
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from .models import *
import decimal
import logging
from django.contrib.gis.geos import fromstr

logger = logging.getLogger(__name__)

# Create your views here.
#def theatres_test(request, lat, lon):
def theatres_test(request):
    response_data = {}
    #lat = str(request.GET.get('lat'))
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    print "lat : %s" % lat
    print "lon : %s" % lon
    logger.error(lat)
    logger.error(lon)

    #theatres = Theatre.objects.all()
    cursor = connection.cursor()

    #cursor.execute("select tms_id, name from xmlparser_theatre")
    cursor.execute("select tms_id, name from xmlparser_theatre where lat = {0}".format(lat))
    theatres = cursor.fetchall()
    response_data['theatre'] = theatres

    return HttpResponse(json.dumps(response_data), content_type="application/json")
    #return HttpResponse('<div>{0} {1}</div>'.format(lat, lon))

def theatres_all(request):
    response_data = {}
    response_data['theatres'] = []
    cursor = connection.cursor()
    columns = ['tms_id', 'name', 'lat', 'lon', 'zip']
    cursor.execute("select {0} from xmlparser_theatre where active = true".format(','.join(columns)))
    theatres = cursor.fetchall()

    for theatre in theatres:
        d = {}
        for i, t in enumerate(theatre):
            #if type(t) is decimal.Decimal:
            if type(t) is not str:
                t = str(t)
            d[columns[i]] = t
        response_data['theatres'].append(d)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def showtimes_nearby(request):
    response_data = {}
    response_data['showtimes'] = []
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    rang = int(request.GET.get('range')) * 1600

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

    for showtime in showtimes:
        ss = []
        for s in showtime:
            if not isinstance(s, str):
                s = str(s)
                ss.append(s)
        response_data['showtimes'].append(ss)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def theatres_nearby(request):
    response_data = {}
    response_data['theatres'] = []
    cursor = connection.cursor()
    columns = ['tms_id', 'name', 'chain', 'chain_code', 'zip']

    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    rang = request.GET.get('range')
    if rang is None:
        rang = 10

    pnt = fromstr('POINT({0} {1})'.format(lon, lat), srid=4326)
    theatres_query = Theatre.objects.filter(geom__distance_lte=(pnt, D(mi=rang))).filter(active__exact=True).distance(pnt).order_by('distance')
    theatres = []
    for t in theatres_query:
        tt = {}
        #for c in columns:
            #c = (str(c) if isinstance(c, str))
        #    if not isinstance(c, str):
        #        c = str(c)
        #    tt[c] = t[c]
        tt['tms_id'] = t.tms_id
        tt['distance'] = str(t.distance.mi)
        tt['name'] = t.name
        tt['chain'] = t.chain
        tt['chain_code'] = t.chain_code
        tt['zip'] = t.zip

        theatres.append(tt)

    response_data['theatres'] = theatres

    return HttpResponse(json.dumps(response_data), content_type="application/json")
