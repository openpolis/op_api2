from django.conf.urls import url
from django.conf import settings
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, Resource
from politici.models import OpLocation, OpLocationType, OpProfession, OpResources, OpPolitician, OpResourcesType, OpEducationLevel, OpInstitutionCharge, OpPoliticalCharge, OpOrganizationCharge, OpInstitution


class LocationTypeResource(ModelResource):
    class Meta:
        queryset = OpLocationType.objects.using('politici').all()
        resource_name = 'tipi_territori'
        allowed_methods = ['get',]
        filtering = {
            'name': ALL,
        }

class LocationResource(ModelResource):
    location_type = fields.ForeignKey(LocationTypeResource, 'location_type', full=True)
    class Meta:
        queryset = OpLocation.objects.using('politici').all()
        resource_name = 'territori'
        allowed_methods = ['get',]
        filtering = {
            'location_type': ALL_WITH_RELATIONS,
            'name': ALL,
        }




class EducationLevelResource(ModelResource):
    def get_resource_uri(self, bundle_or_obj):
        """
        Needs to work for through table and OpEducationLevel table
        """
        if bundle_or_obj.__class__.__name__ == 'OpPoliticianHasOpEducationLevel':
            return '/politici/v2/%s/%s/' % (self._meta.resource_name,bundle_or_obj.obj.education_level.pk)
        else:
            return '/politici/v2/%s/%s/' % (self._meta.resource_name,bundle_or_obj.obj.pk)
    class Meta:
        queryset = OpEducationLevel.objects.using('politici').all()
        resource_name = 'education_level'
        allowed_methods = ['get',]

class ProfessionResource(ModelResource):
    class Meta:
        queryset = OpProfession.objects.using('politici').all()
        resource_name = 'professioni'
        allowed_methods = ['get',]
        filtering = {
            'oid': ALL,
            'description': ALL,
            }


class ResourceTypeResource(ModelResource):
    class Meta:
        queryset = OpResourcesType.objects.using('politici').all()
        resource_name = 'denominazione'
        allowed_methods = ['get', ]


class ResourceResource(ModelResource):
    resource_type = fields.ForeignKey(ResourceTypeResource, 'resources_type', full=True)
    def get_resource_uri(self, bundle_or_obj):
        return '/politici/v2/%s/%s/' % (self._meta.resource_name,bundle_or_obj.obj.content.pk)

    class Meta:
        queryset = OpResources.objects.using('politici').all()
        resource_name = 'risorse'
        allowed_methods = ['get', ]



class ChargeResource(ModelResource):
    politician = fields.ForeignKey('politici.v2.api.PoliticianResource', 'politician', full=True)
    textual_rep = fields.CharField('getTextualRepresentation', readonly=True, null=True)
    def get_resource_uri(self, bundle_or_obj):
        return '/politici/v2/%s/%s/' % (self._meta.resource_name,bundle_or_obj.obj.content.pk)

    class Meta:
        allowed_methods = ['get', ]

class InstitutionResource(ModelResource):

    class Meta:
        queryset = OpInstitution.objects.using('politici').all()
        resource_name = 'istituzioni'
        excludes = ['priority',]
        allowed_methods = ['get']

class InstitutionChargeResource(ChargeResource):
    textual_rep = fields.CharField('getExtendedTextualRepresentation', readonly=True, null=True)
    location = fields.ForeignKey(LocationResource, 'location', null=True)
    class Meta(ChargeResource.Meta):
        queryset = OpInstitutionCharge.objects.using('politici').all()
        resource_name = 'cariche_istituzionali'
        filtering = {
            'date_end': ALL,
            'location': ALL_WITH_RELATIONS,
        }

class PoliticalChargeResource(ChargeResource):
    location = fields.ForeignKey(LocationResource, 'location', null=True)
    class Meta(ChargeResource.Meta):
        queryset = OpPoliticalCharge.objects.using('politici').all()
        resource_name = 'cariche_politiche'

class OrganizationChargeResource(ChargeResource):
    class Meta(ChargeResource.Meta):
        queryset = OpOrganizationCharge.objects.using('politici').all()
        resource_name = 'cariche_organizzazioni'

