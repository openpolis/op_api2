from django.conf.urls import url
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
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
        queryset = OpPolitician.objects.using('politici').all()
        resource_name = 'politici'
        allowed_methods = ['get',]
