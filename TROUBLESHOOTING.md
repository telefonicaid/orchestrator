# Troubleshooting

## Log location

Depending on how the application was launched the logs location may vary.

If you are using the `rpm` distribution the logs are located in `/var/log/orchestrator`.

## Log rotation

Logs are configured by default to rotate every 500Mb and keep 2 older copies. For further information seee LOGGIN section of settings

## Version, launch date and listen ports

You can easily discover what version was launched, at what date it was launched,
and on what ports are listening. Just search for the keyword `Starting Service` on logs
files and you will see that information:

```
time=15:12:54.743 | lvl=INFO | op= | msg=Starting Service
   ____           _               _             _
  / __ \         | |             | |           | |
 | |  | |_ __ ___| |__   ___  ___| |_ _ __ __ _| |_ ___  _ __
 | |  | | '__/ __| '_ \ / _ \/ __| __| '__/ _` | __/ _ \| '__|
 | |__| | | | (__| | | |  __/\__ \ |_| | | (_| | || (_) | |
  \____/|_|  \___|_| |_|\___||___/\__|_|  \__,_|\__\___/|_|

 v0.1.0


## Endpoint connection errors

At start time Orchestrator tries to connect to Auth (Keystone) and Access Control (Keypass) Endpoints

If all endpoints are available the following info entry will appear in the logs.

```
time=24/Feb/2015 10:47:49 | lvl=INFO | op=orchestrator_api:48 | msg=Checking endpoints OK
```

If Keystone connection is not available the following error entry will appear in the logs.
```
time=24/Feb/2015 10:50:04 | lvl=ERROR | op=orchestrator_api:34 | msg=keystone endpoint not found
time=24/Feb/2015 10:50:04 | lvl=INFO | op=orchestrator_api:48 | msg=Checking endpoints ERROR keystone endpoint not found 
```

If Keypass connection is not available the following error entry will appear in the logs.
```
time=24/Feb/2015 10:49:27 | lvl=ERROR | op=orchestrator_api:40 | msg=keyspass endpoint not found
time=24/Feb/2015 10:49:27 | lvl=INFO | op=orchestrator_api:48 | msg=Checking endpoints ERROR keypass endpoint not found
```

## API Errors
