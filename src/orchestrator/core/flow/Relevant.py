#
# Copyright 2019 Telefonica Espana
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
from orchestrator.common.util import ContextFilterSubService

class Relevant(FlowBase):

    def getRelevant(self,
                    SERVICE_ID,
                    SERVICE_NAME,
                    SUBSERVICE_ID,
                    SUBSERVICE_NAME,
                    USER_NAME,
                    USER_PASSWORD,
                    USER_TOKEN,
                    COMPONENT,
                    LOG_LEVEL,
                    CORRELATOR_ID,
                    TRANSACTION_ID,
                    CUSTOM_TEXT):

        '''Get something relevant of a domain.

        In case of HTTP error, return HTTP error

        Params:
            SERVICE_ID
            SUBSERVICE_ID
            USER_NAME
            USER_PASSWORD
            USER_TOKEN
            COMPONENT
            LOG_LEVEL
            CORRELATOR_ID
            TRANSACTION_ID
            CUSTOM_TEXT
        Return:

        '''
        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % USER_PASSWORD,
            "USER_TOKEN": self.get_extended_token(USER_TOKEN),
            "COMPONENT": COMPONENT,
            "LOG_LEVEL": LOG_LEVEL,
            "CORRELATOR_ID": CORRELATOR_ID,
            "TRANSACTION_ID": TRANSACTION_ID,
            "CUSTOM_TEXT": CUSTOM_TEXT
        }
        SERVICE_NAME = None
        SUBSERVICE_NAME = None
        self.logger.debug("FLOW projects invoked with: %s" % json.dumps(
            data_log, indent=3)
        )
        try:
            if not USER_TOKEN:
                if not SERVICE_ID:
                    USER_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                   USER_NAME,
                                                   USER_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(USER_TOKEN,
                                                      SERVICE_NAME)

                else:
                    USER_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                    USER_NAME,
                                                    USER_PASSWORD)
            self.logger.debug("USER_TOKEN=%s" % USER_TOKEN)

            # Ensure SERVICE_NAME and SUBSERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(USER_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))

            if SUBSERVICE_ID and not SUBSERVICE_NAME:
                SUBSERVICE_NAME = self.ensure_subservice_name(USER_TOKEN,
                                                              SERVICE_ID,
                                                              SUBSERVICE_ID,
                                                              None)
            if SUBSERVICE_NAME:
                self.logger.addFilter(ContextFilterSubService(SUBSERVICE_NAME))

            if self.idm.isTokenAdmin(USER_TOKEN, SERVICE_ID):
                self.logger.info("USER_TOKEN is token admin")
                OUTPUT = self.splunk.searchRelevant(SERVICE_NAME,
                                                    SUBSERVICE_NAME,
                                                    COMPONENT,
                                                    LOG_LEVEL,
                                                    CORRELATOR_ID,
                                                    TRANSACTION_ID,
                                                    CUSTOM_TEXT)
            else:
                self.logger.warn("USER_TOKEN is not token admin")
                raise Exception("Token is not a admin token")

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        # format OUTPUT
        #OUTPUT is a { { "preview":false, "offset":137, "result": {} } } ?

        data_log = {
            "OUTPUT": OUTPUT
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate operations metrics into flow metrics
        self.collectComponentMetrics()

        return OUTPUT, SERVICE_NAME, SUBSERVICE_NAME
