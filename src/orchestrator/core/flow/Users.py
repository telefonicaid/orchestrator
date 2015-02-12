import logging

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class Users(FlowBase):

    def users(self,
              SERVICE_ID,
              SERVICE_ADMIN_USER,
              SERVICE_ADMIN_PASSWORD,
              SERVICE_ADMIN_TOKEN):

        '''Get users.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        '''
        logger.debug("users invoked with: ")
        logger.debug("SERVICE_ID=%s" % SERVICE_ID)
        logger.debug("SERVICE_ADMIN_USER=%s" % SERVICE_ADMIN_USER)
        logger.debug("SERVICE_ADMIN_PASSWORD=%s" % SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                         SERVICE_ADMIN_USER,
                                                         SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)



            ID_DOM1 = SERVICE_ID


            SERVICE_ROLES = self.idm.getDomainRoles(SERVICE_ADMIN_TOKEN,
                                                    ID_DOM1)

            logger.debug("SERVICE_ROLES=%s" % SERVICE_ROLES)

            SERVICE_USERS = self.idm.getDomainUsers(SERVICE_ADMIN_TOKEN,
                                                    ID_DOM1)

            logger.debug("SERVICE_USERS=%s" % SERVICE_USERS)


            # Get Roles de SubServicio

            # Listar los usuarios de un Servicio
              # Obtener roles de usuario

            # Listar los usuarios de un Subservicio


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("SERVICE_USERS=%s" % SERVICE_USERS)
        return SERVICE_USERS



    def user(self,
              SERVICE_ID,
              USER_ID,
              SERVICE_ADMIN_USER,
              SERVICE_ADMIN_PASSWORD,
              SERVICE_ADMIN_TOKEN):

        '''Get user detail

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_ID: Service ID
        - USER_ID: User ID
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token

        '''
        logger.debug("users invoked with: ")
        logger.debug("SERVICE_ID=%s" % SERVICE_ID)
        logger.debug("USER_ID=%s" % USER_ID)
        logger.debug("SERVICE_ADMIN_USER=%s" % SERVICE_ADMIN_USER)
        logger.debug("SERVICE_ADMIN_PASSWORD=%s" % SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                         SERVICE_ADMIN_USER,
                                                         SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            DETAIL_USER = self.idm.detailUser(SERVICE_ADMIN_TOKEN,
                                              USER_ID)
            logger.debug("DETAIL_USER=%s" % DETAIL_USER)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("DETAIL_USER=%s" % DETAIL_USER)

        return DETAIL_USER
