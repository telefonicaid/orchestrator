import logging
from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')

def assignRoleServiceUser(KEYSTONE_PROTOCOL,
                          KEYSTONE_HOST,
                          KEYSTONE_PORT,
                          SERVICE_NAME,
                          SERVICE_ADMIN_USER,
                          SERVICE_ADMIN_PASSWORD,
                          ROLE_NAME,
                          SERVICE_USER_NAME):

    '''assigns a service role to an user in IoT keystone).

    In case of HTTP error, return HTTP error

    Params:
        - KEYSTONE_PROTOCOL: HTTP or HTTPS
        - KEYSTONE_HOST: Keystone HOSTNAME or IP
        - KEYSTONE_PORT: Keystone PORT
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - ROLE_NAME: Role name
        - SERVICE_USER_NAME: User service name
    Return:
        - ?
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
        # 2.  Get role
        #
        ID_ROLE = idm.getRoleId(SERVICE_ADMIN_TOKEN,
                                ROLE_NAME)
        logger.debug("ID of user %s: %s" % (ROLE_NAME, ID_ROLE))

        #
        # 3.  Get User
        #
        ID_USER = idm.getUserId(SERVICE_ADMIN_TOKEN,
                                SERVICE_USER_NAME)
        logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, ID_USER))


        #
        # 4.  Grant role to user in service
        #
        idm.grantDomainRole(SERVICE_ADMIN_TOKEN,
                            ID_DOM1,
                            ID_USER,
                            ID_ROLE)


    except Exception, ex:
        logger.error(ex)
        return ex.message[0]

    logger.info("Summary report:")
    logger.info("ID_DOM1=%s" % ID_DOM1)
    logger.info("ID_USER=%s" % ID_USER)
    logger.info("ID_ROLE=%s" % ID_ROLE)

    return {}
