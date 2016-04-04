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

class CreateNewServiceUser(FlowBase):

    def createNewServiceUser(self,
                             SERVICE_NAME,
                             SERVICE_ID,
                             SERVICE_ADMIN_USER,
                             SERVICE_ADMIN_PASSWORD,
                             SERVICE_ADMIN_TOKEN,
                             NEW_USER_NAME,
                             NEW_USER_PASSWORD,
                             NEW_USER_EMAIL,
                             NEW_USER_DESCRIPTION):
        '''Creates a new user Service (aka domain user keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_USER_NAME: New user name (required)
        - NEW_USER_PASSWORD: New user password (required)
        - NEW_USER_EMAIL: New user email (optional)
        - NEW_USER_DESCRIPTION: New user description (optional)
        Return:
        - id: New user Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "NEW_USER_NAME": "%s" % NEW_USER_NAME,
            "NEW_USER_PASSWORD": "%s" % NEW_USER_PASSWORD,
            "NEW_USER_EMAIL": "%s" % NEW_USER_EMAIL,
            "NEW_USER_DESCRIPTION": "%s" % NEW_USER_DESCRIPTION
        }
        self.logger.debug("FLOW createNewServiceUser invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            if not SERVICE_ID:
                SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                  SERVICE_NAME)

            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                       SERVICE_ID))

            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            #
            # 2.  Create user
            #
            ID_USER = self.idm.createUserDomain(SERVICE_ADMIN_TOKEN,
                                                SERVICE_ID,
                                                SERVICE_NAME,
                                                NEW_USER_NAME,
                                                NEW_USER_PASSWORD,
                                                NEW_USER_EMAIL,
                                                NEW_USER_DESCRIPTION)
            self.logger.debug("ID of user %s: %s" % (NEW_USER_NAME, ID_USER))

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "ID_USER": "%s" % ID_USER,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": ID_USER}
