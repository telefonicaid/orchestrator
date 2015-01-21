import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')

def createNewService(KEYSTONE_PROTOCOL,
                     KEYSTONE_HOST,
                     KEYSTONE_PORT,
                     DOMAIN_NAME,
                     DOMAIN_ADMIN_USER,
                     DOMAIN_ADMIN_PASSWORD,
                     NEW_SERVICE_NAME,
                     NEW_SERVICE_DESCRIPTION,
                     NEW_SERVICE_ADMIN_USER,
                     NEW_SERVICE_ADMIN_PASSWORD,
                     KEYPASS_PROTOCOL,
                     KEYPASS_HOST,
                     KEYPASS_PORT):

    '''Creates a new Service (aka domain keystone).

    In case of HTTP error, return HTTP error
    
    Params:
        - KEYSTONE_PROTOCOL: HTTP or HTTPS
        - KEYSTONE_HOST: Keystone HOSTNAME or IP
        - KEYSTONE_PORT: Keystone PORT
        - DOMAIN_NAME: Admin Domain name
        - DOMAIN_ADMIN_USER: Regional Service Provider username
        - DOMAIN_ADMIN_PASSWORD: Regional Service Provider password
        - NEW_SERVICE_NAME: New service name
        - NEW_SERVICE_DESCRIPTION: New service description
        - NEW_SERVICE_ADMIN_USER: New service admin username
        - NEW_SERVICE_ADMIN_PASSWORD: New service admin password
        - KEYPASS_PROTOCOL: HTTP or HTTPS
        - KEYPASS_HOST: Keypass (or PEPProxy) HOSTNAME or IP
        - KEYPASS_PORT: Keypass (or PEPProxy) PORT
    Return:
        - TOKEN: service admin token
    '''
    
    SUB_SERVICE_ADMIN_ROLE_NAME="SubServiceAdmin"
    SUB_SERVICE_CUSTOMER_ROLE_NAME="SubServiceCustomer"

    idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT,
                        KEYPASS_PROTOCOL, KEYPASS_HOST, KEYPASS_PORT)
    try:
        CLOUD_ADMIN_TOKEN = idm.getToken(DOMAIN_NAME,
                                         DOMAIN_ADMIN_USER,
                                         DOMAIN_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % CLOUD_ADMIN_TOKEN)


        #
        # 1. Create service (aka domain)
        #
        ID_DOM1 = idm.createDomain(CLOUD_ADMIN_TOKEN,
                                   NEW_SERVICE_NAME,
                                   NEW_SERVICE_DESCRIPTION)
        logger.debug("ID of your new service %s:%s" % (NEW_SERVICE_NAME, ID_DOM1))

        #
        # 2. Create user admin for new service (aka domain)
        #
        ID_ADM1 = idm.createUserAdminDomain(CLOUD_ADMIN_TOKEN,
                                            NEW_SERVICE_NAME,
                                            ID_DOM1,
                                            NEW_SERVICE_ADMIN_USER,
                                            NEW_SERVICE_ADMIN_PASSWORD)
        logger.debug("ID of user %s: %s" % (NEW_SERVICE_ADMIN_USER, ID_ADM1))

        #
        # 3. Grant Admin role to $NEW_SERVICE_ADMIN_USER of new service
        #
        ADMIN_ROLE_ID = idm.getRoleId(CLOUD_ADMIN_TOKEN,
                                      ROLE_NAME="admin")
        logger.debug("ID of role  %s: %s" % (NEW_SERVICE_ADMIN_USER, ID_ADM1))
        
        idm.grantDomainRole(CLOUD_ADMIN_TOKEN, ID_DOM1, ID_ADM1, ADMIN_ROLE_ID)
        
        NEW_SERVICE_ADMIN_TOKEN = idm.getToken(NEW_SERVICE_NAME,
                                               NEW_SERVICE_ADMIN_USER,
                                               NEW_SERVICE_ADMIN_PASSWORD)
        logger.debug("NEW_SERVICE_ADMIN_TOKEN %s" % NEW_SERVICE_ADMIN_TOKEN)


        #
        # 4. Create SubService roles
        #
        ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN = idm.createDomainRole(
                                                  NEW_SERVICE_ADMIN_TOKEN,
                                                  SUB_SERVICE_ADMIN_ROLE_NAME,
                                                  ID_DOM1)
        logger.debug("ID of role %s: %s" % (SUB_SERVICE_ADMIN_ROLE_NAME,
                                     ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN))

        ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER = idm.createDomainRole(
                                                 NEW_SERVICE_ADMIN_TOKEN,
                                                 SUB_SERVICE_CUSTOMER_ROLE_NAME,
                                                 ID_DOM1)
        logger.debug("ID of role %s: %s" % (SUB_SERVICE_CUSTOMER_ROLE_NAME,
                                     ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER))

        #
        # 5. Provision default platform roles AccessControl policies
        #
        idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                           ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                           POLICY_FILE_NAME='policy-orion-admin.xml')
        idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                           ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                           POLICY_FILE_NAME='policy-perseo-admin.xml')
        idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                           ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                           POLICY_FILE_NAME='policy-orion-customer.xml')
        idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                           ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                           POLICY_FILE_NAME='policy-perseo-customer.xml')


    except Exception, ex:
        logger.error(ex)
        return ex.message[0]
    
    logger.info("Summary report:")
    logger.info("ID_DOM1=%s" % ID_DOM1)
    logger.info("NEW_SERVICE_ADMIN_TOKEN=%s" % NEW_SERVICE_ADMIN_TOKEN)
    logger.info("ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN=%s" % ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN)
    logger.info("ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER=%s" % ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER)

    return {"token": NEW_SERVICE_ADMIN_TOKEN}
