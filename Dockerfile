FROM centos:7

MAINTAINER Alvaro Vega <alvaro.vegagarcia@telefonica.com>

ENV ORCHESTRATOR_USER orchestrator

ENV ORCHESTRATOR_VERSION 3.2.1

ENV python_lib /var/env-orchestrator/lib/python2.7/site-packages
ENV DJANGO_SETTINGS_MODULE settings
ENV PYTHONPATH "${PYTHONPATH}:/opt/orchestrator"

COPY . /opt/sworchestrator/

WORKDIR $python_lib/iotp-orchestrator

RUN \
    adduser --comment "${ORCHESTRATOR_USER}" ${ORCHESTRATOR_USER} && \
    # Install dependencies
    yum install -y epel-release && yum update -y epel-release && \
    yum install -y yum-plugin-remove-with-leaves python python-pip python-devel openldap-devel python-virtualenv gcc ssh && \
    yum install -y tcping findutils sed && \
    mkdir -p $python_lib/iotp-orchestrator && \
    mkdir -p $python_lib/iotp-orchestrator/bin && \
    cp -rp /opt/sworchestrator/src/* $python_lib/iotp-orchestrator && cp -p /opt/sworchestrator/requirements.txt $python_lib/iotp-orchestrator && \
    cp -rp /opt/sworchestrator/bin $python_lib/iotp-orchestrator && \
    chmod 755 $python_lib/iotp-orchestrator/bin/orchestrator-entrypoint.sh && \
    pip install -r $python_lib/iotp-orchestrator/requirements.txt && \
    pip install repoze.lru && \
    find $python_lib/iotp-orchestrator -name "*.pyc" -delete && \
    ln -s $python_lib/iotp-orchestrator /opt/orchestrator && \
    ln -s /opt/orchestrator/orchestrator/commands /opt/orchestrator/bin/ && \
    mkdir -p /var/log/orchestrator && \
    # Put orchestrator version
    sed -i 's/ORC_version/'$ORCHESTRATOR_VERSION'/g' /opt/orchestrator/settings/common.py && \
    sed -i 's/\${project.version}/'$ORCHESTRATOR_VERSION'/g' /opt/orchestrator/orchestrator/core/banner.txt && \
    echo "INFO: Cleaning unused software..." && \
    rm -rf /opt/sworchestrator && \
    yum erase -y --remove-leaves yum-plugin-remove-with-leaves gcc && \
    # Delete pip cache
    rm -rf ~/.cache && \
    # Erase without dependencies of the document formatting system (man). This cannot be removed using yum 
    # as yum uses hard dependencies and doing so will uninstall essential packages
    rpm -qa groff redhat-logos | xargs -r rpm -e --nodeps && \
    # Clean yum data
    yum clean all && rm -rf /var/lib/yum/yumdb && rm -rf /var/lib/yum/history && \
    # Rebuild rpm data files
    rpm -vv --rebuilddb && \
    # Delete unused locales. Only preserve en_US and the locale aliases
    find /usr/share/locale -mindepth 1 -maxdepth 1 ! -name 'en_US' ! -name 'locale.alias' | xargs -r rm -r && \
    bash -c 'localedef --list-archive | grep -v -e "en_US" | xargs localedef --delete-from-archive' && \
    # We use cp instead of mv as to refresh locale changes for ssh connections
    # We use /bin/cp instead of cp to avoid any alias substitution, which in some cases has been problematic
    /bin/cp -f /usr/lib/locale/locale-archive /usr/lib/locale/locale-archive.tmpl && \
    build-locale-archive && \
    # We don't need to manage Linux account passwords requisites: lenght, mays/mins, etc
    # This cannot be removed using yum as yum uses hard dependencies and doing so will uninstall essential packages
    rm -rf /usr/share/cracklib && \
    # We don't need glibc locale data
    # This cannot be removed using yum as yum uses hard dependencies and doing so will uninstall essential packages
    rm -rf /usr/share/i18n /usr/{lib,lib64}/gconv && \
    # We don't need wallpapers
    rm -rf /usr/share/wallpapers/* && \
    # Don't need old log files inside docker images
    rm -f /tmp/* /var/log/*log

# Define the entry point
ENTRYPOINT ["/opt/orchestrator/bin/orchestrator-entrypoint.sh"]

EXPOSE 8084

