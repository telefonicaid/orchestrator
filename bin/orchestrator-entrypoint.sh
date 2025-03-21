#!/bin/bash

#
# DEFAULT SETTINGS
#
# UWSGI
[[ "${PORT}" == "" ]] && export PORT=8084
[[ "${STATS_PORT}" == "" ]] && export STATS_PORT=8184
[[ "${PROCESSES}" == "" ]] && export PROCESSES=6
[[ "${THREADS}" == "" ]] && export THREADS=8
[[ "${HARAKIRI}" == "" ]] && export HARAKIRI=80
[[ "${HTTP_TIMEOUT}" == "" ]] && export HTTP_TIMEOUT=200
[[ "${MAX_REQUESTS}" == "" ]] && export MAX_REQUESTS=250
[[ "${QUEUE_SIZE}" == "" ]] && export QUEUE_SIZE=256
[[ "${ENVIRONMENT}" == "" ]] && export ENVIRONMENT="DJANGO_SETTINGS_MODULE=settings.dev"
[[ "${UWSGI_BUFFER_SIZE}" == "" ]] && export UWSGI_BUFFER_SIZE=4096

# Default values
[[ "${KEYSTONE_HOST}" == "" ]] && export KEYSTONE_HOST=localhost
[[ "${KEYSTONE_PORT}" == "" ]] && export KEYSTONE_PORT=5001
[[ "${KEYSTONE_PROTOCOL}" == "" ]] && export KEYSTONE_PROTOCOL=http

[[ "${KEYPASS_HOST}" == "" ]] && export KEYPASS_HOST=localhost
[[ "${KEYPASS_PORT}" == "" ]] && export KEYPASS_PORT=7070 # Pep and default internal container port
[[ "${KEYPASS_PROTOCOL}" == "" ]] && export KEYPASS_PROTOCOL=http

[[ "${ORION_HOST}" == "" ]] && export ORION_HOST=localhost
[[ "${ORION_PORT}" == "" ]] && export ORION_PORT=1026  # Pep and default internal container port
[[ "${ORION_PROTOCOL}" == "" ]] && export ORION_PROTOCOL=http

[[ "${PEP_PERSEO_HOST}" == "" ]] && export PEP_PERSEO_HOST=localhost
[[ "${PEP_PERSEO_PORT}" == "" ]] && export PEP_PERSEO_PORT=1026  # Pep Perseo
[[ "${PEP_PERSEO_PROTOCOL}" == "" ]] && export PEP_PERSEO_PROTOCOL=http

[[ "${STH_HOST}" == "" ]] && export STH_HOST=localhost
[[ "${STH_PORT}" == "" ]] && export STH_PORT=8666  # Pep and default internal container port
[[ "${STH_PROTOCOL}" == "" ]] && export STH_PROTOCOL=http
[[ "${STH_NOTIFYPATH}" == "" ]] && export STH_NOTIFYPATH=notify

[[ "${PERSEO_HOST}" == "" ]] && export PERSEO_HOST=localhost
[[ "${PERSEO_PORT}" == "" ]] && export PERSEO_PORT=9090  # Pep and default internal container port
[[ "${PERSEO_PROTOCOL}" == "" ]] && export PERSEO_PROTOCOL=http
[[ "${PERSEO_NOTIFYPATH}" == "" ]] && export PERSEO_NOTIFYPATH=notices

[[ "${CYGNUS_HOST}" == "" ]] && export CYGNUS_HOST=localhost
[[ "${CYGNUS_PORT}" == "" ]] && export CYGNUS_PORT=5050  # Pep and default internal container port
[[ "${CYGNUS_PROTOCOL}" == "" ]] && export CYGNUS_PROTOCOL=http
[[ "${CYGNUS_NOTIFYPATH}" == "" ]] && export CYGNUS_NOTIFYPATH=notify

[[ "${LDAP_HOST}" == "" ]] && export LDAP_HOST=localhost
[[ "${LDAP_PORT}" == "" ]] && export LDAP_PORT=389
[[ "${LDAP_BASEDN}" == "" ]] && export LDAP_BASEDN='dc=openstack,dc=org'

[[ "${MAILER_HOST}" == "" ]] && export MAILER_HOST=localhost
[[ "${MAILER_PORT}" == "" ]] && export MAILER_PORT=587
[[ "${MAILER_TLS}" == "" ]] && export MAILER_TLS=true
[[ "${MAILER_USER}" == "" ]] && export MAILER_USER=smtpuser@yourdomain.com
[[ "${MAILER_PASSWORD}" == "" ]] && export MAILER_PASSWORD=yourpassword
[[ "${MAILER_FROM}" == "" ]] && export MAILER_FROM=smtpuser
[[ "${MAILER_TO}" == "" ]] && export MAILER_TO=smtpuser

[[ "${MONGODB_URI}" == "" ]] && export MONGODB_URI='localhost:27017'


[[ "${PEP_USER}" == "" ]] && export PEP_USER=pep
[[ "${PEP_PASSWORD}" == "" ]] && export PEP_PASSWORD=pep
[[ "${IOTAGENT_USER}" == "" ]] && export IOTAGENT_USER=iotagent
[[ "${IOTAGENT_PASSWORD}" == "" ]] && export IOTAGENT_PASSWORD=iotagent

[[ "${ORC_EXTENDED_METRICS}" == "" ]] && export ORC_EXTENDED_METRICS=false

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
        -mailertls)
            MAILER_TLS=$VALUE
            ;;
        -mongodburi)
            MONGODB_URI=$VALUE
            ;;
        -pepuser)
            PEP_USER=$VALUE
            ;;
        -peppwd)
            PEP_PASSWORD=$VALUE
            ;;
        -iotagentuser)
            IOTAGENT_USER=$VALUE
            ;;
        -iotagentpwd)
            IOTAGENT_PASSWORD=$VALUE
            ;;
        -cygnusmultisink|-cygnusmultiagent)
            CYGNUS_MULTISINK=$VALUE
            ;;
        -debuglevel)
            DEBUG_LEVEL=$VALUE
            ;;
        -uwsgibuffersize)
            UWSGI_BUFFER_SIZE=$VALUE
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


