import logging
import json
from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class CreateNewServiceRole(FlowBase):

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
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin token
        - SERVICE_ADMIN_PASSWORD: Service admin token
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_ROLE_NAME: New role name
        Return:
        - id: New role Id
        '''
        data_log = {
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SERVICE_NAME":"%s" % SERVICE_NAME,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN,
            "NEW_ROLE_NAME":"%s" % NEW_ROLE_NAME
        }
        logger.debug("createNewServiceRole invoked with: %s" % json.dumps(data_log, indent=3))

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
                SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                  SERVICE_NAME)


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
            return self.composeErrorCode(ex)


        data_log = {
            "SERVICE_ID":"%s" % SERVICE_ID,
            "ID_ROLE":"%s" % ID_ROLE
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": ID_ROLE}


