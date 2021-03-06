from django.db.models.query_utils import Q
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from territori.models import OpLocation, OpLocationType
from politici.models import OpProfession, OpResources, OpPolitician, OpResourcesType, OpEducationLevel, OpInstitutionCharge, OpPoliticalCharge, OpOrganizationCharge, OpInstitution, OpChargeType
from tastypie.exceptions import NotFound
from api_auth import PrivateResourceMeta

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
        include_resource_uri = False


class ProfessionResource(ModelResource):
    class Meta(PrivateResourceMeta):
        queryset = OpProfession.objects.using('politici').all()
        resource_name = 'professioni'
        allowed_methods = ['get',]
        filtering = {
            'oid': ALL,
            'description': ALL,
            }
        include_resource_uri = False


class ResourceTypeResource(ModelResource):
    class Meta(PrivateResourceMeta):
        queryset = OpResourcesType.objects.using('politici').all()
        resource_name = 'denominazione'


class ResourceResource(ModelResource):
    description = fields.CharField('descrizione', null=True)
    type = fields.CharField('resources_type__denominazione', null=True)
    external_uri = fields.CharField('valore', null=True)

#    resource_type = fields.ForeignKey(ResourceTypeResource, 'resources_type', full=True)
#    def get_resource_uri(self, bundle_or_obj):
#        return '/politici/v2/%s/%s/' % (self._meta.resource_name,bundle_or_obj.obj.content.pk)

    class Meta(PrivateResourceMeta):
        queryset = OpResources.objects.using('politici').all()
        resource_name = 'risorse'
        include_resource_uri = False
        excludes = ['descrizione','valore'] # rename above

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
        ordering = ['priority']
        include_resource_uri = False


class ChargeTypeResource(ModelResource):

    def dehydrate(self, bundle):
        # add uri to list of rappresentanti filtered by tipo_carica
        bundle.data['rappresentanti_uri'] = "%s?tipo_carica=%s" % (
            self._build_reverse_url("api_dispatch_list", kwargs={
                'resource_name': DeputiesResource.Meta.resource_name,
                'api_name': self._meta.api_name,
                }),
            bundle.obj.pk
            )
        return bundle

    class Meta(PrivateResourceMeta):
        queryset = OpChargeType.objects.using('politici').all()
        resource_name = 'cariche'
        include_resource_uri = False
        ordering = ['priority']
        excludes = ['priority']


class ChargeResource(ModelResource):
    id = fields.IntegerField('pk')
    textual_rep = fields.CharField('getTextualRepresentation', readonly=True, null=True)

    def get_resource_uri(self, bundle_or_obj):
        return '/politici/v2/%s/%s/' % (getattr(self,'_meta').resource_name,bundle_or_obj.obj.content.pk)


class LocalizedChargeResource(ChargeResource):
    charge_type = fields.ForeignKey(ChargeTypeResource, 'charge_type', null=True, full=True)
    location = fields.ForeignKey('territori.v2.api.LocationResource', 'location', null=True)
    location_id = fields.IntegerField('location__pk', null=True)
    location_name = fields.CharField('location', null=True)

    def get_detail(self, request, **kwargs):

        self.fields['location'].full = True

        return super(LocalizedChargeResource, self).get_detail(request, **kwargs)


class InstitutionChargeResource(LocalizedChargeResource):
    politician = fields.ForeignKey('politici.v2.api.PoliticianResource', 'politician', full=True)
    textual_rep = fields.CharField('getExtendedTextualRepresentation', readonly=True, null=True)
    institution = fields.ForeignKey(InstitutionResource, 'institution', full=True)
    group = fields.CharField('group__name', readonly=True, null=True)
    party = fields.CharField('party__name', readonly=True, null=True)

    class Meta(PrivateResourceMeta):
        queryset = OpInstitutionCharge.objects.using('politici').all()
        resource_name = 'cariche_istituzionali'
        filtering = {
            'date_end': ALL,
            'location': ALL_WITH_RELATIONS,
            'charge_type': ALL,
            }


class PoliticalChargeResource(LocalizedChargeResource):
    politician = fields.ForeignKey('politici.v2.api.PoliticianResource', 'politician', full=True)
    party = fields.CharField('party__name', readonly=True, null=True)

    class Meta(PrivateResourceMeta):
        queryset = OpPoliticalCharge.objects.using('politici').all()
        resource_name = 'cariche_politiche'
        filtering = {
            'date_end': ALL,
            'location': ALL_WITH_RELATIONS,
            'charge_type': ALL,
        }


class OrganizationChargeResource(ChargeResource):
    politician = fields.ForeignKey('politici.v2.api.PoliticianResource', 'politician', full=True)
    class Meta(PrivateResourceMeta):
        queryset = OpOrganizationCharge.objects.using('politici').all()
        resource_name = 'cariche_organizzazioni'
        filtering = {
            'date_end': ALL,
            'charge_name': ALL,
        }