# Check if CYGNUS multisink
if [ "$CYGNUS_MULTISINK" == "true" ]; then
    sed -i ':a;N;$!ba;s/CYGNUS = {[A-Za-z0-9,\/\"\n: ]*}/CYGNUS_MYSQL = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$CYGNUS_PORT'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
} \
CYGNUS_MONGO = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$((CYGNUS_PORT + 1))'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
} \
CYGNUS_CKAN = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$((CYGNUS_PORT + 2))'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
} \
CYGNUS_HADOOP = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$((CYGNUS_PORT + 3))'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
} \
CYGNUS_POSTGRESQL = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$((CYGNUS_PORT + 4))'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
} \
CYGNUS_ORION = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$((CYGNUS_PORT + 6))'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
} \
CYGNUS_POSTGIS = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$((CYGNUS_PORT + 7))'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py

    sed -i ':a;N;$!ba;s/"CYGNUS"/"CYGNUS_MYSQL", "CYGNUS_MONGO", "CYGNUS_CKAN", "CYGNUS_HADOOP", "CYGNUS_POSTGRESQL", "CYGNUS_ORION", "CYGNUS_POSTGIS"/g' /opt/orchestrator/settings/dev.py
else
    sed -i ':a;N;$!ba;s/CYGNUS = {[A-Za-z0-9,\/\"\n: ]*}/CYGNUS = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$CYGNUS_PORT'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\", \
             \"notifypath\": \"\/'$CYGNUS_NOTIFYPATH'\" \
}/g' /opt/orchestrator/settings/dev.py
fi

sed -i ':a;N;$!ba;s/LDAP = {[A-Za-z0-9,=@.\-\/\"\n: ]*}/LDAP = { \
             \"host\": \"'$LDAP_HOST'\", \
             \"port\": \"'$LDAP_PORT'\", \
             \"basedn\": \"'$LDAP_BASEDN'\", \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/MAILER = {[A-Za-z0-9,=@.\-\/\"\n: ]*}/MAILER = { \
             \"host\": \"'$MAILER_HOST'\", \
             \"port\": \"'$MAILER_PORT'\", \
             \"tls\": \"'$MAILER_TLS'\", \
             \"user\": \"'$MAILER_USER'\", \
             \"password\": \"'$MAILER_PASSWORD'\", \
             \"from\": \"'$MAILER_FROM'\", \
             \"to\": \"'$MAILER_TO'\", \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/MONGODB = {[A-Za-z0-9,\/\"\n: ]*}/MONGODB = { \
             \"URI\": \"mongodb:\/\/'$MONGODB_URI'\" \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/PEP = {[A-Za-z0-9,=@.\-\/\"\n: ]*}/PEP = { \
             \"user\": \"'$PEP_PASSWORD'\", \
             \"password\": \"'$PEP_PASSWORD'\", \
}/g' /opt/orchestrator/settings/dev.py

sed -i ':a;N;$!ba;s/IOTAGENT = {[A-Za-z0-9,=@.\-\/\"\n: ]*}/IOTAGENT = { \
             \"user\": \"'$IOTAGENT_USER'\", \
             \"password\": \"'$IOTAGENT_PASSWORD'\", \
}/g' /opt/orchestrator/settings/dev.py


if [ "$DEBUG_LEVEL" ]; then
echo "
LOGGING['handlers']['console']['level'] = '$DEBUG_LEVEL'
LOGGING['handlers']['logfile']['level'] = 'CRITICAL'
LOGGING['loggers']['orchestrator_api']['level'] = '$DEBUG_LEVEL'
LOGGING['loggers']['orchestrator_core']['level'] = '$DEBUG_LEVEL'
" >> /opt/orchestrator/settings/dev.py
fi


if [ "$ORC_EXTENDED_METRICS" == "true" ]; then
echo "
ORC_EXTENDED_METRICS = True
" >> /opt/orchestrator/settings/dev.py
fi

# Wait until Keystone and Keypass are up
while ! nc -zvw10 $KEYSTONE_HOST $KEYSTONE_PORT ; do sleep 10; done
while ! nc -zvw10 $KEYPASS_HOST $KEYPASS_PORT ; do sleep 10; done

echo "Using UWSGI configuration options: "
echo "  PORT=${PORT}"
echo "  STATS_PORT=${STATS_PORT}"
echo "  PROCESSES=${PROCESSES}"
echo "  THREADS=${THREADS}"
echo "  HARAKIRI=${HARAKIRI}"
echo "  HTTP_TIMEOUT=${HTTP_TIMEOUT}"
echo "  MAX_REQUESTS=${MAX_REQUESTS}"
echo "  QUEUE_SIZE=${QUEUE_SIZE}"
echo "  UWSGI_BUFFER_SIZE=${UWSGI_BUFFER_SIZE}"

uwsgi --http :$PORT \
      --stats :$STATS_PORT \
      --stats-http \
      --chdir /opt/orchestrator \
      --wsgi-file wsgi.py \
      --env $ENVIRONMENT \
      --master \
      --processes $PROCESSES \
      --threads $THREADS \
      --harakiri $HARAKIRI \
      --http-timeout $HTTP_TIMEOUT \
      --max-requests $MAX_REQUESTS \
      --listen $QUEUE_SIZE \
      --vacuum \
      --enable-threads \
      --buffer-size $UWSGI_BUFFER_SIZE

