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
import logging.config

from settings.common import LOGGING
from orchestrator.core.flow.Domains import Domains

logging.config.dictConfig(LOGGING)

def main():

    print "This script removes a Service (aka keystone domain) in IoT Platform"

    print ""

    SCRIPT_NAME=sys.argv[0]
    NUM_ARGS_EXPECTED=9

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <SERVICE_NAME>                  Service name"
        print "  <DOMAIN_ADMIN_USER>             Regional Service Provider username"
        print "  <DOMAIN_ADMIN_PASSWORD>         Regional Service Provider password"
        print "  <KEYPASS_PROTOCOL>              HTTP or HTTPS"
        print "  <KEYPASS_HOST>                  Keypass (or PEPProxy) HOSTNAME or IP"
        print "  <KEYPASS_PORT>                  Keypass (or PEPProxy) PORT"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValenciaB \\"
        print "                                 cloud_admin    \\"
        print "                                 password       \\"
        print "                                 http           \\"
        print "                                 localhost      \\"
        print "                                 8080           \\"
        print ""
        print "For bug reporting, please contact with:"
        print "<iot_support@tid.es>"
        return

    KEYSTONE_PROTOCOL=sys.argv[1]
    KEYSTONE_HOST=sys.argv[2]
    KEYSTONE_PORT=sys.argv[3]
    SERVICE_NAME=sys.argv[4]
    DOMAIN_ADMIN_USER=sys.argv[5]
    DOMAIN_ADMIN_PASSWORD=sys.argv[6]
    KEYPASS_PROTOCOL=sys.argv[7]
    KEYPASS_HOST=sys.argv[8]
    KEYPASS_PORT=sys.argv[9]

    flow = Domains(KEYSTONE_PROTOCOL,
                            KEYSTONE_HOST,
                            KEYSTONE_PORT,
                            KEYPASS_PROTOCOL,
                            KEYPASS_HOST,
                            KEYPASS_PORT)

    domain_detail = flow.delete_domain(None,
                                       SERVICE_NAME,
                                       DOMAIN_ADMIN_USER,
                                       DOMAIN_ADMIN_PASSWORD,
                                       None)
    pprint.pprint(domain_detail)



if __name__ == '__main__':

    main()
