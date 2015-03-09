import logging
import json

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class CreateNewSubService(FlowBase):

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
        - ID: New subservice id
        '''

        data_log = {
            "SERVICE_NAME":"%s" % SERVICE_NAME,
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN,
            "NEW_SUBSERVICE_NAME":"%s" % NEW_SUBSERVICE_NAME,
            "NEW_SUBSERVICE_DESCRIPTION":"%s" % NEW_SUBSERVICE_DESCRIPTION
        }
        logger.debug("createNewSubService invoked with: %s" % json.dumps(data_log, indent=3))

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
                SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                  SERVICE_NAME)

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
            return self.composeErrorCode(ex)

        data_log = {
            "SERVICE_ID":"%s" % SERVICE_ID,
            "ID_PRO1":"%s" % ID_PRO1,
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": ID_PRO1}



