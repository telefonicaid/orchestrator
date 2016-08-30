FROM centos:6

MAINTAINER Alvaro Vega <alvaro.vegagarcia@telefonica.com>

ENV ORCHESTRATOR_USER orchestrator
ENV ORCHESTRATOR_VERSION 1.3.0

ENV KEYSTONE_HOST localhost
ENV KEYSTONE_PORT 5001
ENV KEYSTONE_PROTOCOL http

ENV KEYPASS_HOST localhost
ENV KEYPASS_PORT 17070
ENV KEYPASS_PROTOCOL http

ENV ORION_HOST localhost
ENV ORION_PORT 1026
ENV ORION_PROTOCOL http

ENV IOTA_HOST localhost
ENV IOTA_PORT 4052
ENV IOTA_PROTOCOL http

ENV STH_HOST localhost
ENV STH_PORT 18666
ENV STH_PROTOCOL http

ENV PERSEO_HOST localhost
ENV PERSEO_PORT 19090
ENV PERSEO_PROTOCOL http

ENV CYGNUS_HOST localhost
ENV CYGNUS_PORT 5050
ENV CYGNUS_PROTOCOL http

ENV python_lib /var/env-orchestrator/lib/python2.6/site-packages

RUN \
    adduser --comment "${ORCHESTRATOR_USER}" ${ORCHESTRATOR_USER} && \
    # Install dependencies
    yum update -y && yum install -y wget && \
    wget https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
    yum localinstall -y --nogpgcheck epel-release-6-8.noarch.rpm && \
    yum install -y python git python-pip python-devel python-virtualenv gcc ssh && \
    yum install -y nc findutils sed && \
    mkdir -p $python_lib/iotp-orchestrator && \
    mkdir -p $python_lib/iotp-orchestrator/bin

COPY ./src/ $python_lib/iotp-orchestrator
COPY ./requirements.txt $python_lib/iotp-orchestrator
COPY ./bin/orchestrator-daemon.sh $python_lib/iotp-orchestrator/bin/orchestrator-daemon.sh
COPY ./bin/orchestrator-daemon $python_lib/iotp-orchestrator/bin/orchestrator-daemon
COPY ./bin/orchestrator-entrypoint.sh $python_lib/iotp-orchestrator/bin/orchestrator-entrypoint.sh

WORKDIR /$python_lib/iotp-orchestrator

RUN \
    chmod 755 $python_lib/iotp-orchestrator/bin/orchestrator-entrypoint.sh && \
    pip install -r $python_lib/iotp-orchestrator/requirements.txt && \
    pip install repoze.lru && \
    find $python_lib/iotp-orchestrator -name "*.pyc" -delete && \
    cp $python_lib/iotp-orchestrator/bin/orchestrator-daemon.sh /etc/init.d/orchestrator && \
    cp $python_lib/iotp-orchestrator/bin/orchestrator-daemon /etc/default/orchestrator-daemon && \
    ln -s $python_lib/iotp-orchestrator /opt/orchestrator && \
    ln -s /opt/orchestrator/orchestrator/commands /opt/orchestrator/bin/ && \
    mkdir -p /var/log/orchestrator && \

    # Set IOTP EndPoints in orchestrator config
    sed -i ':a;N;$!ba;s/KEYSTONE = {[A-Za-z0-9,\"\n: ]*}/KEYSTONE = { \
             \"host\": \"'$KEYSTONE_HOST'\", \
             \"port\": \"'$KEYSTONE_PORT'\", \
             \"protocol\": \"'$KEYSTONE_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py  && \

    sed -i ':a;N;$!ba;s/KEYPASS = {[A-Za-z0-9,\"\n: ]*}/KEYPASS = { \
             \"host\": \"'$KEYPASS_HOST'\", \
             \"port\": \"'$KEYPASS_PORT'\", \
             \"protocol\": \"'$KEYPASS_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py  && \

    sed -i ':a;N;$!ba;s/ORION = {[A-Za-z0-9,\"\n: ]*}/ORION = { \
             \"host\": \"'$ORION_HOST'\", \
             \"port\": \"'$ORION_PORT'\", \
             \"protocol\": \"'$ORION_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py  && \

    sed -i ':a;N;$!ba;s/IOTA = {[A-Za-z0-9,\"\n: ]*}/IOTA = { \
             \"host\": \"'$IOTA_HOST'\", \
             \"port\": \"'$IOTA_PORT'\", \
             \"protocol\": \"'$IOTA_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py  && \

    sed -i ':a;N;$!ba;s/STH = {[A-Za-z0-9,\"\n: ]*}/STH = { \
             \"host\": \"'$STH_HOST'\", \
             \"port\": \"'$STH_PORT'\", \
             \"protocol\": \"'$STH_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py  && \

    sed -i ':a;N;$!ba;s/PERSEO = {[A-Za-z0-9,\"\n: ]*}/PERSEO = { \
             \"host\": \"'$PERSEO_HOST'\", \
             \"port\": \"'$PERSEO_PORT'\", \
             \"protocol\": \"'$PERSEO_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py  && \

    sed -i ':a;N;$!ba;s/CYGNUS = {[A-Za-z0-9,\"\n: ]*}/CYGNUS = { \
             \"host\": \"'$CYGNUS_HOST'\", \
             \"port\": \"'$CYGNUS_PORT'\", \
             \"protocol\": \"'$CYGNUS_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py  && \

    # Put IOT endpoints conf into ochestrator-entrypoint.sh
    sed -i 's/KEYSTONE_PORT=5001/KEYSTONE_PORT='$KEYSTONE_PORT'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/KEYSTONE_PROTOCOL=http/KEYSTONE_PROTOCOL='$KEYSTONE_PROTOCOL'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/KEYPASS_PORT=17070/KEYPASS_PORT='$KEYPASS_PORT'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/KEYPASS_PROTOCOL=http/KEYPASS_PROTOCOL='$KEYPASS_PROTOCOL'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/ORION_PORT=1026/ORION_PORT='$ORION_PORT'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/ORION_PROTOCOL=http/ORION_PROTOCOL='$ORION_PROTOCOL'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/IOTA_PORT=4052/IOTA_PORT='$IOTA_PORT'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/IOTA_PROTOCOL=http/IOTA_PROTOCOL='$IOTA_PROTOCOL'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/STH_PORT=18666/STH_PORT='$STH_PORT'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/STH_PROTOCOL=http/STH_PROTOCOL='$STH_PROTOCOL'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/PERSEO_PORT=19090/PERSEO_PORT='$PERSEO_PORT'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/PERSEO_PROTOCOL=http/PERSEO_PROTOCOL='$PERSEO_PROTOCOL'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/CYGNUS_PORT=5050/CYGNUS_PORT='$CYGNUS_PORT'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    sed -i 's/CYGNUS_PROTOCOL=http/CYGNUS_PROTOCOL='$CYGNUS_PROTOCOL'/g' /opt/orchestrator/bin/orchestrator-entrypoint.sh && \
    # Put orchestrator version
    sed -i 's/ORC_version/'$ORCHESTRATOR_VERSION'/g' /opt/orchestrator/settings/common.py && \
    sed -i 's/\${project.version}/'$ORCHESTRATOR_VERSION'/g' /opt/orchestrator/orchestrator/core/banner.txt

# Define the entry point
ENTRYPOINT ["/opt/orchestrator/bin/orchestrator-entrypoint.sh"]

EXPOSE 8084
