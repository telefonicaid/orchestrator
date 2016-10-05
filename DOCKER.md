
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
  image: telefonicaiot/orchestrator:develop
  expose:
    - "8084"
  links:
    - keystone
    - keypass
    - pep-orion
    - pep-perseo-fe
    - iota
  ports:
    - "8084:8084"
  command: -keystonehost keystone -keypasshost keypass -orionhost pep-orion -iotahost iota -pepperseohost pep-perseo-fe -sthhost sth -perseohost perseo-fe -cygnushost cygnus
```

As you can see there are several arguments to pass to orchestrator entry point in order to configure some relevant endpoints for orchestrator as keystone, keypass, orion, iota and so on. Make sure all of them are present and in that order:
```
   -keystonehost keystone
   -keypasshost keypass
   -orionhost pep-orion
   -iotahost iota
   -pepperseohost pep-perseo-fe
   -sthhost sth
   -perseohost perseo-fe
   -cygnushost cygnus
```


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

        curl localhost:8084

A few points to consider:

* The name `orchestrator1` can be anything and doesn't have to be related to the name given to the docker image in the previous section.
* In `-p 8084:8084` the first value represents the port to listen in on localhost. If you wanted to run a second orchestrator on your machine you should change this value to something else, for example `-p 8184:8084`.
* Anything after the name of the container image (in this case `orchestrator`) is interpreted as a parameter for the Orchestrator. Take a look at the [documentation](../.../.../doc/admin/cli.md) for other command-line options.

