import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')

def createNewServiceUser(KEYSTONE_PROTOCOL,
                         KEYSTONE_HOST,
                         KEYSTONE_PORT,
                         SERVICE_NAME,
                         SERVICE_ADMIN_USER,
                         SERVICE_ADMIN_PASSWORD,
                         NEW_USER_NAME,
                         NEW_USER_PASSWORD):

    '''Creates a new user Service (aka domain user keystone).

    In case of HTTP error, return HTTP error
    
    Params:
        - KEYSTONE_PROTOCOL: HTTP or HTTPS
        - KEYSTONE_HOST: Keystone HOSTNAME or IP
        - KEYSTONE_PORT: Keystone PORT
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - NEW_USER_NAME: New user name
        - NEW_USER_PASSWORD: New user password
    '''
    
    idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    try:
        SERVICE_ADMIN_TOKEN = idm.getToken(SERVICE_NAME,
                                           SERVICE_ADMIN_USER,
                                           SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


        #
        # 1. Get service (aka domain)
        #
        ID_DOM1 = idm.getDomain(SERVICE_ADMIN_TOKEN,
                                SERVICE_NAME)

        logger.debug("ID of your service %s:%s" % (SERVICE_NAME, ID_DOM1))

        #
        # 2.  Create user 
        #
        ID_USER = idm.createUserDomain(SERVICE_ADMIN_TOKEN,
                                       ID_DOM1,
                                       SERVICE_NAME,
                                       NEW_USER_NAME,
                                       NEW_USER_PASSWORD)
        logger.debug("ID of user %s: %s" % (NEW_USER_NAME, ID_USER))


    except Exception, ex:
        logger.error(ex)
        return ex.message[0]
    
    logger.info("Summary report:")
    logger.info("ID_DOM1=%s" % ID_DOM1)
    logger.info("ID_USER=%s" % ID_USER)

    return {"id":ID_USER}
