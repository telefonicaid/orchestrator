# IOTP Orchestrator [![Build Status](http://ci-iot-deven-01/jenkins/job/IOTP-Orchestrator-Package/badge/icon)](http://ci-iot-deven-01/jenkins/job/IOTP-Orchestrator-Package/)

Orchestrator tries to group all provision operations for IoT platform that tipically implies several steps or several system interaction.
Orchestrator exposes an API and provide scripts commands to perform all these operations.
Orchestrator is used maninly by IoT portal

- Create/list services
- Create/list subservices
- Create/list/modify/delete users
- Assign/unassingn roles to users

Orchestrator is based mainly on:
- Python
- Django / DjangoRestFramework
- httplib

Orchestrator needs a WSGI server like Apache, Lighttp or NGIX

Orchestrator interacts mainly with Identity Manager (keystone) and Access Control (keypass)


In this README document you will find how to get started with the application and basic concepts. For a more detailed information you can read the following docs:

* [API](http://docs.piotp.apiary.io/#orchestrator)
* [Logs and Alarms](TROUBLESHOOTING.md)
* [Installation guide](INSTALL.md)
* [Configuration](CONFIG.md)

