# IOTP Orchestrator [![Build Status](http://ci-iot-deven-01/jenkins/job/IOTP-Orchestrator-Package/badge/icon)](http://ci-iot-deven-01/jenkins/job/IOTP-Orchestrator-Package/)


Component to expose an API to automatise provisioning in all the IoT Platform modules.

- Create/list services
- Create/list subservices
- Create/list/modify/delete users
- Assign/unassingn roles to users

Orchestrator is based mainly on:
    Python
    Django / DjangoRestFramework
    httplib

Orchestrator needs a WSGI server like Apache, Lighttp or NGIX

Orchestrator interacts mainly with Identity Manager (keystone) and Access Control (keypass))



In this README document you will find how to get started with the application and basic concepts. For a more detailed information you can read the following docs:

* [API](API.md)
* [Logs and Alarms](TROUBLESHOOTING.md)
* [Installation guide](INSTALL.md)
* [Operation and Maintenance guide](o&m.md)
* [Configuration](CONFIG.md)

Config:
settings.py configure endpoints of Keypass and Keystone
