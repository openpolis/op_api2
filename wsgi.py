"""
WSGI config for open_aci project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys, site

# these constants depend on how the server machine is setup                                                                                                 
DOMAIN_ROOT = '/home/op/op_api2'
PROJECT_ROOT = os.path.join(DOMAIN_ROOT)
SITE_PACKAGES = '/home/python_envs/op_api2/lib/python2.7/site-packages'

## general setup logic                                                                                                                                      
# add virtualenv's ``site-packages`` dir to the Python path                                                                                                 
site.addsitedir(SITE_PACKAGES)

# prepend ``PROJECT_ROOT`` to the Python path                                                                                                               
if PROJECT_ROOT not in sys.path:
   sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_local")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
