# Configuration guide

## Endpoints
The most important things that can be customized are endpoints of keystone and keypass

By default in settings/common.py endpoints are:
```
KEYSTONE = {}
KEYPASS = {}
```

and tipically are fixed in settings/dev.py like
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
