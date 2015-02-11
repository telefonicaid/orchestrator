import logging
from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class CreateNewServiceRole(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)
        
    def createNewServiceRole(self,
                             SERVICE_ID,
                             SERVICE_NAME,
                             SERVICE_ADMIN_USER,
                             SERVICE_ADMIN_PASSWORD,
                             SERVICE_ADMIN_TOKEN,
                             NEW_ROLE_NAME):

        '''Creates a new role Service (aka domain role keystone).
        
        In case of HTTP error, return HTTP error
        
        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin token
        - SERVICE_ADMIN_PASSWORD: Service admin token
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_ROLE_NAME: New role name
        '''
    
        
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #
            if not SERVICE_ID:
                ID_DOM1 = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                               SERVICE_NAME)
                SEVICE_ID = ID_DOM1

            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, SERVICE_ID))

            #
            # 2.  Create role
            #
            ID_ROLE = self.idm.createRoleDomain(SERVICE_ADMIN_TOKEN,
                                                SERVICE_ID,
                                                NEW_ROLE_NAME)
            logger.debug("ID of user %s: %s" % (NEW_ROLE_NAME, ID_ROLE))


        except Exception, ex:
            logger.error(ex)
            res = { "error": str(ex), "code": 400 }
            if isinstance(ex.message, tuple):
                res['code'] = ex.message[0]
            return res
    
        logger.info("Summary report:")
        logger.info("ID_DOM1=%s" % SERVICE_ID)
        logger.info("ID_ROLE=%s" % ID_ROLE)

        return {"id": ID_ROLE}


