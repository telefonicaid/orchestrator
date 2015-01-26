import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')

def removeUser(KEYSTONE_PROTOCOL,
               KEYSTONE_HOST,
               KEYSTONE_PORT,
               SERVICE_NAME,
               SERVICE_ADMIN_USER,
               SERVICE_ADMIN_PASSWORD,
               USER_NAME):

    '''Removes an user Service (aka domain user keystone).

    In case of HTTP error, return HTTP error
    
    Params:
        - KEYSTONE_PROTOCOL: HTTP or HTTPS
        - KEYSTONE_HOST: Keystone HOSTNAME or IP
        - KEYSTONE_PORT: Keystone PORT
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - USER_NAME: User name
    '''
    
    idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    try:
        SERVICE_ADMIN_TOKEN = idm.getToken(SERVICE_NAME,
                                           SERVICE_ADMIN_USER,
                                           SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


        #
        # 2. Get user ID
        #
        ID_USER = idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                      USER_NAME)
        logger.debug("ID of user %s: %s" % (USER_NAME, ID_USER))


        # TODO: disable us before remove it ?
        
        #
        # 3. Remove user ID
        #
        idm.removeUser(SERVICE_ADMIN_TOKEN,
                       ID_USER)
        #logger.debug("ID of user %s: %s" % (USER_NAME, ID_USER))


    except Exception, ex:
        logger.error(ex)
        return ex.message[0]
    
    logger.info("Summary report:")
    logger.info("ID_USER=%s" % ID_USER)

    #return {"id":ID_USER}
