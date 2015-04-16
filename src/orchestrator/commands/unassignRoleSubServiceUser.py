import sys
import logging.config

from settings.common import LOGGING
from orchestrator.core.flow.Roles import Roles

logging.config.dictConfig(LOGGING)

def main():

    print "This script revokes a role to a service user IoT keystone"
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
        print "  <SUBSERVICE_NAME>               SubService name"
        print "  <SERVICE_ADMIN_USER>            Service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        Service admin password"
        print "  <ROLE_NAME>                     Name of role"
        print "  <SERVICE_USER>                  Service username"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 Electricidad   \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        print "                                 ServiceCustomer\\"
        print "                                 Carl           \\"
        print ""
        print "For bug reporting, please contact with:"
        print "<iot_support@tid.es>"
        return

    KEYSTONE_PROTOCOL=sys.argv[1]
    KEYSTONE_HOST=sys.argv[2]
    KEYSTONE_PORT=sys.argv[3]
    SERVICE_NAME=sys.argv[4]
    SUBSERVICE_NAME=sys.argv[5]
    SERVICE_ADMIN_USER=sys.argv[6]
    SERVICE_ADMIN_PASSWORD=sys.argv[7]
    ROLE_NAME=sys.argv[8]
    SERVICE_USER=sys.argv[9]

    flow = Roles(KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT)

    flow.revokeRoleSubServiceUser(
                             SERVICE_NAME,
                             SUBSERVICE_NAME,
                             None,
                             SERVICE_ADMIN_USER,
                             SERVICE_ADMIN_PASSWORD,
                             None,
                             ROLE_NAME,
                             None,
                             SERVICE_USER,
                             None)


if __name__ == '__main__':

    main()
