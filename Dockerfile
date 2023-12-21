ARG  IMAGE_TAG=12.4-slim
FROM debian:${IMAGE_TAG}

MAINTAINER Alvaro Vega <alvaro.vegagarcia@telefonica.com>

ARG CLEAN_DEV_TOOLS


ENV ORCHESTRATOR_USER orchestrator
# By default all linux users non root, has a UID above 1000, so it's taken 10001 which would never end up allocated automatically.
ENV ORCHESTRATOR_USER_UID 10001
ENV ORCHESTRATOR_VERSION 4.6.0
ENV python_lib /var/env-orchestrator/lib/python3.11/site-packages
ENV DJANGO_SETTINGS_MODULE settings
ENV PYTHONPATH "${PYTHONPATH}:/opt/orchestrator"
ENV CLEAN_DEV_TOOLS ${CLEAN_DEV_TOOLS:-1}

COPY . /opt/sworchestrator/

WORKDIR $python_lib/iotp-orchestrator

RUN \
    adduser -u ${ORCHESTRATOR_USER_UID} ${ORCHESTRATOR_USER} && \
    # Install security updates
    apt-get -y update && \
    apt-get -y upgrade && \
    # Install dependencies
    apt-get -y install \
      curl \
      python3-dev \
      python3-pip \
      openssl \
      libssl-dev \
      libldap2-dev \
      libsasl2-dev \
      git \
      gcc \
      sed \
      ldap-utils \
      netcat-traditional \
      findutils && \
    # Install from source
    mkdir -p $python_lib/iotp-orchestrator && \
    mkdir -p $python_lib/iotp-orchestrator/bin && \
    cp -r /opt/sworchestrator/src/* $python_lib/iotp-orchestrator && \
    cp -p /opt/sworchestrator/requirements.txt $python_lib/iotp-orchestrator && \
    cp -r /opt/sworchestrator/bin $python_lib/iotp-orchestrator && \
    chmod 755 $python_lib/iotp-orchestrator/bin/orchestrator-entrypoint.sh && \
    chown -R ${ORCHESTRATOR_USER}:${ORCHESTRATOR_USER} $python_lib/iotp-orchestrator && \
    rm /usr/lib/python3.11/EXTERNALLY-MANAGED && \
    pip3 install -r $python_lib/iotp-orchestrator/requirements.txt && \
    find $python_lib/iotp-orchestrator -name "*.pyc" -delete && \
    ln -s $python_lib/iotp-orchestrator /opt/orchestrator && \
    ln -s /opt/orchestrator/orchestrator/commands /opt/orchestrator/bin/ && \
    mkdir -p /var/log/orchestrator && \
    chown -R ${ORCHESTRATOR_USER}:${ORCHESTRATOR_USER} /var/log/orchestrator && \
    # Put orchestrator version
    sed -i 's/ORC_version/'$ORCHESTRATOR_VERSION'/g' /opt/orchestrator/settings/common.py && \
    sed -i 's/\${project.version}/'$ORCHESTRATOR_VERSION'/g' /opt/orchestrator/orchestrator/core/banner.txt && \
    echo "INFO: Cleaning unused software..." && \
    apt-get clean && \
    apt-get -y autoremove --purge && \
    if [ ${CLEAN_DEV_TOOLS} -eq 0 ] ; then exit 0 ; fi && \
    # remove the same packages we installed at the beginning to build Orch
    apt-get -y remove --purge \
       git \
       gcc && \
    apt-get -y autoremove --purge && \
    # Don't need old log files inside docker images
    rm -f /var/log/*log

# Define the entry point
ENTRYPOINT ["/opt/orchestrator/bin/orchestrator-entrypoint.sh"]

EXPOSE 8084

HEALTHCHECK --interval=60s --timeout=5s --start-period=10s \
            CMD curl --fail -X GET http://localhost:8084/v1.0/version || exit 1
