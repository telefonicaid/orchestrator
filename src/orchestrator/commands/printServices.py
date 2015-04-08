import sys
import pprint
import logging.config

from src.settings.common import LOGGING
from orchestrator.core.flow.Domains import Domains

logging.config.dictConfig(LOGGING)

def main():

    print "This script prints services"

    print ""

    SCRIPT_NAME=sys.argv[0]
    NUM_ARGS_EXPECTED=6

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <DOMAIN_NAME>                   Admin Domain name"
        print "  <DOMAIN_ADMIN_USER>             Regional Service Provider username"
        print "  <DOMAIN_ADMIN_PASSWORD>         Regional Service Provider password"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
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

    flow = Domains(KEYSTONE_PROTOCOL,
                            KEYSTONE_HOST,
                            KEYSTONE_PORT)

    domain_detail = flow.get_domain(None,
                                    DOMAIN_NAME,
                                    DOMAIN_ADMIN_USER,
                                    DOMAIN_ADMIN_PASSWORD,
                                    None)
    pprint.pprint(domain_detail)



if __name__ == '__main__':

    main()
