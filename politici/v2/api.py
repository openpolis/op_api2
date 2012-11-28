from django.db.models.query_utils import Q
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from politici.models import OpLocation, OpLocationType, OpProfession, OpResources, OpPolitician, OpResourcesType, OpEducationLevel, OpInstitutionCharge, OpPoliticalCharge, OpOrganizationCharge, OpInstitution
from tastypie.exceptions import NotFound
from api_auth import PrivateResourceMeta



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
        allowed_methods = ['get',]
        include_resource_uri = False
        filtering = {
            'name': ALL,
        }


class LocationResource(ModelResource):
    location_type = fields.ForeignKey(LocationTypeResource, 'location_type', full=True)

    def dehydrate(self, bundle):
        # add uri to list of rappresentanti filtered by city
        if bundle.obj.location_type_id == OpLocation.CITY_TYPE_ID:
            bundle.data['rappresentanti_uri'] = "%s/?territorio=%s" % (
                self._build_reverse_url("api_dispatch_list", kwargs={
                    'resource_name': DeputiesResource.Meta.resource_name,
                    'api_name': self._meta.api_name,
                }),
                bundle.obj.pk
            )

        return bundle

    class Meta(PrivateResourceMeta):
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
    class Meta(PrivateResourceMeta):
        queryset = OpEducationLevel.objects.using('politici').all()
        resource_name = 'education_level'
        allowed_methods = ['get',]


class ProfessionResource(ModelResource):
    class Meta(PrivateResourceMeta):
        queryset = OpProfession.objects.using('politici').all()
        resource_name = 'professioni'
        allowed_methods = ['get',]
        filtering = {
            'oid': ALL,
            'description': ALL,
            }


class ResourceTypeResource(ModelResource):
    class Meta(PrivateResourceMeta):
        queryset = OpResourcesType.objects.using('politici').all()
        resource_name = 'denominazione'
        allowed_methods = ['get', ]


class ResourceResource(ModelResource):
    resource_type = fields.ForeignKey(ResourceTypeResource, 'resources_type', full=True)
    def get_resource_uri(self, bundle_or_obj):
        return '/politici/v2/%s/%s/' % (self._meta.resource_name,bundle_or_obj.obj.content.pk)

    class Meta(PrivateResourceMeta):
        queryset = OpResources.objects.using('politici').all()
        resource_name = 'risorse'
        allowed_methods = ['get', ]


class ChargeResource(ModelResource):
    id = fields.IntegerField('pk')
    politician = fields.ForeignKey('politici.v2.api.PoliticianResource', 'politician', full=True)
    textual_rep = fields.CharField('getTextualRepresentation', readonly=True, null=True)

    def get_resource_uri(self, bundle_or_obj):
        return '/politici/v2/%s/%s/' % (self._meta.resource_name,bundle_or_obj.obj.content.pk)

    class Meta(PrivateResourceMeta):
        allowed_methods = ['get', ]


class InstitutionResource(ModelResource):

    def dehydrate(self, bundle):

        bundle.data['rappresentanti_uri'] = "%s?istituzione=%s" % (
            self._build_reverse_url("api_dispatch_list", kwargs={
                'resource_name': DeputiesResource.Meta.resource_name,
                'api_name' : self._meta.api_name
            }),
            bundle.obj.pk
        )

        return bundle

    class Meta(PrivateResourceMeta):
        queryset = OpInstitution.objects.using('politici').all()
        resource_name = 'istituzioni'
        excludes = ['priority','short_name']
        allowed_methods = ['get']
        ordering = ['priority']


class InstitutionChargeResource(ChargeResource):
    textual_rep = fields.CharField('getExtendedTextualRepresentation', readonly=True, null=True)
    location = fields.CharField('location__name', null=True)
    location_id = fields.CharField('location__pk', null=True)
    institution = fields.ForeignKey(InstitutionResource, 'institution', full=True)
    group = fields.CharField('group__name', readonly=True, null=True)
    party = fields.CharField('party__name', readonly=True, null=True)
    charge_type = fields.CharField('charge_type__name', readonly=True, null=True)

    class Meta(ChargeResource.Meta):
        queryset = OpInstitutionCharge.objects.using('politici').all()
        resource_name = 'cariche_istituzionali'
        filtering = {
            'date_end': ALL,
            'location': ALL_WITH_RELATIONS,
        }


class PoliticalChargeResource(ChargeResource):
    location = fields.CharField('location__name', null=True)
    location_id = fields.CharField('location__pk', null=True)
    party = fields.CharField('party__name', readonly=True, null=True)
    charge_type = fields.CharField('charge_type__name', readonly=True, null=True)
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

    class Meta(PrivateResourceMeta):
        queryset = OpPolitician.objects.using('politici').distinct()
        resource_name = 'politici'
        allowed_methods = ['get',]


