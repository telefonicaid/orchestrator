import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class CreateNewSubService(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

        
    def createNewSubService(self,
                            SERVICE_NAME,
                            SERVICE_ID,
                            SERVICE_ADMIN_USER,
                            SERVICE_ADMIN_PASSWORD,
                            SERVICE_ADMIN_TOKEN,
                            NEW_SUBSERVICE_NAME,
                            NEW_SUBSERVICE_DESCRIPTION):
        
        '''Creates a new SubService (aka project keystone).
        
        In case of HTTP error, return HTTP error
        
        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id 
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - SUBSERVICE_NAME: New subservice name (required)
        - SUBSERVICE_DESCRIPTION: New subservice description
        Return:
        - ID: subservice id
        '''
    
        
        try:
            if not SERVICE_ADMIN_TOKEN: 
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)
            

            #
            # 1. Create service (aka domain)
            #
            if not SERVICE_ID:
                ID_DOM1 = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                               SERVICE_NAME)
                SERVICE_ID=ID_DOM1
            
            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, SERVICE_ID))
            
            #
            # 2.  Create subservice (aka project)
            #
            ID_PRO1 = self.idm.createProject(SERVICE_ADMIN_TOKEN,
                                             SERVICE_ID,
                                             NEW_SUBSERVICE_NAME,
                                             NEW_SUBSERVICE_DESCRIPTION)
            logger.debug("ID of user %s: %s" % (NEW_SUBSERVICE_NAME, ID_PRO1))
            
            
        except Exception, ex:
            logger.error(ex)
            res = { "error": str(ex), "code": 400 }
            if isinstance(ex.message, tuple):
                res['code'] = ex.message[0]
            return res
    
        logger.info("Summary report:")
        logger.info("ID_DOM1=%s" % SERVICE_ID)
        logger.info("ID_PRO1=%s" % ID_PRO1)

        return {"id": ID_PRO1}



