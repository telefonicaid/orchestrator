# Troubleshooting: logs and alarms

## Log location

Depending on how the application was launched the logs location may vary.

If you are using the `rpm` distribution the logs are located in `/var/log/orchestrator`.

## Log rotation

Logs are configured by default to rotate every 25Mb and keep 2 older copies. For further information seee LOGGIN section of settings

## Log Level

The following levels are allowed to use to print logs:

 CRITICAL: only CRITICAL messages are logged
 ERROR: only ERROR messages are logged
 WARN (default): WARN and ERROR messages are logged
 INFO: INFO, WARN and ERROR messages are logged
 DEBUG: DEBUG, INFO, WARN and ERROR messages are logged



There are some API operations to allow get and change log level.

To get current log level:
```
curl -i -X GET 'http://localhost:8084/v1.0/admin/log' -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{ "SERVICE_ADMIN_USER": "cloud_admin", "SERVICE_ADMIN_PASSWORD":"password"}'
```

To change log level to DEBUG level:
```
curl -i -X PUT 'http://localhost:8084/v1.0/admin/log?level=DEBUG' -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{ "SERVICE_ADMIN_USER": "cloud_admin", "SERVICE_ADMIN_PASSWORD":"password"}'
```


## Version, launch date and listen ports

You can easily discover what version was launched, at what date it was launched,
and on what ports are listening. Just search for the keyword `Starting Service` on logs
files and you will see that information:

```
time=15:12:54.743 | lvl=INFO | component=Orchestrator | msg=Starting Service
   ____           _               _             _
  / __ \         | |             | |           | |
 | |  | |_ __ ___| |__   ___  ___| |_ _ __ __ _| |_ ___  _ __
 | |  | | '__/ __| '_ \ / _ \/ __| __| '__/ _` | __/ _ \| '__|
 | |__| | | | (__| | | |  __/\__ \ |_| | | (_| | || (_) | |
  \____/|_|  \___|_| |_|\___||___/\__|_|  \__,_|\__\___/|_|

 v1.2.0

```



## Alarms

Alarm conditions:


| Alarm ID   | Severity   |   Detection strategy                                                                                              | Stop condition                                                                                                                                                                                                                            | Description                                                                                                   | Action
|:---------- |:----------:|:----------------------------------------------------------------------------------------------------------------- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 1          | CRITICAL   | A CRITICAL trace is found                                                                                            | N/A                                                                                                                                                                                                                                       | A problem has occurred at orchestrator startup. The CRITICAL 'msg' field details the particular problem. | Solving the issue that is precluding Orchestrator startup, e.g. if the problem was due to the listening port is being used, the solution would be either changing Orchestrator listening port or ending the process that is already using the port.
| 2          | CRITICAL   | The following ERROR text appears in the 'msg' field: "Runtime Error (`<detail>`)"                                 | N/A                                                                                                                                                                                                                                       | Runtime Error. The `<detail>` text containts the detailed information.                                        | Restart Orchestrator. If it persists (e.g. new Runtime Errors appear within the next hour), scale up the problem to development team.


## Endpoint connection errors

At start time Orchestrator tries to connect to Auth (Keystone) and Access Control (Keypass) Endpoints.

If all of these endpoints are available the following info entry will appear in the logs.

```
time=24/Feb/2015 10:47:49 | lvl=INFO | component=Orchestrator | msg=Checking endpoints OK
```

If Keystone connection is not available the following error entry will appear in the logs.
```
time=24/Feb/2015 10:50:04 | lvl=ERROR | component=Orchestrator | msg=keystone endpoint not found
time=24/Feb/2015 10:50:04 | lvl=INFO | component=Orchestrator | msg=Checking endpoints ERROR keystone endpoint not found
```

If Keypass connection is not available the following error entry will appear in the logs.
```
time=24/Feb/2015 10:49:27 | lvl=ERROR | component=Orchestrator | msg=keypass endpoint not found
time=24/Feb/2015 10:49:27 | lvl=INFO | component=Orchestrator | msg=Checking endpoints ERROR keypass endpoint not found
```


## Endpoint configuration errors

At start time Orchestrator tries to connect to Auth (Keystone),  Access Control (Keypass) Endpoints
other endpoints (as orion, perseo or iotagent)

if Any of the above endpoints are not available the following error entry will appear in the log.
```
time=24/Feb/2015 10:49:27 | lvl=ERROR | component=Orchestrator | msg="KEYSTONE endpoint configuration error. Forcing to use default conf values (localhost)"
```


## API Errors
