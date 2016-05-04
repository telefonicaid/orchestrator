FROM centos:6

MAINTAINER Alvaro Vega <alvaro.vegagarcia@telefonica.com>

ENV ORCHESTRATOR_USER orchestrator
ENV GIT_REV_ORCHESTRATOR develop
ENV CLEAN_DEV_TOOLS 1

RUN adduser --comment "${ORCHESTRATOR_USER}" ${ORCHESTRATOR_USER}

WORKDIR /opt

RUN \
    yum update -y && yum install -y wget && \
    wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
    yum localinstall -y --nogpgcheck epel-release-6-8.noarch.rpm && \
    yum install -y python git python-pip python-devel python-virtualenv gcc ssh && \
    # Install orchestrator from source
    git clone https://github.com/telefonicaid/orchestrator && \
    cd orchestrator && \
    git checkout ${GIT_REV_ORCHESTRATOR}

WORKDIR /opt/orchestrator
RUN pip install -r requirements.txt

EXPOSE 8084

WORKDIR /opt/orchestrator/bin
CMD ["./orchestrator-daemon.sh", "start"]
