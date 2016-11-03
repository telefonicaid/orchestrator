# <a name="top"> Orchestrator </a>

[![Build Status](http://ci-iot-deven-01.hi.inet/jenkins/job/IOTP-Orchestrator-Package/badge/icon)](http://ci-iot-deven-01.hi.inet/jenkins/job/IOTP-Orchestrator-Package/)
[![License badge](https://img.shields.io/badge/license-AGPL-blue.svg)](https://opensource.org/licenses/AGPL-3.0)
[![Travis badge](https://travis-ci.org/telefonicaid/orchestrator.svg?branch=master)](https://travis-ci.org/telefonicaid/orchestrator)
[![Docker badge](https://img.shields.io/docker/pulls/telefonicaiot/orchestrator.svg)](https://hub.docker.com/r/telefonicaiot/orchestrator/)
[![Support badge]( https://img.shields.io/badge/support-sof-yellowgreen.svg)](http://stackoverflow.com/questions/tagged/orchestrator/)
[![Join the chat at https://gitter.im/telefonicaid/orchestrator](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/telefonicaid/orchestrator?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Orchestrator tries to group all provision operations for IoT platform that tipically implies several steps or several systems interaction.
Orchestrator exposes an API and provide scripts commands to perform all these operations. Script commands simplifies the inherent usage of keystone, such as usage of long identifiers no so easy to remember and to use, using names al resolving internally to deal with keystone.
Orchestrator Script commands can interact with any remote Keystone and Keypass, since related host and port should be provideed as argument to earch script.
Orchestrator is used maninly by [IoT Portal](https://pdihub.hi.inet/fiware/iotp-portal) and operation team

A tipical scenario for IoT Platform can be [scenario_test](https://pdihub.hi.inet/ep/fiware-components/wiki/Keystone-scenario-test) or [these](https://github.com/telefonicaid/orchestrator/blob/master/src/tests/scenarios/SCENARIOS.md)

- Create/List/Update/Delete services
- Create/List/Update/Delete subservices
- Create/List/Update/Delete users in a service
- Create/List/Update/Delete roles in a service
- Assign/unassign roles to users in a service
- Create/List Trust Tokens
- Activate / deactivate IoT Modules
- Retrieve statistics about API usage

Orchestrator is based mainly on:
- Python
- Django / DjangoRestFramework
- httplib

Orchestrator relies on these other IoT parts:
- Identity Manager (Keystone)
- Access Control (Keypass)
- Context Broker (Orion)
- IoTAgent (IoTA)
- CEP (Perseo)

These are all dependencies [requirements.txt](https://github.com/telefonicaid/orchestrator/blob/master/requirements.txt)

Orchestrator needs a WSGI server like Apache, Lighttpd or NGIX. [wsgi.py](https://github.com/telefonicaid/orchestrator/blob/master/src/wsgi.py)

Orchestrator interacts mainly with Identity Manager [Keystone](https://github.com/telefonicaid/fiware-keystone-scim) and Access Control [Keypass](https://github.com/telefonicaid/fiware-keypass).
Since ContextBroker and IotAgent are secured elements (by [PepProxy](https://github.com/telefonicaid/fiware-pep-steelskin)) orchestrator can interact directly with tem using user provided credencials. If credencials or access control level is not enoght then orchestrator operation will not be performed.

In this README document you will find how to get started with the application and basic concepts. For a more detailed information you can read the following docs:

* [API](http://docs.orchestrator2.apiary.io)
* [scripts](SCRIPTS.md)
* [Logs and Alarms](TROUBLESHOOTING.md)
* [Installation guide](INSTALL.md)
* [Configuration](CONFIG.md)
* [IoTModules](IOTMODULES.md)
* [Docker configuraton](DOCKER.md)

