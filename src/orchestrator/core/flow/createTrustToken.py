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
from settings.common import IOTAGENT, PEP


class CreateTrustToken(FlowBase):

    def createTrustToken(self,
                         SERVICE_NAME,
                         SERVICE_ID,
                         SUBSERVICE_NAME,
                         SUBSERVICE_ID,
                         SERVICE_ADMIN_USER,
                         SERVICE_ADMIN_PASSWORD,
                         SERVICE_ADMIN_TOKEN,
                         ROLE_NAME,
                         ROLE_ID,
                         TRUSTEE_USER_NAME,
                         TRUSTEE_USER_ID,
                         TRUSTOR_USER_NAME,
                         TRUSTOR_USER_ID):
        '''Creates a trust token

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService Id
        - SERVICE_ADMIN_USER: Service admin token
        - SERVICE_ADMIN_PASSWORD: Service admin token
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role name
        - TRUSTEE_USER_NAME:
        - TRUSTEE_USER_ID:
        - TRUSTOR_USER_NAME:
        - TRUSTOR_USER_ID:
        Return:
        - token: Trust Token
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_NAME": "%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "TRUSTEE_USER_NAME": "%s" % TRUSTEE_USER_NAME,
            "TRUSTEE_USER_ID": "%s" % TRUSTEE_USER_ID,
            "TRUSTOR_USER_NAME": "%s" % TRUSTOR_USER_NAME,
            "TRUSTOR_USER_ID": "%s" % TRUSTOR_USER_ID,
        }
        self.logger.debug("FLOW createTrustToken invoked with: %s" % json.dumps(
            data_log, indent=3)
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
            if not SERVICE_ID and SERVICE_NAME:
                SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                  SERVICE_NAME)
                self.logger.debug("ID of your service %s" % SERVICE_ID)

            if not SERVICE_NAME:
                SERVICE = self.idm.getDomain(SERVICE_ADMIN_TOKEN, SERVICE_ID)
                SERVICE_NAME = SERVICE['domain']['name']
                self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                           SERVICE_ID))

            #
            # 2. Get SubService (aka project)
            #
            if not SUBSERVICE_ID and SUBSERVICE_NAME:
                SUBSERVICE_ID = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)
                self.logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME,
                                                              SUBSERVICE_ID))

            #
            # 3. Get role
            #
            if not ROLE_ID and ROLE_NAME:
                if SERVICE_ADMIN_USER and SERVICE_ADMIN_USER == TRUSTOR_USER_NAME:
                    ROLE_ID = self.idm.getUserRoleId(SERVICE_ADMIN_TOKEN,
                                                     SERVICE_ID,
                                                     SUBSERVICE_ID,
                                                     ROLE_NAME)
                else:
                    ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                       SERVICE_ID,
                                                       ROLE_NAME)

                self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 4. Get Trustee User
            #
            if not TRUSTEE_USER_ID and TRUSTEE_USER_NAME:
                # We are asuming that trustee belong to SERVICE!!
                if TRUSTEE_USER_NAME == "iotagent":
                    IOTAGENT_TOKEN = self.idm.getToken('default',
                                                  IOTAGENT['user'],
                                                  IOTAGENT['password'],
                                                  False)
                    TRUSTEE_USER_ID = self.idm.getUserId(IOTAGENT_TOKEN,
                                                        TRUSTEE_USER_NAME)
                else:
                    TRUSTEE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                               SERVICE_ID,
                                                               TRUSTEE_USER_NAME)
                self.logger.debug("ID of trustee user %s: %s" % (TRUSTEE_USER_NAME,
                                                            TRUSTEE_USER_ID))

            #
            # 5. Get Trustor User
            #
            if not TRUSTOR_USER_ID and TRUSTOR_USER_NAME:
                if SERVICE_ADMIN_USER and SERVICE_ADMIN_USER == TRUSTOR_USER_NAME:
                    TRUSTOR_USER_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                         TRUSTOR_USER_NAME)
                else:
                    TRUSTOR_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                               SERVICE_ID,
                                                               TRUSTOR_USER_NAME)
                self.logger.debug("ID of trustor user %s: %s" % (TRUSTOR_USER_NAME,
                                                            TRUSTOR_USER_ID))

            #
            # 6. Create trust
            #
            ID_TRUST = self.idm.createTrustToken(SERVICE_ADMIN_TOKEN,
                                                 SUBSERVICE_ID,
                                                 ROLE_ID,
                                                 TRUSTEE_USER_ID,
                                                 TRUSTOR_USER_ID)

            self.logger.debug("ID of Trust %s" % (ID_TRUST))

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ID_TRUST": "%s" % ID_TRUST
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": ID_TRUST}



    def getTrustsUserTrustee(self,
                             SERVICE_NAME,
                             SERVICE_ID,
                             SERVICE_ADMIN_USER,
                             SERVICE_ADMIN_PASSWORD,
                             SERVICE_ADMIN_TOKEN,
                             TRUSTEE_USER_NAME,
                             TRUSTEE_USER_ID):
        '''Lists all trust of a trustee user

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin token
        - SERVICE_ADMIN_PASSWORD: Service admin token
        - SERVICE_ADMIN_TOKEN: Service admin token
        - TRUSTEE_USER_NAME:
        - TRUSTEE_USER_ID:
        Return:
        - trusts
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "TRUSTEE_USER_NAME": "%s" % TRUSTEE_USER_NAME,
            "TRUSTEE_USER_ID": "%s" % TRUSTEE_USER_ID,
        }
        self.logger.debug("FLOW getTrustsUserTrustee invoked with: %s" % json.dumps(
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

            #
            # 2. Get Trustee User
            #
            if not TRUSTEE_USER_ID:
                # We are asuming that trustee belong to SERVICE!!
                if TRUSTEE_USER_NAME == "iotagent":
                    PEP_TOKEN = self.idm.getToken('admin_domain',
                                                  PEP['user'],
                                                  PEP['password'],
                                                  False)
                    TRUSTEE_USER_ID = self.idm.getUserId(PEP_TOKEN,
                                                         'iotagent')
                else:
                    TRUSTEE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                               SERVICE_ID,
                                                               TRUSTEE_USER_NAME)
            self.logger.debug("ID of trustee user %s: %s" % (TRUSTEE_USER_NAME,
                                                        TRUSTEE_USER_ID))

            #
            # 3. Get trusts
            #
            TRUSTS = self.idm.getTrustsTrustee(SERVICE_ADMIN_TOKEN,
                                               TRUSTEE_USER_ID)

            self.logger.debug("Trusts %s" % (TRUSTS))

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "TRUSTS": "%s" % TRUSTS
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return TRUSTS
