#
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of IoT orchestrator
#
# IoT orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# IoT orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with IoT orchestrator. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT team
#
import json

from orchestrator.core.flow.base import FlowBase
from orchestrator.common.util import ContextFilterService

class Users(FlowBase):

    def users(self,
              SERVICE_NAME,
              SERVICE_ID,
              SERVICE_ADMIN_USER,
              SERVICE_ADMIN_PASSWORD,
              SERVICE_ADMIN_TOKEN,
              START_INDEX=None,
              COUNT=None):

        '''Get users.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - START_INDEX: where pagination start
        - COUNT: number of results
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "START_INDEX": "%s" % START_INDEX,
            "COUNT": "%s" % COUNT,
        }
        self.logger.debug("FLOW users invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            # SERVICE_ROLES = self.idm.getDomainRoles(SERVICE_ADMIN_TOKEN,
            #                                         SERVICE_ID)

            # self.logger.debug("SERVICE_ROLES=%s" %  json.dumps(SERVICE_ROLES,
            #                                               indent=3))

            SERVICE_USERS = self.idm.getDomainUsers(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    START_INDEX,
                                                    COUNT)

            self.logger.debug("SERVICE_USERS=%s" % json.dumps(SERVICE_USERS,
                                                         indent=3))

            # Get Roles de SubServicio

            # Listar los usuarios de un Servicio
            # Obtener roles de usuario

            # Listar los usuarios de un Subservicio

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SERVICE_USERS": SERVICE_USERS,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return SERVICE_USERS, SERVICE_NAME, None


    def user(self,
             SERVICE_ID,
             SERVICE_NAME,
             USER_ID,
             SERVICE_ADMIN_USER,
             SERVICE_ADMIN_PASSWORD,
             SERVICE_ADMIN_TOKEN):

        '''Get user detail

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_ID: Service ID
        - SERVICE_NAME: Service NAME
        - USER_ID: User ID
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token

        '''
        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "USER_ID": "%s" % USER_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
        }
        self.logger.debug("FLOW user invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                    SERVICE_ID,
                    SERVICE_ADMIN_USER,
                    SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            DETAIL_USER = self.idm.detailUser(SERVICE_ADMIN_TOKEN,
                                              USER_ID)
            self.logger.debug("DETAIL_USER=%s" % json.dumps(DETAIL_USER, indent=3))

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "DETAIL_USER": DETAIL_USER,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return DETAIL_USER, SERVICE_NAME, None
