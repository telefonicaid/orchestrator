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


class Domains(FlowBase):

    def domains(self,
                DOMAIN_NAME,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Domains.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - array list of domains
        '''
        data_log = {
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN
        }
        logger.debug("domains invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            DOMAINS = self.idm.getDomains(ADMIN_TOKEN)

            logger.debug("DOMAINS=%s" % json.dumps(DOMAINS, indent=3))

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAINS": DOMAINS
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))
        return DOMAINS

    def get_domain(self,
                   DOMAIN_ID,
                   DOMAIN_NAME,
                   ADMIN_USER,
                   ADMIN_PASSWORD,
                   ADMIN_TOKEN):
        '''Get Domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - domain detail
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN
        }
        logger.debug("get_domain invoked with: %s" % json.dumps(data_log,
                                                                indent=3))
        try:
            if not ADMIN_TOKEN:
                if DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
                else:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)

            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            DOMAIN = self.idm.getDomain(ADMIN_TOKEN, DOMAIN_ID)

            logger.debug("DOMAIN=%s" % DOMAIN)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAIN": DOMAIN
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))
        return DOMAIN

    def update_domain(self,
                      DOMAIN_ID,
                      DOMAIN_NAME,
                      ADMIN_USER,
                      ADMIN_PASSWORD,
                      ADMIN_TOKEN,
                      NEW_SERVICE_DESCRIPTION):

        '''Update Domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_SERVICE_DESCRIPTION: New service description
        Return:
        - domain detail
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN,
            "NEW_SERVICE_DESCRIPTION": "%s" % NEW_SERVICE_DESCRIPTION,
        }
        logger.debug("updateDomain invoked with: %s" % json.dumps(data_log,
                                                                  indent=3))

        try:
            if not ADMIN_TOKEN:
                # UpdateDomain can be only done by cloud_admin
                ADMIN_TOKEN = self.idm.getToken("admin_domain",
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            if not DOMAIN_ID:
                DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                 DOMAIN_NAME)

            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)
            DOMAIN = self.idm.updateDomain(ADMIN_TOKEN,
                                           DOMAIN_ID,
                                           NEW_SERVICE_DESCRIPTION)

            logger.debug("DOMAIN=%s" % DOMAIN)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAIN": DOMAIN
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DOMAIN

    def delete_domain(self,
                      DOMAIN_ID,
                      DOMAIN_NAME,
                      ADMIN_USER,
                      ADMIN_PASSWORD,
                      ADMIN_TOKEN):

        '''Delete a Domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - domain detail
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN
        }
        logger.debug("delete_domain invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken("admin_domain",
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)

            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)
            # Another way:
            # if not DOMAIN_ID:
            #     DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
            #                                      DOMAIN_NAME)

            if not DOMAIN_ID:
                DOMAINS = self.idm.getDomains(ADMIN_TOKEN)
                for domain in DOMAINS['domains']:
                    if domain['name'] == DOMAIN_NAME:
                        DOMAIN_ID = domain['id']
                        break

            if not DOMAIN_NAME:
                DOMAIN = self.idm.getDomain(ADMIN_TOKEN, DOMAIN_ID)
                DOMAIN_NAME = DOMAIN['domain']['name']

            DOMAIN = self.idm.disableDomain(ADMIN_TOKEN, DOMAIN_ID)

            self.idm.deleteDomain(ADMIN_TOKEN, DOMAIN_ID)

            # Delete policy of roles in Access Control
            self.ac.deleteTenantPolicies(DOMAIN_NAME, ADMIN_TOKEN)

            logger.debug("DOMAIN=%s" % DOMAIN)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAIN": DOMAIN
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))
        return DOMAIN


    def getDomainRolePolicies(self,
                              SERVICE_ID,
                              SERVICE_NAME,
                              SERVICE_ADMIN_USER,
                              SERVICE_ADMIN_PASSWORD,
                              SERVICE_ADMIN_TOKEN,
                              ROLE_NAME,
                              ROLE_ID):

        '''Get domain role policies

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_ID:
        - SERVICE_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME
        - ROLE_ID
        Return:
        - XACML policies
        '''
        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": "%s" % SERVICE_ADMIN_TOKEN,
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
        }
        logger.debug("get_domain_role_policies invoked with: %s" % json.dumps(
            data_log, indent=3)
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

            # Get Role ID
            if not ROLE_ID and ROLE_NAME:
                if ROLE_NAME == "Admin":
                    SERVICE_ADMIN_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                          SERVICE_ADMIN_USER)
                    roles = self.roles_assignments(SERVICE_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_TOKEN,
                                                   True)
                    for role in roles['role_assignments']:
                        if role['role']['name'] == 'admin':
                            ROLE_ID=role['role']['id']
                            break
                else:
                    ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                       SERVICE_ID,
                                                       ROLE_NAME)
            logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            # Get policies in Access Control
            policies = self.ac.getRolePolicies(SERVICE_NAME, SERVICE_ADMIN_TOKEN, ROLE_ID)

            logger.debug("POLICIES=%s" % policies)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "POLICIES": policies
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))
        return policies
