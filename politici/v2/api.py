from django.db.models.query_utils import Q
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, Resource
from politici.models import OpLocation, OpLocationType, OpProfession, OpResources, OpPolitician, OpResourcesType, OpEducationLevel, OpInstitutionCharge, OpPoliticalCharge, OpOrganizationCharge, OpInstitution
from tastypie.exceptions import NotFound

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
        excludes = ['priority','short_name']
        allowed_methods = ['get']
        ordering = ['priority']

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

    class Meta:
        queryset = OpPolitician.objects.using('politici').distinct()
        resource_name = 'politici'
        allowed_methods = ['get',]



class InstitutionChargesField(fields.OneToManyField):

    def dehydrate_related(self, bundle, related_resource):
        """
        Based on the ``full_resource``, returns either the endpoint or the data
        from ``full_dehydrate`` for the related resource.
        """
        return {
            'description': "%s %s" % (bundle.obj.institution.name, bundle.obj.getExtendedTextualRepresentation()),
            'institution_charge_uri': related_resource.get_resource_uri(bundle)
        }

    @classmethod
    def filtered_institution_charges(cls, bundle):

        if DeputiesResource._cached_politician_charges is None:
            DeputiesResource._cached_politician_charges = {}

            related_filters = DeputiesResource.build_prefixed_filters( bundle.request.GET )
            # fill all extracted politician id to avoid multiple big queries
            related_filters['politician_id__in'] = DeputiesResource._cached_politician_ids

            query = None

            if 'custom' in related_filters:
                custom = related_filters.pop('custom')
                query = OpInstitutionCharge.objects.using('politici').filter(custom, **related_filters )
            else:
                query = OpInstitutionCharge.objects.using('politici').filter( **related_filters )
            # init cache for politician charges
            for charge in query:
                if charge.politician_id not in DeputiesResource._cached_politician_charges:
                    DeputiesResource._cached_politician_charges[charge.politician_id] = []
                DeputiesResource._cached_politician_charges[charge.politician_id].append(charge)



#        related_filters = DeputiesResource.build_prefixed_filters( bundle.request.GET )
#
#        if 'custom' in related_filters:
#            custom = related_filters.pop('custom')
#            return bundle.obj.opinstitutioncharge_set.filter(custom, **related_filters )
#        else:
#            return bundle.obj.opinstitutioncharge_set.filter( **related_filters )

class DeputiesResource(ModelResource):


#    institution_charges = InstitutionChargesField(InstitutionChargeResource, lambda bundle: InstitutionChargesField.filtered_institution_charges(bundle), null=True)

    @classmethod
    def build_prefixed_filters(cls, filters, prefix=''):

        orm_filters = {}

        if "data" not in filters:
            orm_filters['{0}date_end__isnull'.format(prefix)] = True
        elif filters['data'] != 'all':
            orm_filters['{0}date_end__gte'.format(prefix)] = filters['data']
            orm_filters['{0}date_start__lte'.format(prefix)] = filters['data']


        if "territorio" in filters:
            try:
                city = OpLocation.objects.using('politici').comuni().get(pk=filters['territorio'])
#                provincia = OpLocation.objects.using('politici').province().get(pk=filter['territorio'])
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
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
            return self.get_object_list(request).filter(custom ,**applicable_filters)
        else:
            return self.get_object_list(request).filter(**applicable_filters)

    def alter_list_data_to_serialize(self, request, data):

        # takes all politician id
        politician_ids = [o.obj.content_id for o in data['objects']]

        related_filters = DeputiesResource.build_prefixed_filters( request.GET )
        # fill all extracted politician id to avoid multiple big queries
        related_filters['politician_id__in'] = politician_ids

        args_filters = []
        if 'custom' in related_filters:
            args_filters.append( related_filters.pop('custom') )

        related_resource = InstitutionChargeResource()

        for charge in OpInstitutionCharge.objects.using('politici').filter(*args_filters, **related_filters ).select_related(
            'constituency', 'location', 'party', 'charge_type', 'institution', 'content', 'group'
        ):
            for obj in data['objects']:
                print obj.obj.content_id
                if obj.obj.content_id == charge.politician_id:
                    if 'institution_charges' not in obj.data:
                        print 'init charges for %s' % obj.obj
                        obj.data['institution_charges'] = []
                    obj.data['institution_charges'].append({
                        'description': "%s %s" % (charge.institution.name, charge.getExtendedTextualRepresentation()),
                        'institution_charge_uri': related_resource.get_resource_uri( self.build_bundle(charge))
                    })

        return data
#    _cached_politician_ids= []
#    _cached_politician_charges= None
#    def build_bundle(self, obj=None, data=None, request=None):
#        # add to cache the politician id found
#        DeputiesResource._cached_politician_ids.append(obj.pk)
#
#        return super(DeputiesResource, self).build_bundle(obj, data, request)
#
#    def full_dehydrate(self, bundle):
#        """
#        Given a bundle with an object instance, extract the information from it
#        to populate the resource.
#        """
#        # Dehydrate each field.
#        for field_name, field_object in self.fields.items():
#            # A touch leaky but it makes URI resolution work.
#            if getattr(field_object, 'dehydrated_type', None) == 'related':
#                field_object.api_name = self._meta.api_name
#                field_object.resource_name = self._meta.resource_name
#
#            bundle.data[field_name] = field_object.dehydrate(bundle)
#
#            # Check for an optional method to do further dehydration.
#            method = getattr(self, "dehydrate_%s" % field_name, None)
#
#            if method:
#                bundle.data[field_name] = method(bundle)
#
#        bundle = self.dehydrate(bundle)
#        return bundle
#
#
#    def get_list(self, request, **kwargs):
#        """
#        Returns a serialized list of resources.
#
#        Calls ``obj_get_list`` to provide the data, then handles that result
#        set and serializes it.
#
#        Should return a HttpResponse (200 OK).
#        """
#        # TODO: Uncached for now. Invalidation that works for everyone may be
#        #       impossible.
#        objects = self.obj_get_list(request=request, **self.remove_api_resource_names(kwargs))
#        sorted_objects = self.apply_sorting(objects, options=request.GET)
#
#        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_list_uri(), limit=self._meta.limit)
#        to_be_serialized = paginator.page()
#
#        # Dehydrate the bundles in preparation for serialization.
#        bundles = [self.build_bundle(obj=obj, request=request) for obj in to_be_serialized['objects']]
#        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
#        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
#        return self.create_response(request, to_be_serialized)


    class Meta:
        resource_name = 'rappresentanti'
        queryset = OpPolitician.objects.using('politici').distinct().all()
        ordering = ['last_name', 'first_name', 'birth_date']
        allowed_methods = ['get',]
        fields = ['first_name', 'last_name', 'birth_date', 'birth_location', 'sex']

