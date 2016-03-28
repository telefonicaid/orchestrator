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
import logging
import json

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class RemoveUser(FlowBase):

    def removeUser(self,
                   SERVICE_NAME,
                   SERVICE_ID,
                   SERVICE_ADMIN_USER,
                   SERVICE_ADMIN_PASSWORD,
                   SERVICE_ADMIN_TOKEN,
                   USER_NAME,
                   USER_ID):

        '''Removes an user Service (aka domain user keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - USER_NAME: User name
        - USER_ID: User id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "USER_NAME": "%s" % USER_NAME,
            "USER_ID": "%s" % USER_ID
        }
        logger.debug("FLOW projects invoked with: %s" % json.dumps(
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
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 2. Get user ID
            #
            if not USER_ID:
                USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   USER_NAME)
            logger.debug("ID of user %s: %s" % (USER_NAME, USER_ID))

            # TODO: disable us before remove it ?

            #
            # 3. Remove user ID
            #
            self.idm.removeUser(SERVICE_ADMIN_TOKEN,
                                USER_ID)
            # logger.debug("ID of user %s: %s" % (USER_NAME, ID_USER))

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "USER_ID": USER_ID
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {}
