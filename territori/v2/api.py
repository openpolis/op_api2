from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from api_auth import PrivateResourceMeta
import politici.v2.api
from territori.models import OpLocation, OpLocationType


class LocationTypeResource(ModelResource):
    def dehydrate(self, bundle):
        # add uri to list of locations filtered by location_type
        bundle.data['territori_uri'] = "%s?location_type=%s" % (
            self._build_reverse_url("api_dispatch_list", kwargs={
                'resource_name': LocationResource.Meta.resource_name,
                'api_name': self._meta.api_name,
                }),
            bundle.obj.pk
            )

        return bundle

    class Meta(PrivateResourceMeta):
        queryset = OpLocationType.objects.using('politici').all()
        resource_name = 'tipi_territori'
        include_resource_uri = False
        filtering = {
            'name': ALL,
            }


class LocationResource(ModelResource):
    location_type = fields.ForeignKey(LocationTypeResource, 'location_type', full=True)

    def dehydrate(self, bundle):
        # build a fullname
        bundle.data['full_name'] = unicode(bundle.obj)

        # add uri to list of rappresentanti filtered by city
        if bundle.obj.location_type_id == OpLocation.CITY_TYPE_ID:
            bundle.data['rappresentanti_uri'] = "%s?territorio=%s" % (
                self._build_reverse_url("api_dispatch_list", kwargs={
                    'resource_name': politici.v2.api.DeputiesResource.Meta.resource_name,
                    'api_name': self._meta.api_name,
                    }),
                bundle.obj.pk
                )

        return bundle

    class Meta(PrivateResourceMeta):
        queryset = OpLocation.objects.using('politici').all()
        resource_name = 'territori'
        filtering = {
            'location_type': ALL_WITH_RELATIONS,
            'name': ALL,
            }
