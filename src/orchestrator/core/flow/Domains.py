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
from orchestrator.core.flow.Roles import Roles
from settings.dev import IOTMODULES

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
        - DOMAIN_NAME: Service name
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
        logger.debug("FLOW domains invoked with: %s" % json.dumps(
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
        - DOMAIN_ID: Service Id
        - DOMAIN_NAME: Service Name
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
        logger.debug("FLOW get_domain invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                if DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD, False)
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
        - DOMAIN_ID: Service Id
        - DOMAIN_NAME: Service Name
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
        logger.debug("FLOW updateDomain invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                # UpdateDomain can be only done by cloud_admin
                ADMIN_TOKEN = self.idm.getToken("admin_domain",
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            if not DOMAIN_ID and DOMAIN_NAME:
                DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                 DOMAIN_NAME,
                                                 False)

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
        - DOMAIN_ID: Service Id
        - DOMAIN_NAME: Service Name
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
        logger.debug("FLOW delete_domain invoked with: %s" % json.dumps(
            data_log,
            indent=3)
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

            # Get all subservices
            projects = self.idm.getDomainProjects(ADMIN_TOKEN, DOMAIN_ID)
            for project in projects['projects']:

                PROJECT_NAME = project['name'].split('/')[1]
                #
                # Delete all devices in subservice
                #
                devices_deleted = self.iota.deleteAllDevices(
                    ADMIN_TOKEN,
                    DOMAIN_NAME,
                    PROJECT_NAME)

                if (len(devices_deleted) > 0):
                    logger.info("devices deleted %s", devices_deleted)

                #
                # Delete all subscriptions in subservice
                #
                subscriptions_deleted = self.cb.deleteAllSubscriptions(
                                                              ADMIN_TOKEN,
                                                              DOMAIN_NAME,
                                                              PROJECT_NAME)
                if (len(subscriptions_deleted) > 0):
                    logger.info("subscriptions deleted %s", subscriptions_deleted)


            #
            # Delete all devices
            #

            devices_deleted = self.iota.deleteAllDevices(ADMIN_TOKEN,
                                                         DOMAIN_NAME)

            #
            # Delete all subscriptions
            #
            # TODO: BUG: admin_domain (cloud_admin) can not delete a subsription in a service!!!!
            subscriptions_deleted = self.cb.deleteAllSubscriptions(
                                                              ADMIN_TOKEN,
                                                              DOMAIN_NAME)
            if (len(subscriptions_deleted) > 0):
                logger.info("subscriptions deleted %s", subscriptions_deleted)


            #
            # Disable Domain
            #
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
        - SERVICE_ID: Service Id
        - SERVICE_NAME: Service Name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role Name
        - ROLE_ID: Role Id
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
        logger.debug("FLOW get_domain_role_policies invoked with: %s" % json.dumps(
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

            # Get Role ID
            if not ROLE_ID and ROLE_NAME:
                if ROLE_NAME == "Admin":
                    SERVICE_ADMIN_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                          SERVICE_ADMIN_USER)
                    # Get KEYSTONE CONF from base idm class
                    roles_flow = Roles(self.idm.KEYSTONE_PROTOCOL,
                                       self.idm.KEYSTONE_HOST,
                                       self.idm.KEYSTONE_PORT)
                    roles = roles_flow.roles_assignments(SERVICE_ID,
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
            if self.idm.isTokenAdmin(SERVICE_ADMIN_TOKEN, SERVICE_ID):

                policies = self.ac.getRolePolicies(SERVICE_NAME,
                                                   SERVICE_ADMIN_TOKEN,
                                                   ROLE_ID)

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

    def activate_module(self,
                        DOMAIN_NAME,
                        DOMAIN_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SERVICE_USER_TOKEN,
                        IOTMODULE):

        '''Activate Module

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - IOTMODULE: IoT Module to activate: STH,  PERSEO
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
            "IOTMODULE": "%s" % IOTMODULE,
        }
        logger.debug("FLOW activate_module invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:

            if not SERVICE_USER_TOKEN:
                if not DOMAIN_ID:
                    SERVICE_USER_TOKEN = self.idm.getToken(
                        DOMAIN_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getToken2(
                        DOMAIN_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            # Ensure DOMAIN_NAME
            DOMAIN_NAME = self.ensure_service_name(SERVICE_USER_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)


            REFERENCE_URL = self.get_endpoint_iot_module(IOTMODULE)

            DURATION="P1Y"

            # Set default ATTRIBUTES for subscription
            ATTRIBUTES = []
            # logger.debug("Trying to getContextTypes...")
            # cb_res = self.cb.getContextTypes(
            #     SERVICE_USER_TOKEN,
            #     DOMAIN_NAME,
            #     "",
            #     None)
            # logger.debug("getContextTypes res=%s" % cb_res)
            # for entity_type in cb_res['types']:
            #     for att in entity_type["attributes"] :
            #         ATTRIBUTES.append(att)

            # Set default ENTITIES for subscription
            ENTITIES = [ {
                "isPattern": "true",
                "id": ".*"
            } ]

            # Set default Notify conditions
            NOTIFY_ATTRIBUTES = []
            NOTIFY_ATTRIBUTES.append("TimeInstant")
            NOTIFY_CONDITIONS = [ {
                "type": "ONCHANGE",
                "condValues": NOTIFY_ATTRIBUTES
            } ]
            logger.debug("Trying to subscribe moduleiot in CB...")
            cb_res = self.cb.subscribeContext(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                "",
                REFERENCE_URL,
                DURATION,
                ENTITIES,
                ATTRIBUTES,
                NOTIFY_CONDITIONS
            )
            logger.debug("subscribeContext res=%s" % cb_res)
            subscriptionid = cb_res['subscribeResponse']['subscriptionId']
            logger.debug("subscription id=%s" % subscriptionid)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "subscriptionid": subscriptionid
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return subscriptionid

    def deactivate_module(self,
                          DOMAIN_NAME,
                          DOMAIN_ID,
                          SERVICE_USER_NAME,
                          SERVICE_USER_PASSWORD,
                          SERVICE_USER_TOKEN,
                          IOTMODULE):

        ''' Deactivate IoT Module

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - IOTMODULE: IoT Module to activate: STH, PERSEO
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
            "IOTMODULE": "%s" % IOTMODULE,
        }
        logger.debug("FLOW deactivate_module invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:

            if not SERVICE_USER_TOKEN:
                if not DOMAIN_ID:
                    SERVICE_USER_TOKEN = self.idm.getToken(
                        DOMAIN_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)
                else:
                    SERVICE_USER_TOKEN = self.idm.getToken2(
                        DOMAIN_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            # Ensure DOMAIN_NAME
            DOMAIN_NAME = self.ensure_service_name(SERVICE_USER_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)

            REFERENCE_URL = self.get_endpoint_iot_module(IOTMODULE)

            logger.debug("Trying to get list subscriptions from CB...")
            cb_res = self.cb.getListSubscriptions(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                ""
            )
            logger.debug("getListSubscriptions res=%s" % cb_res)

            for sub in cb_res:
                subs_url = sub["notification"]["callback"]
                subscriptionid = sub['id']
                if subs_url.startswith(REFERENCE_URL):

                    self.cb.unsubscribeContext(SERVICE_USER_TOKEN,
                                               DOMAIN_NAME,
                                               "",
                                               sub['id'])
                    break

            # logger.debug("subscribeContext res=%s" % cb_res)
            # subscriptionid = cb_res['subscribeResponse']['subscriptionId']
            # logger.debug("subscription id=%s" % subscriptionid)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "subscriptionid": subscriptionid
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return subscriptionid


    def list_activated_modules(self,
                               DOMAIN_NAME,
                               DOMAIN_ID,
                               SERVICE_USER_NAME,
                               SERVICE_USER_PASSWORD,
                               SERVICE_USER_TOKEN):

        '''List Activated IoT Modules

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
        }
        logger.debug("FLOW list_activated_modules invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:

            if not SERVICE_USER_TOKEN:
                if not DOMAIN_ID:
                    SERVICE_USER_TOKEN = self.idm.getToken(
                        DOMAIN_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)
                else:
                    SERVICE_USER_TOKEN = self.idm.getToken2(
                        DOMAIN_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            # Ensure DOMAIN_NAME
            DOMAIN_NAME = self.ensure_service_name(SERVICE_USER_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)

            logger.debug("Trying to get list subscriptions from CB...")
            cb_res = self.cb.getListSubscriptions(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                ""
            )
            logger.debug("getListSubscriptions res=%s" % cb_res)
            modules = []
            for sub in cb_res:
                sub_callback = sub["notification"]["callback"]
                for iotmodule in IOTMODULES:
                    if sub_callback.startswith(self.get_endpoint_iot_module(iotmodule)):
                        if ((len(sub['subject']['entities']) == 1) and
                            (sub['subject']['entities'][0]['idPattern'] == '.*') and
                            (sub['subject']['entities'][0]['type'] == '')):
                            modules.append({ "name": iotmodule,
                                             "subscriptionid": sub['id'],
                                             "alias": self.get_alias_iot_module(iotmodule)
                                             })
                            break

            logger.debug("modules=%s" % modules)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "modules": modules
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return modules
