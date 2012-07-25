from django.db.models.aggregates import Count
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.constants import ALL
from tastypie.resources import Resource, ModelResource
from parlamento.models import OppActHistoryCache


class CacheDateObject(object):
    """
    Object needed to buile api results.
    Represents a cache date, that's a date when cached records were stored in the table
    """
    def __init__(self):
        self.__dict__['_data'] = {}

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data

class ActCacheDatesResource(Resource):
    """
    Resource class representing a cache date (see CacheDateObject).
    References CacheDateObject for internal usage.
    """
    data = fields.DateField(attribute='data')
    data_count = fields.IntegerField(attribute='data_count', default=0)
    acts_url = fields.CharField(attribute='acts_url')

    class Meta:
        resource_name = 'history/dates'
        include_resource_uri = False
        object_class = CacheDateObject
        allowed_methods = ['get']
        ordering = ['data',]

    def get_object_list(self, request):
        queryset = OppActHistoryCache.objects.using('parlamento').values('data').annotate(Count('data')).order_by('-data')
        results = []
        for r in queryset:
            new_obj = self._meta.object_class()
            new_obj.data = r['data']
            new_obj.data_count = r['data__count']
            new_obj.acts_url = "/parlamento/{0}/history/acts?data__exact={1}&format=json".format(
                self._meta.api_name,
                r['data']
            )
            results.append(new_obj)
        return results

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        return CacheDateObject()


class ActCacheResource(ModelResource):
    class Meta:
        queryset = OppActHistoryCache.objects.using('parlamento')
        resource_name = 'history/acts'
        allowed_methods = ['get']
        ordering = ('indice',)
        filtering = {
            'data': ALL,
        }
        ordering = ['indice',]

