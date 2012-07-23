from django.conf.urls import patterns, include
from tastypie.api import Api

from op.v1.api import LocationResource, LocationTypeResource, ProfessionResource, PoliticianResource, ResourceResource,\
EducationLevelResource, InstitutionChargeResource, PoliticalChargeResource, OrganizationChargeResource

v1_api = Api(api_name='v1')
v1_api.register(LocationResource())
v1_api.register(LocationTypeResource())
v1_api.register(PoliticianResource())
v1_api.register(ProfessionResource())
v1_api.register(EducationLevelResource())
v1_api.register(ResourceResource())
v1_api.register(InstitutionChargeResource())
v1_api.register(PoliticalChargeResource())
v1_api.register(OrganizationChargeResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)