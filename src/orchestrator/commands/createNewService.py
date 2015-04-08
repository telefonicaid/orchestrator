#-*- coding: utf-8 -*-
import sys
import pprint
from jsonschema import validate
from jsonschema import Draft4Validator
import logging.config

from src.settings.common import LOGGING
from orchestrator.core.flow.createNewService import CreateNewService
from orchestrator.api import schemas

logging.config.dictConfig(LOGGING)



def main():

    print "This script creates a new service in IoT keystone"
    print "including admin user with role admin, subservice roles"
    print "and configures keypass policies for orion and perseo"
    print ""

    SCRIPT_NAME=sys.argv[0]
    NUM_ARGS_EXPECTED=13

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <DOMAIN_NAME>                   Admin Domain name"
        print "  <DOMAIN_ADMIN_USER>             Regional Service Provider username"
        print "  <DOMAIN_ADMIN_PASSWORD>         Regional Service Provider password"
        print "  <NEW_SERVICE_NAME>              New service name"
        print "  <NEW_SERVICE_DESCRIPTION>       New service description"
        print "  <NEW_SERVICE_ADMIN_USER>        New service admin username"
        print "  <NEW_SERVICE_ADMIN_PASSWORD>    New service admin password"
        print "  <KEYPASS_PROTOCOL>              HTTP or HTTPS"
        print "  <KEYPASS_HOST>                  Keypass (or PEPProxy) HOSTNAME or IP"
        print "  <KEYPASS_PORT>                  Keypass (or PEPProxy) PORT"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 admin_domain   \\"
        print "                                 cloud_admin    \\"
        print "                                 password       \\"
        print "                                 SmartValencia  \\"
        print "                                 smartvalencia  \\"
        print "                                 adm1           \\"
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
    DOMAIN_NAME=sys.argv[4]
    DOMAIN_ADMIN_USER=sys.argv[5]
    DOMAIN_ADMIN_PASSWORD=sys.argv[6]
    NEW_SERVICE_NAME=sys.argv[7]
    NEW_SERVICE_DESCRIPTION=sys.argv[8]
    NEW_SERVICE_ADMIN_USER=sys.argv[9]
    NEW_SERVICE_ADMIN_PASSWORD=sys.argv[10]
    KEYPASS_PROTOCOL=sys.argv[11]
    KEYPASS_HOST=sys.argv[12]
    KEYPASS_PORT=sys.argv[13]

    #parser = argparse.ArgumentParser(
    #         description='Utilities to update API documentation from code')
    # parser.add_argument('-p', '--path', dest='path', default=None,
    #                    help='Path for UDo-wiki repository')
    # parser.add_argument('--tables', dest='tables', action='store_true',
    #                    help='Shows tables draft')
    #args = parser.parse_args()

    #Draft4Validator.check_schema(schemas.json["ServiceCreate"])

    validate(
        {
            "DOMAIN_NAME": DOMAIN_NAME,
            "DOMAIN_ADMIN_USER": DOMAIN_ADMIN_USER,
            "DOMAIN_ADMIN_PASSWORD": DOMAIN_ADMIN_PASSWORD,
            "NEW_SERVICE_NAME": NEW_SERVICE_NAME,
            "NEW_SERVICE_DESCRIPTION": NEW_SERVICE_DESCRIPTION,
            "NEW_SERVICE_ADMIN_USER": NEW_SERVICE_ADMIN_USER,
            "NEW_SERVICE_ADMIN_PASSWORD": NEW_SERVICE_ADMIN_PASSWORD,
        },
        schemas.json["ServiceCreate"])

    flow = CreateNewService(KEYSTONE_PROTOCOL,
                            KEYSTONE_HOST,
                            KEYSTONE_PORT,
                            KEYPASS_PROTOCOL,
                            KEYPASS_HOST,
                            KEYPASS_PORT)

    res = flow.createNewService(
                          DOMAIN_NAME,
                          DOMAIN_ADMIN_USER,
                          DOMAIN_ADMIN_PASSWORD,
                          None,
                          NEW_SERVICE_NAME,
                          NEW_SERVICE_DESCRIPTION,
                          NEW_SERVICE_ADMIN_USER,
                          NEW_SERVICE_ADMIN_PASSWORD,
                          None)



    pprint.pprint(res)

if __name__ == '__main__':

    main()
