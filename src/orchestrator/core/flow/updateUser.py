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

class UpdateUser(FlowBase):

    def updateUser(self,
                   SERVICE_NAME,
                   SERVICE_ID,
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
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - USER_NAME: User name
        - USER_ID: User Id
        - USER_DATA_VALUE: user data value in json
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "USER_NAME": "%s" % USER_NAME,
            "USER_ID": "%s" % USER_ID,
            "USER_DATA_VALUE": "%s" % USER_DATA_VALUE
        }
        self.logger.debug("FLOW updateUser invoked with: %s" % json.dumps(
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

            #
            # 2. Get user ID
            #
            if not USER_ID:
                USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   USER_NAME)
            self.logger.debug("ID of user %s: %s" % (USER_NAME, USER_ID))

            #
            # 3. Updateuser
            #
            self.idm.updateUser(SERVICE_ADMIN_TOKEN,
                                USER_ID,
                                USER_DATA_VALUE)

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "USER_ID": USER_ID,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": USER_ID}, SERVICE_NAME


    def changeUserPassword(self,
                           SERVICE_NAME,
                           SERVICE_ID,
                           USER_ID,
                           SERVICE_USER_NAME,
                           SERVICE_USER_PASSWORD,
                           SERVICE_USER_TOKEN,
                           NEW_USER_PASSWORD):

        '''Change user password.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - USER_ID: user id
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - NEW_USER_PASSWORD: new user password
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "USER_ID": "%s" % USER_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": self.get_extended_token(SERVICE_USER_TOKEN),
            "NEW_USER_PASSWORD": "%s" % NEW_USER_PASSWORD
        }
        self.logger.debug("FLOW change password invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_USER_TOKEN:
                if not SERVICE_ID:
                    SERVICE_USER_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SCOPED=False)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                      SERVICE_NAME,
                                                      SCOPED=False)
                else:
                    SERVICE_USER_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SCOPED=False)
            self.logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)

            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_USER_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)
            #
            # 2. Get user ID
            #
            if not USER_ID and SERVICE_USER_NAME:
                USER_ID = self.idm.getUserId(SERVICE_USER_TOKEN,
                                             SERVICE_USER_NAME)
                self.logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, USER_ID))

            #
            # 3. ChangeUserPassword
            #
            self.idm.changeUserPassword(SERVICE_USER_TOKEN,
                                        USER_ID,
                                        SERVICE_USER_PASSWORD,
                                        NEW_USER_PASSWORD)

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "USER_ID": USER_ID,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": USER_ID}, SERVICE_NAME
