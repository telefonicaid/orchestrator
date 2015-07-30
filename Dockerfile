FROM centos:6

MAINTAINER Alvaro Vega <alvaro.vegagarcia@telefonica.com>

RUN yum update -y && yum install -y wget
RUN wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum localinstall -y --nogpgcheck epel-release-6-8.noarch.rpm
RUN yum install -y python git python-pip python-devel python-virtualenv gcc ssh

RUN mkdir -p /opt/orchestrator
COPY . /opt/orchestrator

WORKDIR /opt/orchestrator
RUN pip install -r requirements.txt

EXPOSE 8084

WORKDIR /opt/orchestrator/bin
CMD ["orchestrator-daemon.sh", "start"]



