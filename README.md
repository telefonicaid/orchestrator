# <a name="top"> Orchestrator </a>

[![Build Status](http://ci-iot-deven-01.hi.inet/jenkins/job/IOTP-Orchestrator-Package/badge/icon)](http://ci-iot-deven-01.hi.inet/jenkins/job/IOTP-Orchestrator-Package/)
[![License badge](https://img.shields.io/badge/license-AGPL-blue.svg)](https://opensource.org/licenses/AGPL-3.0)
[![Travis badge](https://travis-ci.org/telefonicaid/orchestrator.svg?branch=master)](https://travis-ci.org/telefonicaid/orchestrator)
[![Docker badge](https://img.shields.io/docker/pulls/telefonicaiot/orchestrator.svg)](https://hub.docker.com/r/telefonicaiot/orchestrator/)
[![Support badge]( https://img.shields.io/badge/support-sof-yellowgreen.svg)](http://stackoverflow.com/questions/tagged/orchestrator/)
[![Join the chat at https://gitter.im/telefonicaid/orchestrator](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/telefonicaid/orchestrator?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Orchestrator tries to group all provision operations for IoT platform that typically implies several steps or several systems' interaction.
Orchestrator exposes an API and provides scripts to perform all these operations. Scripts simplifies the inherent usage of keystone, such as usage of long identifiers not so easy to remember and to use, using names and resolving internally to deal with keystone.
Orchestrator scripts can interact with any remote 3rd party, since related host and port should be provideed as argument to earch script.
Orchestrator is used mainly by [IoT Portal](https://pdihub.hi.inet/fiware/iotp-portal) and operation team.

A typical scenario for IoT Platform can be this [scenario test](https://pdihub.hi.inet/ep/fiware-components/wiki/Keystone-scenario-test) or [these scenarios](https://github.com/telefonicaid/orchestrator/blob/master/src/tests/scenarios/SCENARIOS.md).


Orchestrator is used to:
- Create/List/Update/Delete services
- Create/List/Update/Delete subservices
- Create/List/Update/Delete users in a service
- Create/List/Update/Delete roles in a service
- Create/List/Update/Delete groups in a service
- Assign/unassign roles to users in a service
- Create/List Trust Tokens
- Activate / deactivate IoT Modules
- Retrieve statistics and metrics about API usage
- Create, List, Modify LDAP Users

Orchestrator is based mainly on:
- Python 2.7 needed
- Django / DjangoRestFramework
- httplib

Orchestrator relies on these other IoT parts:
- Identity Manager: Keystone (mandatory)
- Access Control: Keypass (mandatory)
- Context Broker: Orion (optional)
- CEP: Perseo (optional)
- Cygnus (optional)
- OpenLDAP (optional)
- Mailer (optional)
- MongoDB (optional)

Some of these IoT parts are optional, this means that orchestrator can work without them but excluding the part of feature in which are involved. This way Keystone and Keypass are mandatory to deal with Orchestrator.


These are all dependencies [requirements.txt](https://github.com/telefonicaid/orchestrator/blob/master/requirements.txt).

Orchestrator needs a WSGI server like Apache, Lighttpd or NGIX: [wsgi.py](https://github.com/telefonicaid/orchestrator/blob/master/src/wsgi.py).

Orchestrator interacts mainly with Identity Manager [Keystone](https://github.com/telefonicaid/fiware-keystone-scim) and Access Control [Keypass](https://github.com/telefonicaid/fiware-keypass).
Since ContextBroker and CEP are secured elements (by [PepProxy](https://github.com/telefonicaid/fiware-pep-steelskin)) orchestrator can interact directly with tem using user provided credencials. If credencials or access control level is not enoght then orchestrator operation will not be performed.

In this README document you could find how to get started with the application and basic concepts. For a more detailed information you can read the following docs:

* [API](http://docs.orchestrator2.apiary.io)
* [Scripts](SCRIPTS.md)
* [Logs and Alarms](TROUBLESHOOTING.md)
* [Installation guide](INSTALL.md)
* [Configuration](CONFIG.md)
* [IoTModules](IOTMODULES.md)
* [Docker configuraton](DOCKER.md)
* [Tests](TESTS.md)

