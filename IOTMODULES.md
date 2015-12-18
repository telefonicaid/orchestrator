IoT Platform allows to enable or disable some IoT Modules for each register Service.

IoT Modules are optional features, like persistence services or GPS location service.

Orchestrator allows enable ir disable these IoT Modules per service (aka keystone domain) or subservice (aka keystone project). There are an [API](http://docs.orchestrator2.apiary.io/#reference/orchestrator/activate-iot-module-in-a-sub-service-of-service) and a command to handle IoT Modules through Orchestrator.

Enable or disable an IoT Module implies subscribe or unsubscribe IoTModule in Orion Context Broker for all entities.

IoT Modules are defined in Orchestrator configuration files, typically a file like [that](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings/dev.py) in this sense:

There is a list of possible IoT Modules: 

```
IOTMODULES = [ "STH", "CYGNUS", "PERSEO" ]
```

For each IoT Module there is an object to define fully related endpoint. This object has IoT Module name, like aboe names:

```
STH = {
    "host": "localhost",
    "port": "8666",
    "protocol":"http"
}
```

This way to add a new IoT Module into Orchestrator you should add something like this to [conf]((https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings/dev.py) file

```
IOTMODULES = [ "STH", "CYGNUS", "PERSEO", "MYNEWMOD" ]

MYNEWMOD = {
    "host": "localhost",
    "port": "7777",
    "protocol":"http"
}
```
