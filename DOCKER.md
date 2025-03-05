
# How to use this Dockerfile

You can build a docker image based on this Dockerfile. This image will contain only an Orchestrator instance, exposing port `8084`. This requires that you have [docker](https://docs.docker.com/installation/) installed on your machine.

If you just want to have an Orchestrator running as fast as possible jump to section [The Fastest Way](#the_fastest_way).

If you want to know what and how we are doing things with the container step by step you can go ahead and read the [Build](#build_the_image) and [Run](#run_the_container) sections.

## The Fastest Way

A Docker Compose file is provided for convenience. You must install [Docker Compose](https://docs.docker.com/compose/install/) for this method to work.

Simply navigate to the docker directory of the orchestrator code (if you have downloaded it) and run

        docker-compose up

If you haven't or you don't want to download the whole thing, you can download the file called `docker-compose.yaml` in a directory of your choice and run the aforementioned command. It will work just the same.

You can use [this](https://github.com/telefonicaid/orchestrator/blob/master/docker-compose.yaml) or also you can create a docker-compose.yaml file, were you should include an orchestrator section like this:

```
orchestrator:
  image: telefonicaiot/orchestrator:latest
  expose:
    - "8084"
  links:
    - keystone
    - keypass
    - pep-orion
    - pep-perseo-fe
    - mongo
  ports:
    - "8084:8084"
  command: -keystonehost keystone -keypasshost keypass -orionhost pep-orion -pepperseohost pep-perseo-fe -sthhost sth -perseohost perseo-fe -cygnushost cygnus -mongodburi mongo:27017
```

As you can see there are several arguments to pass to orchestrator entry point in order to configure some relevant endpoints for orchestrator as keystone, keypass, orion, iota and so on. Make sure all of them are present:
```
   -keystonehost <value>
   -keypasshost <value>
   -orionhost <value>
   -pepperseohost <value>
   -sthhost <value>
   -perseohost <value>
   -cygnushost <value>
   -mailerhost <value>
   -ldaphost <value>
   -keystoneport <value>
   -keypassport <value>
   -orionport <value>
   -pepperseoport <value>
   -sthport <value>
   -perseoport <value>
   -cygnusport <value>
   -ldapport <value>
   -mailerport <value>
   -ldapbasedn <value>
   -maileruser <value>
   -mailerpasswd <value>
   -mailerfrom <value>
   -mailerto <value>
   -mongodburi <value>
```



| command option | settings configuration | default value             |
|:---------------|:-----------------------|---------------------------|
| -keystonehost  | KEYSTONE.host          | localhost                 |
| -keypasshost   | KEYPASS.host           | localhost                 |
| -orionhost     | ORION.host             | localhost                 |
| -pepperseohost | PEP_ORION.host         | localhost                 |
| -sthhost       | STH.host               | localhost                 |
| -perseohost    | PERSEO.host            | localhost                 |
| -cygnushost    | CYGNUS.host            | localhost                 |
| -mailerhost    | MAILER.host            | localhost                 |
| -ldaphost      | LDAP.host              | localhost                 |
| -keystoneport  | KEYSTONE.port          | 5001                      |
| -keypassport   | KEYPASS.port           | 7070                      |
| -orionport     | ORION.port             | 1026                      |
| -pepperseoport | PEP_PERSEO.port        | 9090                      |
| -sthport       | STH.port               | 8666                      |
| -perseoport    | PERSEO.port            | 9090                      |
| -cygnusport    | CYGNUS.port            | 5050                      |
| -ldapport      | LDAP.port              | 389                       |
| -mailerport    | MAILER.port            | 587                       |
| -ldapbasedn    | LDAP.basedn            | dc=openstack,dc=org       |
| -maileruser    | MAILER.user            | smtpuser@yourdomain.com   |
| -mailerpasswd  | MAILER.password        | yourpassword              |
| -mailerfrom    | MAILER.from            | smtpuser                  |
| -mailerto      | MAILER.to              | smtpuser                  |
| -mongodburi    | MONGODB.URI            | mongodb://localhost:27017 |
|                |                        |                           |




Additionally, the following environment variables are available for orchestrator docker

| Environment variable        | Configuration attribute   | Default value             |
|:----------------------------|:--------------------------|:--------------------------|
| PORT                        |                           | 8084                      |
| STATS_PORT                  |                           | 8184                      |
| PROCESSES                   |                           | 6                         |
| THREADS                     |                           | 8                         |
| HARAKIRI                    |                           | 80                        |
| HTTP_TIMEOUT                |                           | 200                       |
| MAX_REQUESTS                |                           | 250                       |
| QUEUE_SIZE                  |                           | 256                       |
| UWSGI_BUFFER_SIZE           |                           | 4096                      |
| KEYSTONE_HOST               | KEYSTONE.host             | localhost                 |
| KEYSTONE_PORT               | KEYSTONE.port             | 5001                      |
| KEYSTONE_PROTOCOL           | KEYSTONE.protocol         | http                      |
| KEYPASS_HOST                | KEYPASS.host              | localhost                 |
| KEYPASS_PORT                | KEYPASS.port              | 17070                     |
| KEYPASS_PROTOCOL            | KEYPASS.protocol          | http                      |
| ORION_HOST                  | ORION.host                | localhost                 |
| ORION_PORT                  | ORION.port                | 1026                      |
| ORION_PROTOCOL              | ORION.protocol            | http                      |
| PEP_PERSEO_HOST             | PEP_ORION.host            | localhost                 |
| PEP_PERSEO_PORT             | PEP_PERSEO.port           | 9090                      |
| PEP_PERSEO_PROTOCOL         | PEP_PERSEO.protocol       | http                      |
| STH_HOST                    | STH.host                  | localhost                 |
| STH_PORT                    | STH.port                  | 18666                     |
| STH_NOTIFYPATH              | STH.notifypath            | notify                    |
| STH_PROTOCOL                | STH.protocol              | http                      |
| PERSEO_HOST                 | PERSEO.host               | localhost                 |
| PERSEO_PORT                 | PERSEO.port               | 19090                     |
| PERSEO_PROTOCOL             | PERSEO.protocol           | http                      |
| PERSEO_NOTIFYPATH           | PERSEO.notifypath         | notices                   |
| CYGNUS_HOST                 | CYGNUS.host               | localhost                 |
| CYGNUS_PORT                 | CYGNUS.port               | 5050                      |
| CYGNUS_PROTOCOL             | CYGNUS.protocol           | http                      |
| CYGNUS_NOTIFYPATH           | CYGNUS.notifypath         | notify                    |
| CYGNUS_MULTISING            | CYGNUS.multisink          | false                     |
| MAILER_HOST                 | MAILER.host               | localhost                 |
| MAILER_PORT                 | MAILER.port               | 587                       |
| MAILER_TLS                  | MAILER.tls                | true                      |
| MAILER_USER                 | MAILER.user               | smtpuser@yourdomain.com   |
| MAILER_PASSWORD             | MAILER.password           | yourpassword              |
| MAILER_FROM                 | MAILER.from               | smtpuser                  |
| MAILER_TO                   | MAILER.to                 | smtpuser                  |
| LDAP_HOST                   | LDAP.host                 | localhost                 |
| LDAP_PORT                   | LDAP.port                 | 389                       |
| LDAP_BASEDN                 | LDAP.basedn               | dc=openstack,dc=org       |
| MONGODB_URI                 | MONGODB.URI               | localhost:27017           |
| PEP_USER                    | PEP.user                  | pep                       |
| PEP_PASSWORD                | PEP.password              | pep                       |
| IOTAGENT_USER               | IOTAGENT.user             | iotagent                  |
| IOTAGENT_PASSWORD           | IOTAGENT.password         | iotagent                  |
| ORC_EXTENDED_METRICS        | ORC_EXTENDED_METRICS      | false                     |


## Build the image

This is an alternative approach than the one presented in section [The Fastest Way](#the_fastest_way). You do not need to go through these steps if you have used docker-compose.

You only need to do this once in your system:

        docker build -t orchestrator .

The parameter `-t orchestrator` gives the image a name. This name could be anything, or even include an organization like `-t org/orchestrator`. This name is later used to run the container based on the image.

If you want to know more about images and the building process you can find it in [Docker's documentation](https://docs.docker.com/userguide/dockerimages/).
    
## Run the container

The following line will run the container exposing port `8084`, give it a name -in this case `orchestrator1` and present a bash prompt.

          docker run -d --name orchestrator1 -p 8084:8084 orchestrator

As a result of this command, there is a orchestrator listening on port 8084 on localhost. Try to see if it works now with

          curl localhost:8084/v1.0/version

A few points to consider:

* The name `orchestrator1` can be anything and doesn't have to be related to the name given to the docker image in the previous section.
* In `-p 8084:8084` the first value represents the port to listen in on localhost. If you wanted to run a second orchestrator on your machine you should change this value to something else, for example `-p 8184:8084`.
* Anything after the name of the container image (in this case `orchestrator`) is interpreted as a parameter for the Orchestrator.

In order to obtain stats about uwsgi orchestrator could be started using:

          docker run -d --name orchestrator1 -p 8084:8084 -p 8184:8184 orchestrator

To obtain a json about uwsgi stats:

          curl -X GET localhost:8184

An example of json stats:
```
{
    "version":"2.0.28",
    "listen_queue":0,
    "listen_queue_errors":0,
    "signal_queue":0,
    "load":0,
    "pid":31,
    "uid":0,
    "gid":0,
    "cwd":"/var/env-orchestrator/lib/python3.11/site-packages/iotp-orchestrator",
    "locks":[
        {
            "user 0":0
        },
        {
            "signal":0
        },
        {
            "filemon":0
        },
        {
            "timer":0
        },
        {
            "rbtimer":0
        },
        {
            "cron":0
        },
        {
            "rpc":0
        },
        {
            "snmp":0
        }
    ],
    "sockets":[
        {
            "name":"127.0.0.1:40885",
            "proto":"uwsgi",
            "queue":0,
            "max_queue":256,
            "shared":0,
            "can_offload":0
        }
    ],
    "workers":[
        {
            "id":1,
            "pid":42,
            "accepting":1,
            "requests":1,
            "delta_requests":1,
            "exceptions":0,
            "harakiri_count":0,
            "signals":0,
            "signal_queue":0,
            "status":"idle",
            "rss":0,
            "vsz":0,
            "running_time":53062,
            "last_spawn":1740581846,
            "respawn_count":1,
            "tx":1102,
            "avg_rt":26531,
            "apps":[
                {
                    "id":0,
                    "modifier1":0,
                    "mountpoint":"",
                    "startup_time":0,
                    "requests":1,
                    "exceptions":0,
                    "chdir":""
                }
            ],
            "cores":[
                {
                    "id":0,
                    "requests":0,
                    "static_requests":0,
                    "routed_requests":0,
                    "offloaded_requests":0,
                    "write_errors":0,
                    "read_errors":0,
                    "in_request":0,
                    "vars":[

                    ],
                    "req_info":             {

                    }
                },
                {
                    "id":1,
                    "requests":1,
                    "static_requests":0,
                    "routed_requests":0,
                    "offloaded_requests":0,
                    "write_errors":0,
                    "read_errors":0,
                    "in_request":0,
                    "vars":[

                    ],
                    "req_info":             {

                    }
                },

```
