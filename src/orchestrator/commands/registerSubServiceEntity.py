#!/usr/bin/env python

#
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of IoT orchestrator
#
# IoT orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# IoT orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with IoT orchestrator. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT team
#
import sys
import pprint
from jsonschema import validate
import logging.config
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.append("/var/env-orchestrator/lib/python2.6/site-packages/iotp-orchestrator")

from settings.common import LOGGING
from orchestrator.core.flow.Projects import Projects
from orchestrator.api import schemas

try: logging.config.dictConfig(LOGGING)
except AttributeError: logging.basicConfig(level=logging.WARNING)


def main():

    print "This script register a service entity IOT SubService (keystone project)"
    print ""

    SCRIPT_NAME = sys.argv[0]
    NUM_ARGS_EXPECTED = 20

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <SERVICE_NAME>                  Service name"
        print "  <SUBSERVICE_NAME>               Subservice name"
        print "  <SERVICE_ADMIN_USER>            Service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        Service admin password"
        print "  <ENTITY_TYPE>                   Context Broker Entity Type"
        print "  <ENTITY_ID>                     Context Broker Entity Id"
        print "  <PROTOCOL>                      Protocol"
        print "  <ATT_NAME>                      Context Broker Name attribute"
        print "  <ATT_PROVIDER>                  Context Broker Provider attribute"
        print "  <ATT_ENDPOINT>                  Context Broker Endpoint attribute"
        print "  <ATT_METHOD>                    Context Broker Method attribute"
        print "  <ATT_AUTHENTICATION>            Context Broker Authentication attribute"
        print "  <ATT_INTERACTION_TYPE>          Context Broker Interaction Type attribute"
        print "  <ATT_MAPPING>                   Context Broker Mapping attribute"
        print "  <ATT_TIMEOUT>                   Context Broker Timeout attribute"
        print "  <ORION_PROTOCOL>                ORION protocol: HTTP or HTTPS"
        print "  <ORION_HOST>                    ORION HOSTNAME or IP"
        print "  <ORION_PORT>                    ORION PORT"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 blackbutton    \\"
        print "                                 telepizza      \\"
        print "                                 admin_bb       \\"
        print "                                 4passw0rd      \\"
        print "                                 button_dev_00  \\"
        print "                                 service        \\"
        print "                                 blackbutton-telepizza \\"
        print "                                 TT_BlackButton \\"
        print "                                 blackbutton-telepizza \\"
        print "                                 http://localhost:6500/sync/request \\"
        print "                                 POST \\"
        print "                                 thrid-party \\"
        print "                                 synchronous \\"
        print "                                 XXX \\"
        print "                                 120X \\"
        print "                                 http           \\"
        print "                                 localhost      \\"
        print "                                 1026           \\"
        print ""
        print "For bug reporting, please contact with:"
        print "<iot_support@tid.es>"
        return

    KEYSTONE_PROTOCOL = sys.argv[1]
    KEYSTONE_HOST = sys.argv[2]
    KEYSTONE_PORT = sys.argv[3]
    SERVICE_NAME = sys.argv[4]
    SUBSERVICE_NAME = sys.argv[5]
    SERVICE_USER_NAME = sys.argv[6]
    SERVICE_USER_PASSWORD = sys.argv[7]

    ENTITY_TYPE = sys.argv[8]
    ENTITY_ID = sys.argv[9]
    PROTOCOL = sys.argv[10]

    ATT_NAME = sys.argv[11]
    ATT_PROVIDER = sys.argv[12]
    ATT_ENDPOINT = sys.argv[13]
    ATT_METHOD = sys.argv[14]
    ATT_AUTHENTICATION = sys.argv[15]
    ATT_INTERACTION_TYPE = sys.argv[16]
    ATT_MAPPING = sys.argv[17]
    ATT_TIMEOUT = sys.argv[18]

    ORION_PROTOCOL = sys.argv[19]
    ORION_HOST = sys.argv[20]
    ORION_PORT = sys.argv[21]

    validate(
        {
            "SERVICE_NAME": SERVICE_NAME,
            "SUBSERVICE_NAME": SUBSERVICE_NAME,
            "SERVICE_USER_NAME": SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": SERVICE_USER_PASSWORD,
            "ENTITY_TYPE": ENTITY_TYPE,
            "ENTITY_ID": ENTITY_ID,
            "PROTOCOL": PROTOCOL,
            "ATT_NAME,": ATT_NAME,
            "ATT_PROVIDER,": ATT_PROVIDER,
            "ATT_ENDPOINT,": ATT_ENDPOINT,
            "ATT_METHOD,": ATT_METHOD,
            "ATT_AUTHENTICATION,": ATT_AUTHENTICATION,
            "ATT_INTERACTION_TYPE,": ATT_INTERACTION_TYPE,
            "ATT_MAPPING,": ATT_MAPPING,
            "ATT_TIMEOUT,": ATT_TIMEOUT
        },
        schemas.json["IoTAService"])

    flow = Projects(KEYSTONE_PROTOCOL,
                    KEYSTONE_HOST,
                    KEYSTONE_PORT,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    ORION_PROTOCOL,
                    ORION_HOST,
                    ORION_PORT)

    res, service_name, subservice_name = flow.register_service(
        SERVICE_NAME,
        None,
        SUBSERVICE_NAME,
        None,
        SERVICE_USER_NAME,
        SERVICE_USER_PASSWORD,
        None,
        ENTITY_TYPE,
        ENTITY_ID,
        PROTOCOL,
        ATT_NAME,
        ATT_PROVIDER,
        ATT_ENDPOINT,
        ATT_METHOD,
        ATT_AUTHENTICATION,
        ATT_INTERACTION_TYPE,
        ATT_MAPPING,
        ATT_TIMEOUT
        )

    pprint.pprint(res)
    if 'error' in res:
        sys.exit(res['code'])

if __name__ == '__main__':

    main()
