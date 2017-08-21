#!/bin/bash


# DEFAULT SETTINGS
PORT=8084
PROCESSES=1
THREADS=4
ENVIRONMENT="DJANGO_SETTINGS_MODULE=settings.dev"

# LOAD CUSTOMIZED SETTINGS
[ -f /etc/default/orchestrator-daemon ] && . /etc/default/orchestrator-daemon


# Default values
KEYSTONE_HOST=localhost
KEYSTONE_PORT=5001
KEYSTONE_PROTOCOL=http

KEYPASS_HOST=localhost
KEYPASS_PORT=7070 # Pep and default internal container port
KEYPASS_PROTOCOL=http

ORION_HOST=localhost
ORION_PORT=1026  # Pep and default internal container port
ORION_PROTOCOL=http

IOTA_HOST=localhost
IOTA_PORT=4052
IOTA_PROTOCOL=http

PEP_PERSEO_HOST=localhost
PEP_PERSEO_PORT=1026  # Pep Perseo
PEP_PERSEO_PROTOCOL=http

STH_HOST=localhost
STH_PORT=8666  # Pep and default internal container port
STH_PROTOCOL=http
STH_NOTIFYPATH=notify

PERSEO_HOST=localhost
PERSEO_PORT=9090  # Pep and default internal container port
PERSEO_PROTOCOL=http
PERSEO_NOTIFYPATH=notices

CYGNUS_HOST=localhost
CYGNUS_PORT=5050  # Pep and default internal container port
CYGNUS_PROTOCOL=http
CYGNUS_NOTIFYPATH=notify

while [[ $# -gt 0 ]]; do
    PARAM=`echo $1`
    VALUE=`echo $2`
    case "$PARAM" in
        -keystonehost)
            KEYSTONE_HOST=$VALUE
            ;;
        -keypasshost)
            KEYPASS_HOST=$VALUE
            ;;
        -orionhost)
            ORION_HOST=$VALUE
            ;;
        -iotahost)
            IOTA_HOST=$VALUE
            ;;
        -pepperseohost)
            PEP_PERSEO_HOST=$VALUE
            ;;
        -sthhost)
            STH_HOST=$VALUE
            ;;
        -perseohost)
            PERSEO_HOST=$VALUE
            ;;
        -cygnushost)
            CYGNUS_HOST=$VALUE
            ;;
        -keystoneport)
            KEYSTONE_PORT=$VALUE
            ;;
        -keypassport)
            KEYPASS_PORT=$VALUE
            ;;
        -orionport)
            ORION_PORT=$VALUE
            ;;
        -iotaport)
            IOTA_PORT=$VALUE
            ;;
        -pepperseoport)
            PEP_PERSEO_PORT=$VALUE
            ;;
        -sthport)
            STH_PORT=$VALUE
            ;;
        -perseoport)
            PERSEO_PORT=$VALUE
            ;;
        -cygnusport)
            CYGNUS_PORT=$VALUE
            ;;
        *)
            echo "not found"
            # Do nothing
            ;;
    esac
    shift
    shift
done


sed -i ':a;N;$!ba;s/KEYSTONE = {[A-Za-z0-9,\"\n: ]*}/KEYSTONE = { \
             \"host\": \"'$KEYSTONE_HOST'\", \
             \"port\": \"'$KEYSTONE_PORT'\", \
             \"protocol\": \"'$KEYSTONE_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/KEYPASS = {[A-Za-z0-9,\"\n: ]*}/KEYPASS = { \
             \"host\": \"'$KEYPASS_HOST'\", \
             \"port\": \"'$KEYPASS_PORT'\", \
             \"protocol\": \"'$KEYPASS_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/ORION = {[A-Za-z0-9,\"\n: ]*}/ORION = { \
             \"host\": \"'$ORION_HOST'\", \
             \"port\": \"'$ORION_PORT'\", \
             \"protocol\": \"'$ORION_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/IOTA = {[A-Za-z0-9,\"\n: ]*}/IOTA = { \
             \"host\": \"'$IOTA_HOST'\", \
             \"port\": \"'$IOTA_PORT'\", \
             \"protocol\": \"'$IOTA_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/PERSEO = {[A-Za-z0-9,\/\"\n: ]*}/PERSEO = { \
             \"host\": \"'$PERSEO_HOST'\", \
             \"port\": \"'$PERSEO_PORT'\", \
             \"protocol\": \"'$PERSEO_PROTOCOL'\", \
             \"notifypath\": \"\/'$PERSEO_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/PEP_PERSEO = {[A-Za-z0-9,\"\n: ]*}/PEP_PERSEO = { \
             \"host\": \"'$PEP_PERSEO_HOST'\", \
             \"port\": \"'$PEP_PERSEO_PORT'\", \
             \"protocol\": \"'$PEP_PERSEO_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/STH = {[A-Za-z0-9,\/\"\n: ]*}/STH = { \
             \"host\": \"'$STH_HOST'\", \
             \"port\": \"'$STH_PORT'\", \
             \"protocol\": \"'$STH_PROTOCOL'\", \
             \"notifypath\": \"\/'$STH_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/CYGNUS = {[A-Za-z0-9,\/\"\n: ]*}/CYGNUS = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$CYGNUS_PORT'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py


# Wait until Keystone is up
while ! nc -z $KEYSTONE_HOST $KEYSTONE_PORT ; do sleep 10; done

uwsgi --http :$PORT \
      --chdir /opt/orchestrator \
      --wsgi-file wsgi.py \
      --env $ENVIRONMENT \
      --master --processes $PROCESSES \
      --threads $THREADS
