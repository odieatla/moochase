from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api import WhateverResource, TheatreResource, TestResource

from django.contrib import admin
admin.autodiscover()

whatever_resource = WhateverResource()
theatre_resource = TheatreResource()
test_resource = TestResource()

v1_api = Api(api_name='v1')
v1_api.register(WhateverResource())
v1_api.register(TheatreResource())
v1_api.register(TestResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django15.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^api/', include(whatever_resource.urls)),
    #url(r'^api/', include(theatre_resource.urls)),
    #url(r'^api/', include(test_resource.urls)),
    url(r'^api/', include(v1_api.urls)),

    #url(r'^api/test_showtime\?lat=([-+]?[0-9]*\.?[0-9]*)\&lon=([-+]?[0-9]*\.?[0-9]*)$', 'xmlparser.views.theatres_test'),
    #url(r'^api/test_showtime/$', 'xmlparser.views.theatres_test'),
    #url(r'^api/theatres/all/$', 'xmlparser.views.theatres_all'),
    #url(r'^api/theatres/nearby/$', 'xmlparser.views.theatres_nearby'),
    #url(r'^api/showtimes/nearby/$', 'xmlparser.views.showtimes_nearby'),

    url(r'^admin/', include(admin.site.urls)),
)
