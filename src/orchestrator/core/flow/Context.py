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


class Context(FlowBase):

    def createEntitySubscribe(self,
                              SERVICE_NAME,
                              SERVICE_ID,
                              SUBSERVICE_NAME,
                              SUBSERVICE_ID,
                              SERVICE_USER_NAME,
                              SERVICE_USER_PASSWORD,
                              SERVICE_USER_TOKEN,
                              ENTITY_TYPE,
                              ENTITY_ID,
                              ATTRIBUTES,
                              REFERENCE_URL
                              ):

        '''Create Context Entity and subscribe to it

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService name
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - ENTITY_TYPE: Orion Entity Type
        - ENTITY_ID: Orion Entity ID
        - ATTRIBUTES: Orion Entity attributes
        - REFERENCE_URL: Orion reference_url
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_NAME": "%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
            "ENTITY_TYPE": "%s" % ENTITY_TYPE,
            "ENTITY_ID": "%s" % ENTITY_ID,
            "ATTRIBUTES": "%s" % ATTRIBUTES,
            "REFERENCE_URL": "%s" % REFERENCE_URL
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

            # Invoke to ContextBroker
            cb_res = self.cb.updateContext(SERVICE_USER_TOKEN,
                                           SERVICE_NAME,
                                           SUBSERVICE_NAME,
                                           ENTITY_TYPE,
                                           ENTITY_ID,
                                           ATTRIBUTES)
            logger.debug("UPDATE_CONTEXT=%s" % json.dumps(cb_res, indent=3))

            ENTITY_PATTERN="true"
            ENTITY_ID=".*"
            DURATION="P50Y"
            NOTIFY_CONDITIONS=[]
            cb_res = self.cb.subscribeContext(SERVICE_USER_TOKEN,
                                              SERVICE_NAME,
                                              SUBSERVICE_NAME,
                                              ENTITY_TYPE,
                                              ENTITY_PATTERN
                                              ENTITY_ID,
                                              REFERENCE_URL,
                                              DURATION
                                              ATTRIBUTES,
                                              NOTIFY_CONDITIONS)
            logger.debug("SUBSCRIBE_CONTEXT=%s" % json.dumps(cb_res, indent=3))

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = cb_res

        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return cb_res