class DeputiesResource(ModelResource):

    @classmethod
    def build_prefixed_filters(cls, filters, prefix=''):

        orm_filters = {}

        # removes deleted
        orm_filters['{0}content__deleted_at__isnull'.format(prefix)] = True

        if "data" not in filters:
            orm_filters['{0}date_end__isnull'.format(prefix)] = True
        elif filters['data'] != 'all':
            orm_filters['custom_date'] = (
                # start_date is lower then ...
                Q(**{'{0}date_start__lte'.format(prefix): filters['data']}),
                # and date_end is greater then or null
                    Q(**{'{0}date_end__gte'.format(prefix): filters['data']}) |
                    Q(**{'{0}date_end__isnull'.format(prefix): True })
            )
#            orm_filters['{0}date_end__gte'.format(prefix)] = filters['data']
#            orm_filters['{0}date_start__lte'.format(prefix)] = filters['data']


        if "territorio" in filters:
            try:
                city = OpLocation.objects.using('politici').comune(filters['territorio'])
            except (OpLocation.DoesNotExist, OpLocation.MultipleObjectsReturned):
                raise NotFound("Invalid type of location")
            qset = (
                # consiglieri e assessori
                Q(**{'{0}location_id__in'.format(prefix): (
                    city.pk, # comunali
                    city.getProvince().pk, # provinciali
                    city.getRegion().pk # regionali
                )})
                # senato, camera e parlamento europeo
                | Q(**{'{0}constituency_id__in'.format(prefix): [l.id for l in city.getConstituencies()]})
                # governo nazionale e commissione europea
                | Q(**{'{0}institution_id__in'.format(prefix): [1,3]})
            )
            orm_filters.update({
                'custom': qset
            })

        if "istituzione" in filters:
            orm_filters['{0}institution_id'.format(prefix)] = filters['istituzione']

        if "tipo_carica" in filters:
            orm_filters['{0}charge_type_id'.format(prefix)] = filters['tipo_carica']

        return orm_filters

    def dehydrate(self, bundle):

        if bundle.obj.death_date:
            bundle.data['death_date'] = bundle.obj.death_date

        return bundle

    def build_filters(self, filters=None):

        orm_filters = super(DeputiesResource, self).build_filters(filters)

        orm_filters.update( self.build_prefixed_filters( filters , prefix='opinstitutioncharge__') )

        return orm_filters

    def apply_filters(self, request, applicable_filters):

        filter_args = []

        if 'custom' in applicable_filters: filter_args.append( applicable_filters.pop('custom') )
        if 'custom_date' in applicable_filters: filter_args.extend( applicable_filters.pop('custom_date') )

        return self.get_object_list(request).filter(*filter_args ,**applicable_filters)


    def get_resource_uri(self, bundle_or_obj):
        """
        Handles generating a resource URI for a single resource.

        Uses the model's ``pk`` in order to create the URI.
        """
        kwargs = {
            'resource_name': PoliticianResource.Meta.resource_name,
            }

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.pk
        else:
            kwargs['pk'] = bundle_or_obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

    def alter_list_data_to_serialize(self, request, data):

        # takes all politician id
        politician_ids = [o.obj.content_id for o in data['objects']]

        related_filters = DeputiesResource.build_prefixed_filters( request.GET )
        # fill all extracted politician id to avoid multiple big queries
        related_filters['politician_id__in'] = politician_ids

        args_filters = []
        if 'custom' in related_filters:
            args_filters.append( related_filters.pop('custom') )
        if 'custom_date' in related_filters:
            args_filters.extend( related_filters.pop('custom_date') )

        related_resource = InstitutionChargeResource()

        for charge in OpInstitutionCharge.objects.using('politici').filter(*args_filters, **related_filters ).select_related(
            'constituency', 'location', 'party', 'charge_type', 'institution', 'content', 'group'
        ):
            for obj in data['objects']:

                if obj.obj.content_id == charge.politician_id:

                    # initialize institution charges for this politician
                    if 'institution_charges' not in obj.data: obj.data['institution_charges'] = []

                    # add founded charge
                    obj.data['institution_charges'].append({
                        'description': "%s %s" % (charge.institution.name, charge.getExtendedTextualRepresentation()),
                        'institution_charge_uri': related_resource.get_resource_uri( self.build_bundle(charge))
                    })

        return data

    def get_detail(self, request, **kwargs):
        """
        volontariamente lasciato implementato
        n singolo rappresentante deve essere visualizzato attraverso i politici
        """
        raise NotImplementedError("Errore, risorsa sconosciuta")


    class Meta(PrivateResourceMeta):
        resource_name = 'rappresentanti'
        queryset = OpPolitician.objects.using('politici').distinct().all()
        ordering = ['last_name', 'first_name', 'birth_date']
        allowed_methods = ['get',]
        fields = ['first_name', 'last_name', 'birth_date', 'birth_location', 'sex']

