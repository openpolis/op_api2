from django.conf.urls import patterns, include
from tastypie.api import Api

from territori.v2.api import LocationResource, LocationTypeResource

v2_api = Api(api_name='v2')
v2_api.register(LocationResource())
v2_api.register(LocationTypeResource())

urlpatterns = patterns('',
    (r'^', include(v2_api.urls)),
)
