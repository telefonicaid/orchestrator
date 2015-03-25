import logging
import json

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class Users(FlowBase):

    def users(self,
              SERVICE_ID,
              SERVICE_ADMIN_USER,
              SERVICE_ADMIN_PASSWORD,
              SERVICE_ADMIN_TOKEN,
              START_INDEX=None,
              COUNT=None):

        '''Get users.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - START_INDEX: where pagination start
        - COUNT: number of results
        '''
        data_log = {
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN,
            "START_INDEX":"%s" % START_INDEX,
            "COUNT":"%s" % COUNT,
        }
        logger.debug("users invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                         SERVICE_ADMIN_USER,
                                                         SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)



            # SERVICE_ROLES = self.idm.getDomainRoles(SERVICE_ADMIN_TOKEN,
            #                                         SERVICE_ID)

            # logger.debug("SERVICE_ROLES=%s" %  json.dumps(SERVICE_ROLES, indent=3))

            SERVICE_USERS = self.idm.getDomainUsers(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID)

            logger.debug("SERVICE_USERS=%s" % json.dumps(SERVICE_USERS, indent=3))


            # Get Roles de SubServicio

            # Listar los usuarios de un Servicio
              # Obtener roles de usuario

            # Listar los usuarios de un Subservicio


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "SERVICE_USERS": SERVICE_USERS,
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
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
        data_log = {
            "SERVICE_ID":"%s" % SERVICE_ID,
            "USER_ID":"%s" % USER_ID,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN
        }
        logger.debug("user invoked with: %s" % json.dumps(data_log, indent=3))
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                         SERVICE_ADMIN_USER,
                                                         SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            DETAIL_USER = self.idm.detailUser(SERVICE_ADMIN_TOKEN,
                                              USER_ID)
            logger.debug("DETAIL_USER=%s" % json.dumps(DETAIL_USER, indent=3))


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DETAIL_USER": DETAIL_USER,
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DETAIL_USER
