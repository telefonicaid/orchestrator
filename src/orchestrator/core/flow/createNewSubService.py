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


class CreateNewSubService(FlowBase):

    def createNewSubService(self,
                            SERVICE_NAME,
                            SERVICE_ID,
                            SERVICE_ADMIN_USER,
                            SERVICE_ADMIN_PASSWORD,
                            SERVICE_ADMIN_TOKEN,
                            NEW_SUBSERVICE_NAME,
                            NEW_SUBSERVICE_DESCRIPTION,
                            NEW_SUBSERVICE_ADMIN_USER=None,
                            NEW_SUBSERVICE_ADMIN_PASSWORD=None,
                            NEW_SUBSERVICE_ADMIN_EMAIL=None):

        '''Creates a new SubService (aka project keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_SUBSERVICE_NAME: New subservice name (required)
        - NEW_SUBSERVICE_DESCRIPTION: New subservice description
        - NEW_SUBSERVICE_ADMIN_USER: New subservice admin username
        - NEW_SUBSERVICE_ADMIN_PASSWORD: New subservice admin password
        - NEW_SUBSERVICE_ADMIN_EMAIL: New subservice admin email (optional)
        Return:
        - ID: New subservice id
        '''

        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": "%s" % SERVICE_ADMIN_TOKEN,
            "NEW_SUBSERVICE_NAME": "%s" % NEW_SUBSERVICE_NAME,
            "NEW_SUBSERVICE_DESCRIPTION": "%s" % NEW_SUBSERVICE_DESCRIPTION,
            "NEW_SUBSERVICE_ADMIN_USER": "%s" % NEW_SUBSERVICE_ADMIN_USER,
            "NEW_SUBSERVICE_ADMIN_PASSWORD": "%s" % NEW_SUBSERVICE_ADMIN_PASSWORD,
            "NEW_SUBSERVICE_ADMIN_EMAIL": "%s" % NEW_SUBSERVICE_ADMIN_EMAIL
        }
        logger.debug("FLOW createNewSubService invoked with: %s" % json.dumps(
            data_log, indent=3)
        )
        ID_PRO1=None
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            if not SERVICE_ID:
                SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                  SERVICE_NAME)

            logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                       SERVICE_ID))

            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            #
            # 2.  Create subservice (aka project)
            #
            ID_PRO1 = self.idm.createProject(SERVICE_ADMIN_TOKEN,
                                             SERVICE_ID,
                                             NEW_SUBSERVICE_NAME,
                                             NEW_SUBSERVICE_DESCRIPTION)
            logger.debug("ID of new subservice %s: %s" % (NEW_SUBSERVICE_NAME,
                                                          ID_PRO1))


            #
            # 3. Create SubService Admin user (optional)
            #
            if NEW_SUBSERVICE_ADMIN_USER and NEW_SUBSERVICE_ADMIN_PASSWORD:
                try:
                    ID_USER = self.idm.createUserDomain(
                        SERVICE_ADMIN_TOKEN,
                        SERVICE_ID,
                        SERVICE_NAME,
                        NEW_SUBSERVICE_ADMIN_USER,
                        NEW_SUBSERVICE_ADMIN_PASSWORD,
                        NEW_SUBSERVICE_ADMIN_EMAIL,
                        None)
                except Exception, ex:
                    logger.warn("ERROR creating user %s: %s" % (
                        NEW_SERVICE_ADMIN_USER,
                        ex))
                    logger.info("Removing uncomplete created project %s" % ID_PRO1)
                    self.idm.disableProject(SERVICE_ADMIN_TOKEN, SERVICE_ID, ID_PRO1)
                    self.idm.deleteProject(SERVICE_ADMIN_TOKEN, ID_PRO1)
                    return self.composeErrorCode(ex)

                logger.debug("ID of user %s: %s" % (NEW_SUBSERVICE_ADMIN_USER,
                                                    ID_USER))

                ROLE_NAME = 'SubServiceAdmin'
                ID_ROLE = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
                logger.debug("ID of role  %s: %s" % (ROLE_NAME,
                                                     ID_ROLE))

                self.idm.grantProjectRole(SERVICE_ADMIN_TOKEN,
                                          ID_PRO1,
                                          ID_USER,
                                          ID_ROLE)

        except Exception, ex:
            if ID_PRO1:
                logger.info("removing uncomplete created project %s" % ID_PRO1)
                self.idm.disableProject(SERVICE_ADMIN_TOKEN, SERVICE_ID, ID_PRO1)
                self.idm.deleteProject(SERVICE_ADMIN_TOKEN, ID_PRO1)
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "ID_PRO1": "%s" % ID_PRO1,
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": ID_PRO1}
