# Orchestrator

[![License badge](https://img.shields.io/badge/license-AGPL-blue.svg)](https://opensource.org/licenses/AGPL-3.0)
[![Docker badge](https://img.shields.io/docker/pulls/telefonicaiot/orchestrator.svg)](https://hub.docker.com/r/telefonicaiot/orchestrator/)
[![Support badge]( https://img.shields.io/badge/support-sof-yellowgreen.svg)](http://stackoverflow.com/questions/tagged/orchestrator/)
[![Join the chat at https://gitter.im/telefonicaid/orchestrator](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/telefonicaid/orchestrator?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Orchestrator tries to group all provision operations for IoT platform that typically implies several steps or several systems' interaction.
Orchestrator exposes an API and provides scripts to perform all these operations. Scripts simplifies the inherent usage of keystone, such as usage of long identifiers not so easy to remember and to use, using names and resolving internally to deal with keystone.
Orchestrator scripts can interact with any remote 3rd party, since related host and port should be provideed as argument to earch script.


A typical scenario for IoT Platform can be [these scenarios](https://github.com/telefonicaid/orchestrator/blob/master/src/tests/scenarios/SCENARIOS.md).


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
- Retrieve stats about UWSGI server usage
- Create, List, Modify LDAP Users
- Create, List, Modify LDAP Groups

Orchestrator is based mainly on:
- Python 3 needed
- Django / DjangoRestFramework
- UWSGI

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


---

## License

Orchestrator is licensed under [Affero General Public License (GPL)
version 3](./LICENSE).

© 2026 Telefonica Investigación y Desarrollo, S.A.U

<details>
<summary><strong>Further information on the use of the AGPL open source license</strong></summary>
     
### Are there any legal issues with AGPL 3.0? Is it safe for me to use?

There is absolutely no problem in using a product licensed under AGPL 3.0. Issues with GPL
(or AGPL) licenses are mostly related with the fact that different people assign different
interpretations on the meaning of the term “derivate work” used in these licenses. Due to this,
some people believe that there is a risk in just _using_ software under GPL or AGPL licenses
(even without _modifying_ it).

For the avoidance of doubt, the owners of this software licensed under an AGPL-3.0 license
wish to make a clarifying public statement as follows:

> Please note that software derived as a result of modifying the source code of this
> software in order to fix a bug or incorporate enhancements is considered a derivative
> work of the product. Software that merely uses or aggregates (i.e. links to) an otherwise
> unmodified version of existing software is not considered a derivative work, and therefore
> it does not need to be released as under the same license, or even released as open source.

</details>