class PoliticianResource(ModelResource):
    profession = fields.ForeignKey(ProfessionResource, 'profession', null=True)
    education_levels = fields.ToManyField(EducationLevelResource, 'oppoliticianhasopeducationlevel_set', null=True)
    resources = fields.ToManyField(ResourceResource, 'opresources_set', null=True)
    institution_charges = fields.ToManyField(InstitutionChargeResource, 'opinstitutioncharge_set', null=True)
    political_charges = fields.ToManyField(PoliticalChargeResource, 'oppoliticalcharge_set', null=True)
    organization_charges = fields.ToManyField(OrganizationChargeResource, 'oporganizationcharge_set', null=True)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(PoliticianResource, self).build_filters(filters)

        if "territorio" in filters:
            # filtro per territorio
            orm_filters['opinstitutioncharge__location__pk'] = filters["territorio"]
        elif "tipo_territorio" in filters:
            orm_filters['opinstitutioncharge__location__location_type_id'] = filters['tipo_territorio']

        if "data" in filters:
            if filters['data'] != 'all':
                orm_filters['opinstitutioncharge__date_end__gte'] = filters['data']
                orm_filters['opinstitutioncharge__date_start__lte'] = filters['data']
        else:
            orm_filters['opinstitutioncharge__date_end__isnull'] = True

        if "istituzione" in filters:
            orm_filters['opinstitutioncharge__institution__pk'] = filters['istituzione']

        if "tipo_carica" in filters:
            orm_filters['opinstitutioncharge__charge_type_id'] = filters['tipo_carica']

        return orm_filters

    class Meta:
        queryset = OpPolitician.objects.using('politici').distinct()
        resource_name = 'politici'
        allowed_methods = ['get',]

from tastypie.exceptions import NotFound
from django.db.models import Count

class DeputiesResource(Resource):

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):

        base_url = '/politici/v2/politici/?format=json&territorio=%s' % bundle_or_obj.obj.pk

#        charge_type
#        1 Presidente
#        2 Vicepresidente
#        3 Commissario
#        4 Presidente di commissione
#        5 Deputato
#        6 Senatore
#        7 Presidente del Consiglio
#        8 Vicepresidente del Consiglio
#        9 Ministro
#        10 Viceministro
#        11 Sottosegretario
#        12 Assessore
#        13 Consigliere
#        14 Sindaco
#        15 Vicesindaco
#        16 Commissario straordinario
#        17 iscritto
#        18 carica
#        19 Presidente della Repubblica
#        20 Senatore a vita
#        21 Candidato per le Politiche del 2008

#        institutions
#        1 Commissione Europea
#        2 Parlamento Europeo
#        3 Governo Nazionale
#        4 Camera dei Deputati
#        5 Senato della Repubblica
#        6 Giunta Regionale
#        7 Consiglio Regionale
#        8 Giunta Provinciale
#        9 Consiglio Provinciale
#        10 Giunta Comunale
#        11 Consiglio Comunale
#        12 Commissariamento
#        13 Presidenza della Repubblica


        deputati_url = "%s&tipo_carica=%s" % (base_url, 5)
        senatori_url = "%s&tipo_carica=%s" % (base_url, 6)

        istituti = OpInstitution.objects.using('politici')

        data = {
            'Parlamento Europeo': "%s&istituzione=%s" % ( deputati_url, 2 ),
            'Senato della Repubblica': "%s&istituzione=%s" % ( senatori_url, istituti.get(name='Senato della Repubblica').pk ),
            'Camera dei Deputati': "%s&istituzione=%s" % ( deputati_url, istituti.get(name='Camera dei Deputati').pk ),
            'Giunta Regionale' : '',
            'Consiglio Regionale' : '',
            'Giunta Provinciale' : '',
            'Consiglio Provinciale' : '',
            'Giunta Comunale' : '',
            'Consiglio Comunale' : '',
        }


#        istituzioni = OpInstitution.objects.using('politici')\
#                        .order_by('priority')\
#                        .filter(
#                            opinstitutioncharge__date_end__isnull=True,
#                            opinstitutioncharge__politician__death_date__isnull=True,
#                        ).annotate(c=Count('opinstitutioncharge'))
#
#        if not bundle_or_obj:
#            return istituzioni.all()

        data = {}

        for istituzione in OpInstitution.objects.using('politici').order_by('priority'):
            data[istituzione.name] = "%s&istituzione=%s" % (base_url,istituzione.pk)

        return data
#        return url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail")
#        (r'^rappresentanti/(?P<location>[\w_\.-]+)/', include(entry_point_resource.urls)),

    def obj_get_list(self, request=None, **kwargs):
        # inner get of object list... this is where you'll need to
        # fetch the data from what ever data source
        raise NotFound("Scegli un territorio per vedere i suoi rappresentanti")

    def obj_get(self, request = None, **kwargs):
        # get one object from data source
        pk = int(kwargs['pk'])
        try:
            return OpLocation.objects.using('politici').get(pk=pk)
        except KeyError:
            raise NotFound("Object not found")

    class Meta:
        resource_name = 'rappresentanti'
        queryset = OpLocation.objects.using('politici').comuni()
        allowed_methods = ['get',]

