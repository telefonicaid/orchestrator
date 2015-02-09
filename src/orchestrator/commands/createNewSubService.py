import sys
import pprint
from orchestrator.core.flow.createNewService import createNewSubService



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
        print "  <SERVICE_ADMIN_USER>            Service admin username"
        print "  <SERVICE_ADMIN_PASSWORD>        Service admin password"
        print "  <NEW_SUBSERVICE_NAME>           New subservice name"
        print "  <NEW_SUBSERVICE_DESCRIPTION>    New subservice description"        
        print ""
        print "  Typical usage:"
        print "     %s http           \\" % SCRIPT_NAME
        print "                                 localhost      \\"
        print "                                 5000           \\"
        print "                                 SmartValencia  \\"
        print "                                 adm1           \\"
        print "                                 password       \\"
        print "                                 Electricidad   \\"
        print "                                 electricidad   \\"
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
    NEW_SUBSERVICE_NAME=sys.argv[7]
    NEW_SUBSERVICE_DESCRIPTION=sys.argv[8]


    #parser = argparse.ArgumentParser(
    #         description='Utilities to update API documentation from code')
    # parser.add_argument('-p', '--path', dest='path', default=None,
    #                    help='Path for UDo-wiki repository')
    # parser.add_argument('--tables', dest='tables', action='store_true',
    #                    help='Shows tables draft')
    #args = parser.parse_args()
    
    flow = createNewSubService(KEYSTONE_PROTOCOL,
                               KEYSTONE_HOST,
                               KEYSTONE_PORT)
    
    res = flow.createNewSubService(
                        SERVICE_NAME,
                        None,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD,
                        None,
                        NEW_SUBSERVICE_NAME,
                        NEW_SUBSERVICE_DESCRIPTION)
    pprint.pprint(res)


if __name__ == '__main__':
    
    main()
