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


class Devices(FlowBase):

    def register(self,
                 SERVICE_NAME,
                 SERVICE_ID,
                 SUBSERVICE_NAME,
                 SUBSERVICE_ID,
                 SERVICE_USER_NAME,
                 SERVICE_USER_PASSWORD,
                 SERVICE_USER_TOKEN,
                 DEVICE_ID,
                 PROTOCOL
                ):

        '''Register Device.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService name
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token

        '''

        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_NAME": "%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
        }
        logger.debug("users invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not SERVICE_USER_TOKEN:
                if not SERVICE_ID:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken(
                        SERVICE_NAME,
                        SUBSERVICE_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                      SERVICE_NAME)

                    SUBSERVICE_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                          SERVICE_NAME,
                                                          SUBSERVICE_NAME)
                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(
                        SERVICE_ID,
                        SUBSERVICE_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)

            # Check that protocol exists in IOTA ?

            # call IOTA
            self.iota.registerDevice(SERVICE_USER_TOKEN,
                                     SERVICE_NAME,
                                     SUBSERVICE_NAME,
                                     DEVICE_ID,
                                     PROTOCOL)



        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {

        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DEVICE_ID
