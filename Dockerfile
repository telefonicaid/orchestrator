FROM centos:6

MAINTAINER Alvaro Vega <alvaro.vegagarcia@telefonica.com>

ENV ORCHESTRATOR_USER orchestrator
ENV GIT_REV_ORCHESTRATOR develop
ENV CLEAN_DEV_TOOLS 1

ENV KEYSTONE_HOST mylocalhost
ENV KEYSTONE_PORT 5002
ENV KEYSTONE_PROTOCOL https

ENV KEYPASS_HOST localhost
ENV KEYPASS_PORT 17070
ENV KEYPASS_PROTOCOL http

ENV ORION_HOST localhost
ENV ORION_PORT 1026
ENV ORION_PROTOCOL http

ENV STH_HOST localhost
ENV STH_PORT 18666
ENV STH_PROTOCOL http

ENV PERSEO_HOST localhost
ENV PERSEO_PORT 19090
ENV PERSEO_PROTOCOL http


RUN adduser --comment "${ORCHESTRATOR_USER}" ${ORCHESTRATOR_USER}

WORKDIR /tmp

RUN \
    # Install dependencies
    yum update -y && yum install -y wget && \
    wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
    yum localinstall -y --nogpgcheck epel-release-6-8.noarch.rpm && \
    yum install -y python git python-pip python-devel python-virtualenv gcc ssh && \
    # Install orchestrator from source
    git clone https://github.com/telefonicaid/orchestrator && \
    cd orchestrator && \
    git checkout ${GIT_REV_ORCHESTRATOR} && \
    pip install -r requirements.txt && \
    pip install repoze.lru

ENV python_lib /var/env-orchestrator/lib/python2.6/site-packages

RUN mkdir -p $python_lib/iotp-orchestrator
COPY ./src/ $python_lib/iotp-orchestrator
RUN find $python_lib/iotp-orchestrator -name "*.pyc" -delete
COPY ./bin/orchestrator-daemon.sh /etc/init.d/orchestrator
COPY ./bin/orchestrator-daemon /etc/default/orchestrator-daemon
RUN ln -s $python_lib/iotp-orchestrator /opt/orchestrator
RUN ln -s /opt/orchestrator/orchestrator/commands /opt/orchestrator/bin
RUN mkdir -p /var/log/orchestrator


# Set IOTP EndPoints in orchestrator config
RUN sed -i ':a;N;$!ba;s/KEYSTONE = {[A-Za-z0-9,\"\n: ]*}/KEYSTONE = { \
             \"host\": \"'$KEYSTONE_HOST'\", \
             \"port\": \"'$KEYSTONE_PORT'\", \
             \"protocol\": \"'$KEYSTONE_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

RUN sed -i ':a;N;$!ba;s/KEYPASS = {[A-Za-z0-9,\"\n: ]*}/KEYPASS = { \
             \"host\": \"'$KEYPASS_HOST'\", \
             \"port\": \"'$KEYPASS_PORT'\", \
             \"protocol\": \"'$KEYPASS_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

RUN sed -i ':a;N;$!ba;s/ORION = {[A-Za-z0-9,\"\n: ]*}/ORION = { \
             \"host\": \"'$ORION_HOST'\", \
             \"port\": \"'$ORION_PORT'\", \
             \"protocol\": \"'$ORION_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

RUN sed -i ':a;N;$!ba;s/STH = {[A-Za-z0-9,\"\n: ]*}/STH = { \
             \"host\": \"'$STH_HOST'\", \
             \"port\": \"'$STH_PORT'\", \
             \"protocol\": \"'$STH_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

RUN sed -i ':a;N;$!ba;s/PERSEO = {[A-Za-z0-9,\"\n: ]*}/PERSEO = { \
             \"host\": \"'$PERSEO_HOST'\", \
             \"port\": \"'$PERSEO_PORT'\", \
             \"protocol\": \"'$PERSEO_PROTOCOL'\" \
}/g' /opt/orchestrator/settings/dev.py

RUN cat /opt/orchestrator/settings/dev.py

WORKDIR /
CMD ["/opt/orchestrator/bin/orchestrator-daemon.sh", "start"]
EXPOSE 8084
