"""
WSGI config for orchestrator project.

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
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orchestrator.settings.dev")

from multiprocessing import Manager
manager = Manager()
shared_data = manager.dict()
shared_lock = manager.Lock()

from django.conf import settings
settings.SHARED_DATA = shared_data
settings.SHARED_LOCK = shared_lock

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



#
# Orchestrator startup
#
import orchestrator.core.startup as startup
startup.run()
