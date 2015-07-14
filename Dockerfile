FROM centos:6

MAINTAINER IoT team


RUN yum update -y && yum install -y wget
RUN wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum install -y python git python-pip python-devel python-virtualenv

RUN mkdir /github && mkdir /github/telefonicaid

WORKDIR /github/telefonicaid
RUN git clone https://github.com/telefonicaid/orchestrator

WORKDIR  /github/telefonicaid/orchestrator
RUN git fetch && git checkout develop && pip install -r requirements.txt

EXPOSE 8084

WORKDIR /github/telefonicaid/orchestrator
CMD ["orchestrator", "start"]



