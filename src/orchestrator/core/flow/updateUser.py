import logging

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')

class UpdateUser(FlowBase):

    def updateUser(self,
                   SERVICE_NAME,
                   DOMAIN_ID,
                   SERVICE_ADMIN_USER,
                   SERVICE_ADMIN_PASSWORD,
                   SERVICE_ADMIN_TOKEN,
                   USER_NAME,
                   USER_ID,
                   USER_DATA_VALUE):

        '''Update an User Service (aka domain user keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - DOMAIN_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - USER_NAME: User name
        - USER_ID: User Id
        - USER_DATA_VALUE: user data value in json
        '''
        logger.debug("updateUser invoked with: ")
        logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)
        logger.debug("DOMAIN_ID=%s" % DOMAIN_ID)
        logger.debug("SERVICE_ADMIN_USER=%s" % SERVICE_ADMIN_USER)
        logger.debug("SERVICE_ADMIN_PASSWORD=%s" % SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)
        logger.debug("USER_NAME=%s" % USER_NAME)
        logger.debug("USER_ID=%s" % USER_ID)
        logger.debug("USER_DATA_VALUE=%s" % USER_DATA_VALUE)

        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 2. Get user ID
            #
            if not USER_ID:
                if not DOMAIN_ID:
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                     SERVICE_NAME)

                USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   USER_NAME)
            logger.debug("ID of user %s: %s" % (USER_NAME, USER_ID))

            #
            # 3. Updateuser
            #
            self.idm.updateUser(SERVICE_ADMIN_TOKEN,
                                USER_ID,
                                USER_DATA_VALUE)



        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("USER_ID=%s" % USER_ID)

        #return {"id":ID_USER}
