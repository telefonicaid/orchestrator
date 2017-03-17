#!/bin/bash


# DEFAULT SETTINGS
PORT=8084
PROCESSES=1
THREADS=4
ENVIRONMENT="DJANGO_SETTINGS_MODULE=settings.dev"

# LOAD CUSTOMIZED SETTINGS
[ -f /etc/default/orchestrator-daemon ] && . /etc/default/orchestrator-daemon


# Default values
KEYSTONE_PORT=5001
KEYSTONE_PROTOCOL=http

KEYPASS_PORT=7070 # Pep and default internal container port
KEYPASS_PROTOCOL=http

ORION_PORT=1026  # Pep and default internal container port
ORION_PROTOCOL=http

IOTA_PORT=4052
IOTA_PROTOCOL=http

PEP_PERSEO_PORT=1026  # Pep Perseo
PEP_PERSEO_PROTOCOL=http

STH_PORT=8666  # Pep and default internal container port
STH_PROTOCOL=http
STH_NOTIFYPATH=notify

PERSEO_PORT=9090  # Pep and default internal container port
PERSEO_PROTOCOL=http
PERSEO_NOTIFYPATH=notices

CYGNUS_PORT=5050  # Pep and default internal container port
CYGNUS_PROTOCOL=http
CYGNUS_NOTIFYPATH=notify


# Check arguments
KEYSTONE_HOST_ARG=${1}
KEYSTONE_HOST_VALUE=${2}
KEYPASS_HOST_ARG=${3}
KEYPASS_HOST_VALUE=${4}

ORION_HOST_ARG=${5}
ORION_HOST_VALUE=${6}

IOTA_HOST_ARG=${7}
IOTA_HOST_VALUE=${8}

PEP_PERSEO_HOST_ARG=${9}
PEP_PERSEO_HOST_VALUE=${10}

STH_HOST_ARG=${11}
STH_HOST_VALUE=${12}

PERSEO_HOST_ARG=${13}
PERSEO_HOST_VALUE=${14}

CYGNUS_HOST_ARG=${15}
CYGNUS_HOST_VALUE=${16}


if [ "$KEYSTONE_HOST_ARG" == "-keystonehost" ]; then
    sed -i ':a;N;$!ba;s/KEYSTONE = {[A-Za-z0-9,\"\n: ]*}/KEYSTONE = { \
             \"host\": \"'$KEYSTONE_HOST_VALUE'\", \
             \"port\": \"'$KEYSTONE_PORT'\", \
             \"protocol\": \"'$KEYSTONE_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$KEYPASS_HOST_ARG" == "-keypasshost" ]; then
    sed -i ':a;N;$!ba;s/KEYPASS = {[A-Za-z0-9,\"\n: ]*}/KEYPASS = { \
             \"host\": \"'$KEYPASS_HOST_VALUE'\", \
             \"port\": \"'$KEYPASS_PORT'\", \
             \"protocol\": \"'$KEYPASS_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$ORION_HOST_ARG" == "-orionhost" ]; then
    sed -i ':a;N;$!ba;s/ORION = {[A-Za-z0-9,\"\n: ]*}/ORION = { \
             \"host\": \"'$ORION_HOST_VALUE'\", \
             \"port\": \"'$ORION_PORT'\", \
             \"protocol\": \"'$ORION_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$IOTA_HOST_ARG" == "-iotahost" ]; then
    sed -i ':a;N;$!ba;s/IOTA = {[A-Za-z0-9,\"\n: ]*}/IOTA = { \
             \"host\": \"'$IOTA_HOST_VALUE'\", \
             \"port\": \"'$IOTA_PORT'\", \
             \"protocol\": \"'$IOTA_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$PEP_PERSEO_HOST_ARG" == "-pepperseohost" ]; then
    sed -i ':a;N;$!ba;s/PEP_PERSEO = {[A-Za-z0-9,\"\n: ]*}/PEP_PERSEO = { \
             \"host\": \"'$PEP_PERSEO_HOST_VALUE'\", \
             \"port\": \"'$PEP_PERSEO_PORT'\", \
             \"protocol\": \"'$PEP_PERSEO_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$PERSEO_HOST_ARG" == "-perseohost" ]; then
    sed -i ':a;N;$!ba;s/PERSEO = {[A-Za-z0-9,\/\"\n: ]*}/PERSEO = { \
             \"host\": \"'$PERSEO_HOST_VALUE'\", \
             \"port\": \"'$PERSEO_PORT'\", \
             \"protocol\": \"'$PERSEO_PROTOCOL'\", \
             \"notifypath\": \"\/'$PERSEO_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$STH_HOST_ARG" == "-sthhost" ]; then
    sed -i ':a;N;$!ba;s/STH = {[A-Za-z0-9,\/\"\n: ]*}/STH = { \
             \"host\": \"'$STH_HOST_VALUE'\", \
             \"port\": \"'$STH_PORT'\", \
             \"protocol\": \"'$STH_PROTOCOL'\", \
             \"notifypath\": \"\/'$STH_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$CYGNUS_HOST_ARG" == "-cygnushost" ]; then
    sed -i ':a;N;$!ba;s/CYGNUS = {[A-Za-z0-9,\/\"\n: ]*}/CYGNUS = { \
             \"host\": \"'$CYGNUS_HOST_VALUE'\", \
             \"port\": \"'$CYGNUS_PORT'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

# Wait until Keystone is up
while ! nc -z $KEYSTONE_HOST_VALUE $KEYSTONE_PORT ; do sleep 10; done

uwsgi --http :$PORT \
      --chdir /opt/orchestrator \
      --wsgi-file wsgi.py \
      --env $ENVIRONMENT \
      --master --processes $PROCESSES \
      --threads $THREADS
