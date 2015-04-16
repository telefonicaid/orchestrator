import sys
import pprint
from jsonschema import validate
import logging.config

from src.settings.common import LOGGING
from orchestrator.core.flow.createNewServiceUser import CreateNewServiceUser
from orchestrator.api import schemas

logging.config.dictConfig(LOGGING)

def main():

    print "This script creates a new service in IoT keystone"
    print "including admin user with role admin, subservice roles"
    print "and configures keypass policies for orion and perseo"
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
        print "  <SERVICE_ADMIN_USER>            New service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        New service admin password"
        print "  <NEW_USER_NAME>                 Name of new user"
        print "  <NEW_USER_PASSWORD>             Password of new user"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        print "                                 Electricidad   \\"
        print "                                 bob            \\"
        print "                                 password       \\"
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
    NEW_USER_NAME=sys.argv[7]
    NEW_USER_PASSWORD=sys.argv[8]

    validate(
        {
            "SERVICE_NAME": SERVICE_NAME,
            "SERVICE_ADMIN_USER": SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": SERVICE_ADMIN_PASSWORD,
            "NEW_SERVICE_USER_NAME": NEW_USER_NAME,
            "NEW_SERVICE_USER_PASSWORD": NEW_USER_PASSWORD,
        },
        schemas.json["UserList"])

    flow = CreateNewServiceUser(KEYSTONE_PROTOCOL,
                                KEYSTONE_HOST,
                                KEYSTONE_PORT)

    res = flow.createNewServiceUser(
                         SERVICE_NAME,
                         None,
                         SERVICE_ADMIN_USER,
                         SERVICE_ADMIN_PASSWORD,
                         None,
                         NEW_USER_NAME,
                         NEW_USER_PASSWORD,
                         None,
                         None)
    pprint.pprint(res)


if __name__ == '__main__':

    main()
