from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization


class PrivateResourceMeta():

    authentication = BasicAuthentication()
    authorization = DjangoAuthorization()
    allowed_methods = ['get',]