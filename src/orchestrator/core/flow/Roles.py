import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class Roles(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    def roles(self,
                DOMAIN_ID,
                PROJECT_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Roles of a domain (and project).
        
        In case of HTTP error, return HTTP error
        
        Params:
        - DOMAIN_ID: id of domain
        - PROJECT_ID: id of domain         
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        '''
    
        try:
            if not ADMIN_TOKEN: 
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            DOMAIN_ROLES = self.idm.getDomainRoles(ADMIN_TOKEN,
                                                   DOMAIN_ID)
            logger.debug("DOMAIN_ROLES=%s" % ADMIN_TOKEN)


            # Try to filter by PROJECT_ID each ROLE
            if PROJECT_ID:
                PROJECT_ROLES = self.idm.getDomainRoleAssignment(ADMIN_TOKEN,
                                                                 PROJECT_ID)
                logger.debug("PROJECT_ROLES=%s" % PROJECT_ROLES)

            else:
                ROLES = DOMAIN_ROLES
                
            logger.debug("ROLES=%s" % ROLES)

        except Exception, ex:
            logger.error(ex)
            return { "error": str(ex) }
    
        logger.info("Summary report:")
        
        return ROLES



