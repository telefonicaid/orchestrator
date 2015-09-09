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

    print "This script register a IOTA device for a sub service in IoT keystone"
    print ""

    SCRIPT_NAME = sys.argv[0]
    NUM_ARGS_EXPECTED = 24

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
        print "  <DEVICE_ID>                     IoTA Device Id"
        print "  <PROTOCOL>                      IoTA Protocol"
        print "  <ENTITY_TYPE>                   Context Broker Entity Type"
        print "  <ATT_INTERNAL_ID>               Context Broker attribute Internal Id"
        print "  <ATT_EXTERNAL_ID>               Context Broker attribute External Id"
        print "  <ATT_CCID>                      Context Broker attribute CCID"
        print "  <ATT_IMEI>                      Context Broker attribute IMEI"
        print "  <ATT_IMSI>                      Context Broker attribute IMSI"
        print "  <ATT_INTERACTION_TYPE>          Context Broker attribute Interaction Type: sync or async"
        print "  <ATT_SERVICE_ID>                Context Broker attribute Service Id"
        print "  <ATT_GEOLOCATION>               Context Broker attribute Geolocation"
        print "  <IOTA_PROTOCOL>                 ioTA protocol: HTTP or HTTPS"
        print "  <IOTA_HOST>                     IoTA HOSTNAME or IP"
        print "  <IOTA_PORT>                     IotA PORT"
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
        print "                                 BlackButton    \\"
        print "                                 TT_BLACKBUTTON \\"
        print "                                 button_dev_00  \\"
        print "                                 ZZZZ           \\"
        print "                                 AAA            \\"
        print "                                 1234567890     \\"
        print "                                 0987654321     \\"
        print "                                 synchronous    \\"
        print "                                 S-001          \\"
        print "                                 40.4188,-3.6919\\"
        print "                                 http           \\"
        print "                                 localhost      \\"
        print "                                 4041           \\"
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

    DEVICE_ID = sys.argv[8]
    PROTOCOL = sys.argv[9]
    ENTITY_TYPE = sys.argv[10]
    ATT_INTERNAL_ID = sys.argv[11]
    ATT_EXTERNAL_ID = sys.argv[12]
    ATT_CCID = sys.argv[13]
    ATT_IMEI = sys.argv[14]
    ATT_IMSI = sys.argv[15]
    ATT_INTERACTION_TYPE = sys.argv[16]
    ATT_SERVICE_ID = sys.argv[17]
    ATT_GEOLOCATION = sys.argv[18]

    IOTA_PROTOCOL = sys.argv[19]
    IOTA_HOST = sys.argv[20]
    IOTA_PORT = sys.argv[21]
    ORION_PROTOCOL = sys.argv[22]
    ORION_HOST = sys.argv[23]
    ORION_PORT = sys.argv[24]

    #parser = argparse.ArgumentParser(
    #         description='Utilities to update API documentation from code')
    # parser.add_argument('-p', '--path', dest='path', default=None,
    #                    help='Path for UDo-wiki repository')
    # parser.add_argument('--tables', dest='tables', action='store_true',
    #                    help='Shows tables draft')
    #args = parser.parse_args()

    validate(
        {
            "SERVICE_NAME": SERVICE_NAME,
            "SUBSERVICE_NAME": SUBSERVICE_NAME,
            "SERVICE_USER_NAME": SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": SERVICE_USER_PASSWORD,
            "DEVICE_ID": DEVICE_ID,
            "PROTOCOL": PROTOCOL,
            "ENTITY_TYPE": ENTITY_TYPE,
            "ATT_INTERNAL_ID,": ATT_INTERNAL_ID,
            "ATT_EXTERNAL_ID": ATT_EXTERNAL_ID,
            "ATT_CCID": ATT_CCID,
            "ATT_IMEI": ATT_IMEI,
            "ATT_IMSI": ATT_IMSI,
            "ATT_INTERACTION_TYPE": ATT_INTERACTION_TYPE,
            "ATT_SERVICE_ID": ATT_SERVICE_ID,
            "ATT_GEOLOCATION": ATT_GEOLOCATION,
        },
        schemas.json["IoTADevice"])

    flow = Projects(KEYSTONE_PROTOCOL,
                    KEYSTONE_HOST,
                    KEYSTONE_PORT,
                    None,
                    None,
                    None,
                    IOTA_PROTOCOL,
                    IOTA_HOST,
                    IOTA_PORT,
                    ORION_PROTOCOL,
                    ORION_HOST,
                    ORION_PORT)

    res = flow.register_device(
        SERVICE_NAME,
        None,
        SUBSERVICE_NAME,
        None,
        SERVICE_USER_NAME,
        SERVICE_USER_PASSWORD,
        None,
        DEVICE_ID,
        PROTOCOL,
        ENTITY_TYPE,
        ATT_INTERNAL_ID,
        ATT_EXTERNAL_ID,
        ATT_CCID,
        ATT_IMEI,
        ATT_IMSI,
        ATT_INTERACTION_TYPE,
        ATT_SERVICE_ID,
        ATT_GEOLOCATION
        )

    pprint.pprint(res)
    if 'error' in res:
        sys.exit(res['code'])

if __name__ == '__main__':

    main()
