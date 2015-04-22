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
# along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.
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

from settings.common import LOGGING
from orchestrator.core.flow.updateUser import UpdateUser
from orchestrator.api import schemas

logging.config.dictConfig(LOGGING)

def main():

    print "This scripts changes service user password in IoT keystone"
    print ""

    SCRIPT_NAME=sys.argv[0]
    NUM_ARGS_EXPECTED=8

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <SERVICE_NAME>                  Service name"
        print "  <SERVICE_ADMIN_USER>            Service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        Service admin password"
        print "  <NEW_USER_NAME>                 User name"
        print "  <NEW_USER_PASSWORD>             New user password"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        print "                                 bob            \\"
        print "                                 new_password   \\"
        print ""
        print "For bug reporting, please contact with:"
        print "<iot_support@tid.es>"
        return

    KEYSTONE_PROTOCOL=sys.argv[1]
    KEYSTONE_HOST=sys.argv[2]
    KEYSTONE_PORT=sys.argv[3]
    SERVICE_NAME=sys.argv[4]
    SERVICE_ADMIN_USER=sys.argv[5]
    SERVICE_ADMIN_PASSWORD=sys.argv[6]
    USER_NAME=sys.argv[7]
    NEW_USER_PASSWORD=sys.argv[8]

    validate(
        {
            "SERVICE_NAME": SERVICE_NAME,
            "SERVICE_ADMIN_USER": SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": SERVICE_ADMIN_PASSWORD,
            "NEW_SERVICE_USER_NAME": USER_NAME,
            "NEW_SERVICE_USER_PASSWORD": NEW_USER_PASSWORD,
        },
        schemas.json["UserList"])

    flow = UpdateUser(KEYSTONE_PROTOCOL,
                      KEYSTONE_HOST,
                      KEYSTONE_PORT)

    USER_DATA_VALUE = { "password": NEW_USER_PASSWORD }

    res = flow.updateUser(
                         SERVICE_NAME,
                         None,
                         SERVICE_ADMIN_USER,
                         SERVICE_ADMIN_PASSWORD,
                         None,
                         USER_NAME,
                         None,
                         USER_DATA_VALUE)

    pprint.pprint(res)


if __name__ == '__main__':

    main()
