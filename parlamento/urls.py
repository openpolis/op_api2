from django.conf.urls import patterns, include
from tastypie.api import Api

from parlamento.v2.api import ActCacheResource, ActCacheDatesResource

v1_api = Api(api_name='v2')
v1_api.register(ActCacheResource())
v1_api.register(ActCacheDatesResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)