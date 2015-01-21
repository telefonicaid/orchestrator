import logging
from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')

def assignRoleSubServiceUser(KEYSTONE_PROTOCOL,
                             KEYSTONE_HOST,
                             KEYSTONE_PORT,
                             SERVICE_NAME,
                             SUBSERVICE_NAME,                             
                             SERVICE_ADMIN_USER,
                             SERVICE_ADMIN_PASSWORD,
                             ROLE_NAME,
                             SERVICE_USER_NAME):

    '''Assigns a subservice role to an user in IoT keystone.

    In case of HTTP error, return HTTP error
    
    Params:
        - KEYSTONE_PROTOCOL: HTTP or HTTPS
        - KEYSTONE_HOST: Keystone HOSTNAME or IP
        - KEYSTONE_PORT: Keystone PORT
        - SERVICE_NAME: Service name
        - SERVICE_NAME: SubService name    
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - ROLE_NAME: Role name
        - SERVICE_USER_NAME: User service name
    Return:
        - ¿?
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

        ID_DOM1 = idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                  SERVICE_NAME)

        logger.debug("ID of your service %s:%s" % (SERVICE_NAME, ID_DOM1))



        #
        # 2. Get SubService (aka project)
        #
        
        ID_PRO1 = idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                   SERVICE_NAME,
                                   SUBSERVICE_NAME)

        logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME, ID_PRO1))

        #
        # 3. Get role
        #
        ID_ROLE = idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      ROLE_NAME)
        logger.debug("ID of role %s: %s" % (ROLE_NAME, ID_ROLE))

        #
        # 4. Get User
        #
        ID_USER = idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      SERVICE_USER_NAME)
        logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, ID_USER))


        #
        # 5. Grant role to user in service
        #
        idm.grantProjectRole(SERVICE_ADMIN_TOKEN,
                             ID_PRO1,
                             ID_USER,
                             ID_ROLE)
        
        
    except Exception, ex:
        logger.error(ex)
        return ex.message[0]
    
    logger.info("Summary report:")
    logger.info("ID_PRO1=%s" % ID_PRO1)
    logger.info("ID_USER=%s" % ID_USER)
    logger.info("ID_ROLE=%s" % ID_ROLE)

    return {}
