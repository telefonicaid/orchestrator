import sys
import pprint
from jsonschema import validate
import logging.config

from src.settings.common import LOGGING
from orchestrator.core.flow.createNewServiceRole import CreateNewServiceRole
from orchestrator.api import schemas

logging.config.dictConfig(LOGGING)

def main():

    print "This script creates a new role service in IoT keystone"
    print ""

    SCRIPT_NAME=sys.argv[0]
    NUM_ARGS_EXPECTED=10

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <SERVICE_NAME>                  Service name"
        print "  <SERVICE_ADMIN_USER>            New service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        New service admin password"
        print "  <NEW_ROLE_NAME>                 Name of new role"
        print "  <KEYPASS_PROTOCOL>              HTTP or HTTPS"
        print "  <KEYPASS_HOST>                  Keypass (or PEPProxy) HOSTNAME or IP"
        print "  <KEYPASS_PORT>                  Keypass (or PEPProxy) PORT"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        print "                                 ServiceCustomer\\"
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
    SERVICE_ADMIN_USER=sys.argv[5]
    SERVICE_ADMIN_PASSWORD=sys.argv[6]
    NEW_ROLE_NAME=sys.argv[7]
    KEYPASS_PROTOCOL=sys.argv[8]
    KEYPASS_HOST=sys.argv[9]
    KEYPASS_PORT=sys.argv[10]

    validate(
        {
            "SERVICE_NAME": SERVICE_NAME,
            "SERVICE_ADMIN_USER": SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": SERVICE_ADMIN_PASSWORD,
            "NEW_ROLE_NAME": NEW_ROLE_NAME,
        },
        schemas.json["Role"])

    flow = CreateNewServiceRole(KEYSTONE_PROTOCOL,
                                KEYSTONE_HOST,
                                KEYSTONE_PORT,
                                KEYPASS_PROTOCOL,
                                KEYPASS_HOST,
                                KEYPASS_PORT)

    res = flow.createNewServiceRole(
                         None,
                         SERVICE_NAME,
                         SERVICE_ADMIN_USER,
                         SERVICE_ADMIN_PASSWORD,
                         None,
                         NEW_ROLE_NAME,
                         None)
    pprint.pprint(res)

if __name__ == '__main__':

    main()
