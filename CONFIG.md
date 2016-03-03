# Configuration guide

## Endpoints
The most important things that can be customized are endpoints of keystone and keypass

By default in [settings/common.py](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings/common.py) endpoints are set to:
```
KEYSTONE = {}
KEYPASS = {}
```

and tipically are fixed in [settings/dev.py](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings/dev.py) like
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
```

## Logging

By default logging configuration is defined in [settings/common.py](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings/common.py) like this:

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


## Throttling

By default throlling is configured for all orchestrator API in [settings/common.py](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings/common.py) to 200 request by second.

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

This value could be modified just adding to [settings/dev.py](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings/dev.py)

```
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon']='30/sec'
```
