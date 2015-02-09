import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class Users(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    def Users(self,
              SERVICE_ADMIN_USER,
              SERVICE_ADMIN_PASSWORD,
              SERVICE_ADMIN_TOKEN,
              SERVICE_NAME = None,
              SUBSERVICE_NAME = None):

        '''Get users.
        
        In case of HTTP error, return HTTP error
        
        Params:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - SERVICE_NAME: Service name
        - SUBSERVICE_NAME: SubService name        
        '''
    
        try:
            if not SERVICE_ADMIN_TOKEN: 
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            
            ID_DOM1 = self.idm.getDomainId(SERVICE_NAME,
                                           SERVICE_ADMIN_TOKEN)

            SERVICE_ROLES = self.idm.getDomainRoles(ID_DOM1,
                                                    SERVICE_ADMIN_TOKEN)
            logger.debug("SERVICE_ROLES=%s" % SERVICE_ROLES)

            SERVICE_USERS = self.idm.getDomainUsers(ID_DOM1,
                                                    SERVICE_ADMIN_TOKEN)
            logger.debug("SERVICE_USERS=%s" % SERVICE_USERS)

            
            # Get Roles de SubServicio

            # Listar los usuarios de un Servicio
              # Obtener roles de usuario
            
            # Listar los usuarios de un Subservicio
            

        except Exception, ex:
            logger.error(ex)
            return { "error": str(ex) }
    
        logger.info("Summary report:")
        
        #return {"id":ID_USER}



