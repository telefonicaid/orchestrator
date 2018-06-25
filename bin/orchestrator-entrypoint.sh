#!/bin/bash


# DEFAULT SETTINGS
PORT=8084
PROCESSES=6
THREADS=8
HARAKIRI=40
MAX_REQUESTS=1000
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

LDAP_HOST=localhost
LDAP_PORT=389
LDAP_BASEDN='dc=openstack,dc=org'

MAILER_HOST=localhost
MAILER_PORT=587
MAILER_USER=smtpuser@yourdomain.com
MAILER_PASSWORD=yourpassword
MAILER_FROM=smtpuser
MAILER_TO=smtpuser

MONGODB_URI='localhost:27017'

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
        -ldaphost)
            LDAP_HOST=$VALUE
            ;;
        -mailerhost)
            MAILER_HOST=$VALUE
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
        -ldapport)
            LDAP_PORT=$VALUE
            ;;
        -mailerport)
            MAILER_PORT=$VALUE
            ;;
        -ldapbasedn)
            LDAP_BASEDN=$VALUE
            ;;
        -maileruser)
            MAILER_USER=$VALUE
            ;;
        -mailerpasswd)
            MAILER_PASSWORD=$VALUE
            ;;
        -mailerfrom)
            MAILER_FROM=$VALUE
            ;;
        -mailerto)
            MAILER_TO=$VALUE
            ;;
        -mongodburi)
            MONGODB_URI=$VALUE
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

sed -i ':a;N;$!ba;s/LDAP = {[A-Za-z0-9,=@.\-\/\"\n: ]*}/LDAP = { \
             \"host\": \"'$LDAP_HOST'\", \
             \"port\": \"'$LDAP_PORT'\", \
             \"basedn\": \"'$LDAP_BASEDN'\", \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/MAILER = {[A-Za-z0-9,=@.\-\/\"\n: ]*}/MAILER = { \
             \"host\": \"'$MAILER_HOST'\", \
             \"port\": \"'$MAILER_PORT'\", \
             \"user\": \"'$MAILER_USER'\", \
             \"password\": \"'$MAILER_PASSWORD'\", \
             \"from\": \"'$MAILER_FROM'\", \
             \"to\": \"'$MAILER_TO'\", \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/MONGODB = {[A-Za-z0-9,\/\"\n: ]*}/MONGODB = { \
             \"URI\": \"mongodb:\/\/'$MONGODB_URI'\" \
}/g' /opt/orchestrator/settings/dev.py


# Wait until Keystone is up
while ! tcping -t 1 $KEYSTONE_HOST $KEYSTONE_PORT ; do sleep 10; done

uwsgi --http :$PORT \
      --chdir /opt/orchestrator \
      --wsgi-file wsgi.py \
      --env $ENVIRONMENT \
      --master \
      --processes $PROCESSES \
      --threads $THREADS \
      --harakiri $HARAKIRI \
      --max-requests $MAX_REQUESTS \
      --vacuum \
      --enable-threads \
      --disable-logging
