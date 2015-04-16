import sys
import pprint
from jsonschema import validate
import logging.config

from settings.common import LOGGING
from orchestrator.core.flow.createTrustToken import CreateTrustToken
from orchestrator.api import schemas

logging.config.dictConfig(LOGGING)

def main():

    print "This script creates a new Trust Token in IoT keystone"
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
        print "  <SUBSERVICE_NAME>               SubService name"
        print "  <SERVICE_ADMIN_USER>            New service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        New service admin password"
        print "  <ROLE_NAME>                     Name of role"
        print "  <TRUSTEE_USER_NAME>             Trustee user name"
        print "  <TRUSTOR_USER_NAME>             Trustor user name"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 Electricidad   \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        print "                                 SubServiceAdmin\\"
        print "                                 pep            \\"
        print "                                 adm1           \\"
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
    TRUSTEE_USER_NAME=sys.argv[9]
    TRUSTOR_USER_NAME=sys.argv[10]

    validate(
        {
            "SERVICE_NAME": SERVICE_NAME,
            "SUBSERVICE_NAME": SUBSERVICE_NAME,
            "SERVICE_ADMIN_USER": SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": SERVICE_ADMIN_PASSWORD,
            "ROLE_NAME": ROLE_NAME,
            "TRUSTEE_USER_NAME": TRUSTEE_USER_NAME,
            "TRUSTOR_USER_NAME": TRUSTOR_USER_NAME,
        },
        schemas.json["Trust"])

    flow = CreateTrustToken(KEYSTONE_PROTOCOL,
                            KEYSTONE_HOST,
                            KEYSTONE_PORT)

    res = flow.createTrustToken(
                         SERVICE_NAME,
                         None,
                         SUBSERVICE_NAME,
                         None,
                         SERVICE_ADMIN_USER,
                         SERVICE_ADMIN_PASSWORD,
                         None,
                         ROLE_NAME,
                         None,
                         TRUSTEE_USER_NAME,
                         None,
                         TRUSTOR_USER_NAME,
                         None
                         )
    pprint.pprint(res)

if __name__ == '__main__':

    main()
