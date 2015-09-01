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
import logging.config
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.append("/var/env-orchestrator/lib/python2.6/site-packages/iotp-orchestrator")

from settings.common import LOGGING
from orchestrator.core.flow.Context import Context

try: logging.config.dictConfig(LOGGING)
except AttributeError: logging.basicConfig(level=logging.WARNING)


def main():

    print "This script creates a new context entity in IoT Context Broker"
    print "and subscribe to it"
    print ""

    SCRIPT_NAME = sys.argv[0]
    NUM_ARGS_EXPECTED = 14

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             Keystone PROTOCOL: HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <SERVICE_NAME>                  Service name"
        print "  <SERVICE_USER_NAME>             Service user username"
        print "  <SERVICE_USER_PASSWORD>         Service user password"
        print "  <CB_PROTOCOL>                   ContextBroker (or PEPProxy) PROTOCOL: HTTP or HTTPS"
        print "  <CB_HOST>                       ContextBroker (or PEPProxy) HOSTNAME or IP"
        print "  <CB_PORT>                       ContextBroker (or PEPProxy) PORT"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 smartcity      \\"
        print "                                 Basuras        \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        print "                                 http           \\"
        print "                                 localhost      \\"
        print "                                 1026           \\"
        print "                                 entity_test    \\"
        print "                                 entity_test_id \\"
        print "                                 []             \\"
        print "                                 test_url       \\"
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
    ORION_PROTOCOL = sys.argv[8]
    ORION_HOST = sys.argv[9]
    ORION_PORT = sys.argv[10]
    ENTITY_TYPE = sys.argv[11]
    ENTITY_ID = sys.argv[12]
    ATTRIBUTES = sys.argv[13]
    REFERENCE_URL = sys.argv[14]


    flow = Context(KEYSTONE_PROTOCOL,
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

    res = flow.createEntitySubscribe(
        SERVICE_NAME,
        None,
        SUBSERVICE_NAME,
        None,
        SERVICE_USER_NAME,
        SERVICE_USER_PASSWORD,
        None,
        ENTITY_TYPE,
        ENTITY_ID,
        ATTRIBUTES,
        REFERENCE_URL)

    pprint.pprint(res)

    if 'error' in res:
        sys.exit(res['code'])

if __name__ == '__main__':

    main()
