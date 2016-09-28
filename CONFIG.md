# Configuration guide

## Endpoints
The most important things that can be customized are endpoints about Keystone and Keypass.
Some specific operations involve calls to others endpoints like Orion, Iota or Perseo.
And there are others endpoints that are not invoked but are keept to use into Orion subscriptions like STH, Perseo and Cygnus.



By default in [settings/common.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/common.py) endpoints are set to:
```
KEYSTONE = {}
KEYPASS = {}
IOTA = {}
ORION = {}
CA = {}
PEP_PERSEO = {}
STH = {}
PERSEO = {}
CYGNUS = {}
```

Tipically are fixed in [settings/dev.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/dev.py) like
```
KEYSTONE = {
    "host": "localhost",
    "port": "5001",
    "protocol":"http"
}

KEYPASS = {
    "host": "localhost",
    "port": "7070",
    "protocol":"http"
}

IOTA = {
    "host": "localhost",
    "port": "4052",
    "protocol":"http"
}

ORION = {
    "host": "localhost",
    "port": "1026",
    "protocol":"http"
}

CA = {
    "host": "localhost",
    "port": "9999",
    "protocol":"http"
}

PEP_PERSEO = {
    "host": "localhost",
    "port": "9090",
    "protocol":"http",
}
```

These other endpints are just keept to use with Orion subscriptions about IoT Modules:

```
STH = {
    "host": "localhost",
    "port": "18666",
    "protocol":"http",
    "notifypath":"/notify"
}

PERSEO = {
    "host": "localhost",
    "port": "19090",
    "protocol":"http",
    "notifypath":"/notices"
}

CYGNUS = {
    "host": "localhost",
    "port": "5050",
    "protocol":"http",
    "notifypath":"/notify"
}
IOTMODULES = [ "CYGNUS", "PERSEO" ]
```

## Logging

By default logging configuration is defined in [settings/common.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/common.py) like this:

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "time=%(asctime)s | lvl=%(levelname)s | op=%(name)s:%(lineno)s | msg=%(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/orchestrator/' + "/orchestrator.log",
            'maxBytes': 1024*1024*5, # 5Mb
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'orchestrator_api': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'orchestrator_core': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}
```

There is a easy way to change log level using configuration files. Just adding to [settings/dev.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/dev.py)

```
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['handlers']['logfile']['level'] = 'DEBUG'
LOGGING['loggers']['orchestrator_api']['level'] = 'DEBUG'
LOGGING['loggers']['orchestrator_core']['level'] = 'DEBUG'
```


## Throttling

By default throlling is configured for all orchestrator API in [settings/common.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/common.py) to 200 request by second.

```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/sec',
    }
}
```

This value could be modified just adding to [settings/dev.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/dev.py)

```
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon']='30/sec'
```


### WSGI server options

For an installation which uses Orchestrator RPM, there is a file in /etc/default/orchestrator-daemon to setup orchestrator port as well as number of process and threads sused by WSGI server.

By default the content of that file is:

```
VIRTUALENV=/var/env-orchestrator
ORCHESTRATOR_DIR=${VIRTUALENV}/lib/python2.6/site-packages/iotp-orchestrator
UWGSI=uwsgi
PORT=8084
STATS_PORT=8085
PROCESSES=1
THREADS=4
ENVIRONMENT="DJANGO_SETTINGS_MODULE=settings.dev"
PIDFILE="/var/run/orchestrator.pid"
PNAME="orchestrator"
USER="orchestrator"
```


## Environment users

There are some users needed to to perform some operations related with trust tokens. For that it needed to keep some configuration about that users in [settings/common.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/common.py) and by default is:


```
PEP = {
    "user": "pep",
    "password": "pep"
}

IOTAGENT = {
    "user": "iotagent",
    "password": "iotagent"
}
```

This value could be overwrite just adding right values to [settings/dev.py](https://github.com/telefonicaid/orchestrator/blob/develop/src/settings/dev.py)

```
PEP = {
    "user": "pep_user",
    "password": "pep_password"
}

IOTAGENT = {
    "user": "iotagent_user",
    "password": "iotagent_password"
}
```
