#!/bin/bash

# Default values
KEYSTONE_PORT=5001
KEYSTONE_PROTOCOL=http

KEYPASS_PORT=17070
KEYPASS_PROTOCOL=http

ORION_PORT=1026
ORION_PROTOCOL=http

IOTA_PORT=4052
IOTA_PROTOCOL=http

STH_PORT=18666
STH_PROTOCOL=http

PERSEO_PORT=19090
PERSEO_PROTOCOL=http


# Check arguments
KEYSTONE_HOST_ARG=${1}
KEYSTONE_HOST_VALUE=${2}
KEYPASS_HOST_ARG=${3}
KEYPASS_HOST_VALUE=${4}

ORION_HOST_ARG=${5}
ORION_HOST_VALUE=${6}

IOTA_HOST_ARG=${7}
IOTA_HOST_VALUE=${8}

STH_HOST_ARG=${9}
STH_HOST_VALUE=${10}

PERSEO_HOST_ARG=${11}
PERSEO_HOST_VALUE=${12}


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

if [ "$PERSEO_HOST_ARG" == "-perseohost" ]; then
    sed -i ':a;N;$!ba;s/PERSEO = {[A-Za-z0-9,\"\n: ]*}/PERSEO = { \
             \"host\": \"'$PERSEO_HOST_VALUE'\", \
             \"port\": \"'$PERSEO_PORT'\", \
             \"protocol\": \"'$PERSEO_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

if [ "$STH_HOST_ARG" == "-sthhost" ]; then
    sed -i ':a;N;$!ba;s/STH = {[A-Za-z0-9,\"\n: ]*}/STH = { \
             \"host\": \"'$STH_HOST_VALUE'\", \
             \"port\": \"'$STH_PORT'\", \
             \"protocol\": \"'$STH_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

sleep 60
#/opt/orchestrator/bin/orchestrator-daemon.sh restart
python manage.py runserver 0.0.0.0:8084 --settings=settings.dev
