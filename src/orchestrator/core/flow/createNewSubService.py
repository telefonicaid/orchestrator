import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')

def createNewSubService(KEYSTONE_PROTOCOL,
                        KEYSTONE_HOST,
                        KEYSTONE_PORT,
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD,
                        NEW_SUBSERVICE_NAME,
                        NEW_SUBSERVICE_DESCRIPTION):
    
    '''Creates a new SubService (aka project keystone).

    In case of HTTP error, return HTTP error
    
    Params:
        - KEYSTONE_PROTOCOL: HTTP or HTTPS
        - KEYSTONE_HOST: Keystone HOSTNAME or IP
        - KEYSTONE_PORT: Keystone PORT
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SUBSERVICE_NAME: New subservice name
        - SUBSERVICE_DESCRIPTION: New subservice description
     Return:
        - ID: subservice id
    '''
    
    #SUB_SERVICE_ADMIN_ROLE_NAME="SubServiceAdmin"
    #SUB_SERVICE_CUSTOMER_ROLE_NAME="SubServiceCustomer"

    idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    try:
        SERVICE_ADMIN_TOKEN = idm.getToken(SERVICE_NAME,
                                           SERVICE_ADMIN_USER,
                                           SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


        #
        # 1. Create service (aka domain)
        #
        ID_DOM1 = idm.getDomain(SERVICE_ADMIN_TOKEN,
                                SERVICE_NAME)

        logger.debug("ID of your service %s:%s" % (SERVICE_NAME, ID_DOM1))

        #
        # 2.  Create subservice (aka project)
        #
        ID_PRO1 = idm.createProject(SERVICE_ADMIN_TOKEN,
                                    ID_DOM1,
                                    NEW_SUBSERVICE_NAME,
                                    NEW_SUBSERVICE_DESCRIPTION)
        logger.debug("ID of user %s: %s" % (NEW_SUBSERVICE_NAME, ID_PRO1))


    except Exception, ex:
        logger.error(ex)
        return ex.message[0]
    
    logger.info("Summary report:")
    logger.info("ID_DOM1=%s" % ID_DOM1)
    logger.info("ID_PRO1=%s" % ID_PRO1)

    return {"id": ID_PRO1}