class PoliticianResource(ModelResource):
    profession = fields.ForeignKey(ProfessionResource, 'profession', null=True)
    education_levels = fields.ToManyField(EducationLevelResource, 'oppoliticianhasopeducationlevel_set', null=True)
    resources = fields.ToManyField(ResourceResource, 'opresources_set', null=True)
    institution_charges = fields.ToManyField(InstitutionChargeResource, 'opinstitutioncharge_set', null=True)
    political_charges = fields.ToManyField(PoliticalChargeResource, 'oppoliticalcharge_set', null=True)
    organization_charges = fields.ToManyField(OrganizationChargeResource, 'oporganizationcharge_set', null=True)

    def get_detail(self, request, **kwargs):
        """
        display more information on detail request
        """

        self.fields['profession'].full = True
        self.fields['resources'].full = True

        for charge_type in ['institution_charges', 'political_charges', 'organization_charges']:

            self.fields[charge_type].full = True
            # remove politician to avoid recursion
            if 'politician' in self.fields[charge_type].to.base_fields:
                del self.fields[charge_type].to.base_fields['politician']
            elif 'politician' in self.fields[charge_type].to.declared_fields:
                del self.fields[charge_type].to.declared_fields['politician']


        return super(PoliticianResource, self).get_detail(request, **kwargs)

    def dehydrate(self, bundle):

        # build a fullname
        bundle.data['full_name'] = unicode(bundle.obj)

        if bundle.data['education_levels']:
            bundle.data['education_levels'] = []
            for educationLevel in bundle.obj.oppoliticianhasopeducationlevel_set.all():
                bundle.data['education_levels'].append( {
                    'name': educationLevel.education_level.getNormalizedDescription(),
                    'description': educationLevel.description,
                    } )

        if bundle.data['profession']:
            bundle.data['profession'] = {
                'name': bundle.obj.profession.description,
                'description': bundle.obj.profession.getNormalizedDescription(),
            }

        return bundle

    class Meta(PrivateResourceMeta):
        queryset = OpPolitician.objects.using('politici').distinct()
        resource_name = 'politici'
        excludes = ['is_indexed',]


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
            istituzione_pks = filters['istituzione'].split(',')
            if len(istituzione_pks) == 1:
                orm_filters['{0}institution_id'.format(prefix)] = istituzione_pks[0]
            else:
                orm_filters['{0}institution_id__in'.format(prefix)] = istituzione_pks

        if "tipo_carica" in filters:
            tipo_carica_pks = filters['tipo_carica'].split(',')
            if len(tipo_carica_pks) == 1:
                orm_filters['{0}charge_type_id'.format(prefix)] = tipo_carica_pks[0]
            else:
                orm_filters['{0}charge_type_id__in'.format(prefix)] = tipo_carica_pks

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

        # args_filters may contains a Q objects
        args_filters = []
        if 'custom' in related_filters:
            args_filters.append( related_filters.pop('custom') )
        if 'custom_date' in related_filters:
            args_filters.extend( related_filters.pop('custom_date') )

        related_resource = InstitutionChargeResource()

        for charge in OpInstitutionCharge.objects.using('politici').filter(*args_filters, **related_filters ).select_related(
            'constituency', 'location', 'party', 'charge_type', 'institution', 'content', 'group'
        ):
            for bundle in data['objects']:

                # build a fullname
                bundle.data['full_name'] = unicode(bundle.obj)

                if bundle.obj.content_id == charge.politician_id:
                    # initialize institution charges for this politician
                    if 'institution_charges' not in bundle.data: bundle.data['institution_charges'] = []

                    # remove politician to avoid recursion
                    if 'politician' in related_resource.fields:
                        del related_resource.fields['politician']
                    elif 'politician' in related_resource.declared_fields:
                        del related_resource.declared_fields['politician']

                    charge_bundle = related_resource.build_bundle(obj=charge, request=request)
                    bundle.data['institution_charges'].append( related_resource.full_dehydrate( charge_bundle ) )

        return data

    def get_detail(self, request, **kwargs):
        """
        volontariamente lasciato implementato
        n singolo rappresentante deve essere visualizzato attraverso i politici
        """
        raise NotImplementedError("Errore, risorsa sconosciuta")


    class Meta():
        resource_name = 'rappresentanti'
        queryset = OpPolitician.objects.using('politici').distinct().all()
        ordering = ['last_name', 'first_name', 'birth_date']
        excludes = ['is_indexed','death_date']
        filtering = {
            'birth_date': ALL,
            'sex': ('exact',),
            'last_name': ALL,
            'first_name': ALL,
            'death_date': ALL,
        }
#        fields = ['first_name', 'last_name', 'birth_date', 'birth_location', 'sex']

