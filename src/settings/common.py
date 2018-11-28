# Django settings for orchestrator project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('IoT support', 'iot_support@tid.es'),
)

MANAGERS = ADMINS

CACHE_BACKEND = 'locmem://'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to datqabase file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Encoding
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!yjt(4sb)uxjnn1yvred8x7^%2#!6rg&amp;eelh@g6w3o($tk&amp;!%d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'rest_framework',
)

"""
Simple logging: Use Sentry to improve logging

Handle it in modular settings like this:

    [settings/custom.py]
    LOGGING.update({
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO',
            },
            'extra_log': {
                ...
            }
        }
    })
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            #'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            #'format' : "time=%(asctime)s | lvl=%(levelname)s | op=%(name)s:%(lineno)s | component=Orchestrator | msg=%(message)s",
            'format' : 'time=%(asctime)s.%(msecs)03dZ | lvl=%(levelname)s | corr=%(correlator)s | trans=%(transaction)s | srv=%(service)s | subsrv=/%(subservice)s | comp=Orchestrator | op=%(name)s:%(funcName)s() | msg=%(message)s',
            'datefmt' : "%Y-%m-%dT%H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'INFO',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/orchestrator/' + "/orchestrator.log",
            'maxBytes': 25*1024*1024,  # 25 Mb
            'backupCount': 3,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'filters': ['require_debug_false'],
        #     'class': 'django.utils.log.AdminEmailHandler'
        # },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'orchestrator_api': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
        'orchestrator_core': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/sec',
    }
}




# Settings are splited into settings/common.py settings/dev.py 

# Custom settings
# ---------------
# The following values are tipically modified in custom config files, like dev.py


KEYSTONE = {}
KEYPASS = {}
ORION = {}
PEP_PERSEO = {}
STH = {}
PERSEO = {}
CYGNUS = {}
LDAP = {}
MAILER = {}
MONGODB = {}

# List of possible IoTModules: persistence services, etc
IOTMODULES = [ "CYGNUS", "STH", "PERSEO"]

# Pep user credencials. Pep is a user of admin_domain
# Needed to for resolve pep user id
PEP = {
    "user": "pep",
    "password": "pep"
}

# IoTAgent user credentials. Iotagent is a user of default domain
# Needed to for resolve iotagent user id
IOTAGENT = {
    "user": "iotagent",
    "password": "iotagent"
}

SCIM_API_VERSION = "1.1"  # Supported v1.1 (1.1) and v2.0 (2.0) (by UPM)

# Internal version of Orchestrator
ORC_VERSION = "ORC_version"

# Extend metrics
ORC_EXTENDED_METRICS = False
