import sys
import pprint
from orchestrator.core.flow.Domains import Domains



def main():

    print "This script updates a Services (aka keystone domain) in IoT Platform"

    print ""

    SCRIPT_NAME=sys.argv[0]
    NUM_ARGS_EXPECTED=7

    if (len(sys.argv) - 1 < NUM_ARGS_EXPECTED):
        print "Usage: %s [args]" % SCRIPT_NAME
        print "Args: "
        print "  <KEYSTONE_PROTOCOL>             HTTP or HTTPS"
        print "  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP"
        print "  <KEYSTONE_PORT>                 Keystone PORT"
        print "  <SERVICE_NAME>                  Service name"
        print "  <NEW_SERVICE_DESCRIPTION>       New domain description"        
        print "  <DOMAIN_ADMIN_USER>             Regional Service Provider username"
        print "  <DOMAIN_ADMIN_PASSWORD>         Regional Service Provider password"
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 smart_valencia \\"        
        print "                                 adm1           \\"
        print "                                 password       \\"
        print ""
        print "For bug reporting, please contact with:"
        print "<iot_support@tid.es>"
        return

    KEYSTONE_PROTOCOL=sys.argv[1]
    KEYSTONE_HOST=sys.argv[2]
    KEYSTONE_PORT=sys.argv[3]
    SERVICE_NAME=sys.argv[4]
    NEW_SERVICE_DESCRIPTION=sys.argv[5]    
    DOMAIN_ADMIN_USER=sys.argv[6]
    DOMAIN_ADMIN_PASSWORD=sys.argv[7]


    flow = Domains(KEYSTONE_PROTOCOL,
                            KEYSTONE_HOST,
                            KEYSTONE_PORT)

    domain_detail = flow.update_domain(None,
                                       SERVICE_NAME,
                                       DOMAIN_ADMIN_USER,
                                       DOMAIN_ADMIN_PASSWORD,
                                       None,
                                       NEW_SERVICE_DESCRIPTION                                       
                                   )
    pprint.pprint(domain_detail)



if __name__ == '__main__':

    main()
