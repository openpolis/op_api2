from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# api and admin urls
urlpatterns = patterns('',
    (r'^politici/', include('politici.urls')),
    (r'^parlamento/', include('parlamento.urls')),
    (r'^territori/', include('territori.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)


