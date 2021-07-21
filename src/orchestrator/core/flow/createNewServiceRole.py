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
# along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT team
#
import json

from orchestrator.core.flow.base import FlowBase
from orchestrator.common.util import ContextFilterService


class CreateNewServiceRole(FlowBase):

    def createNewServiceRole(self,
                             SERVICE_ID,
                             SERVICE_NAME,
                             SERVICE_ADMIN_USER,
                             SERVICE_ADMIN_PASSWORD,
                             SERVICE_ADMIN_TOKEN,
                             NEW_ROLE_NAME,
                             XACML_POLICY):

        '''Creates a new role Service (aka domain role keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_ID: Service Id
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin token
        - SERVICE_ADMIN_PASSWORD: Service admin token
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_ROLE_NAME: New role name
        - XACML_POLICY: XACML POLICY for new role
        Return:
        - id: New role Id
        '''
        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "NEW_ROLE_NAME": "%s" % NEW_ROLE_NAME,
            "XACML_POLICY": "%s" % XACML_POLICY
        }
        self.logger.debug("FLOW createNewServiceRole invoked with: %s" % json.dumps(
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
            # 2. Create role
            #
            ID_ROLE = self.idm.createRoleDomain(SERVICE_ADMIN_TOKEN,
                                                SERVICE_ID,
                                                NEW_ROLE_NAME)
            self.logger.debug("ID of user %s: %s" % (NEW_ROLE_NAME, ID_ROLE))

            #
            # 3. Provision policy provided in keypass
            #
            if XACML_POLICY:
                self.logger.debug("set XACML_POLICY %s for role %s" % (XACML_POLICY,
                                                                  ID_ROLE))
                self.ac.provisionPolicyByContent(SERVICE_NAME,
                                                 SERVICE_ADMIN_TOKEN,
                                                 ID_ROLE,
                                                 XACML_POLICY)

            if NEW_ROLE_NAME == 'ServiceCustomer':
                self.logger.debug("set default XACML policies for role %s" % NEW_ROLE_NAME)
                self.ac.provisionPolicy(SERVICE_NAME, SERVICE_ADMIN_TOKEN,
                                        ID_ROLE,
                                        POLICY_FILE_NAME='policy-orion-customer2.xml')
                self.ac.provisionPolicy(SERVICE_NAME, SERVICE_ADMIN_TOKEN,
                                        ID_ROLE,
                                        POLICY_FILE_NAME='policy-perseo-customer2.xml')
                self.ac.provisionPolicy(SERVICE_NAME, SERVICE_ADMIN_TOKEN,
                                        ID_ROLE,
                                        POLICY_FILE_NAME='policy-iotagent-customer2.xml')
                self.ac.provisionPolicy(SERVICE_NAME, SERVICE_ADMIN_TOKEN,
                                        ID_ROLE,
                                        POLICY_FILE_NAME='policy-sth-customer2.xml')
                self.ac.provisionPolicy(SERVICE_NAME, SERVICE_ADMIN_TOKEN,
                                        ID_ROLE,
                                        POLICY_FILE_NAME='policy-keypass-customer2.xml')

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "ID_ROLE": "%s" % ID_ROLE
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {"id": ID_ROLE}, SERVICE_NAME, None
