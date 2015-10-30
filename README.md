# IOTP Orchestrator [![Build Status](http://ci-iot-deven-01/jenkins/job/IOTP-Orchestrator-Package/badge/icon)](http://ci-iot-deven-01/jenkins/job/IOTP-Orchestrator-Package/)

Orchestrator tries to group all provision operations for IoT platform that tipically implies several steps or several systems interaction.
Orchestrator exposes an API and provide scripts commands to perform all these operations. Script commands simplifies the inherent usage of keystone, such as usage of long identifiers no so easy to remember and to use, using names al resolving internally to deal with keystone.
Orchestrator Script commands can interact with any remote Keystone and Keypass, since related host and port should be provideed as argument to earch script.
Orchestrator is used maninly by [IoT Portal](https://pdihub.hi.inet/fiware/iotp-portal)

A tipical scenario for IoT Platform can be [scenario_test](https://pdihub.hi.inet/ep/fiware-components/wiki/Keystone-scenario-test) or [these](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/tests/scenarios/SCENARIOS.md)

- Create/list services
- Create/list subservices
- Create/list/modify/delete users
- Assign/unassign roles to users

Orchestrator is based mainly on:
- Python
- Django / DjangoRestFramework
- httplib

These are all dependencies [requirements.txt](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/requirements.txt)

Orchestrator needs a WSGI server like Apache, Lighttpd or NGIX. [wsgi.py](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/wsgi.py)

Orchestrator interacts mainly with Identity Manager [Keystone](https://github.com/telefonicaid/fiware-keystone-scim)  and Access Control [Keypass](https://github.com/telefonicaid/fiware-keypass)


In this README document you will find how to get started with the application and basic concepts. For a more detailed information you can read the following docs:

* [API](http://docs.orchestrator2.apiary.io)
* [scripts](SCRIPTS.md)
* [Logs and Alarms](TROUBLESHOOTING.md)
* [Installation guide](INSTALL.md)
* [Configuration](CONFIG.md)

