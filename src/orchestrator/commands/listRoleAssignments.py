import sys
import pprint
from orchestrator.core.flow.Roles import Roles



def main():

    print "This script prints roles in a service"

    print ""

    SCRIPT_NAME=sys.argv[0]
    NUM_ARGS_EXPECTED=6

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <SERVICE_NAME>                  Service name"
        print "  <SERVICE_ADMIN_USER>            Service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        Service admin password"
        # print "  <SUBSERVICE_NAME>               SubService name (optional)"
        # print "  <ROLE_NAME>                     Role Name (optional)"
        # print "  <USER_NAME>                     User Name (optional)"
        # print "  <EFFECTIVE>                     Effective roles (optional)"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        # print "                                 Electricidad   \\"
        # print "                                 SubServiceAdmin\\"
        # print "                                 Alice          \\"
        # print "                                 True           \\"
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
    # SUBSERVICE_NAME=sys.argv[7]
    # ROLE_NAME=sys.argv[8]
    # USER_NAME=sys.argv[9]
    # EFFECTIVE=sys.argv[10]

    flow = Roles(KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT)

    roles = flow.roles_assignments(None,
                                   SERVICE_NAME,
                                   None,
                                   None,
                                   None,
                                   SERVICE_ADMIN_USER,
                                   SERVICE_ADMIN_PASSWORD,
                                   None,
                                   True)

    pprint.pprint(roles)



if __name__ == '__main__':

    main()
