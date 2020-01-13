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
from orchestrator.common.util import CSVOperations
from orchestrator.common.util import ContextFilterService
from orchestrator.common.util import ContextFilterSubService
from settings.dev import IOTMODULES


class Projects(FlowBase):

    def projects(self,
                 DOMAIN_ID,
                 DOMAIN_NAME,
                 ADMIN_USER,
                 ADMIN_PASSWORD,
                 ADMIN_TOKEN):

        '''Get Projects of a domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - project array list
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % "***", #ADMIN_PASSWORD,
            "ADMIN_TOKEN": self.get_extended_token(ADMIN_TOKEN)
        }
        self.logger.debug("FLOW projects invoked with: %s" % json.dumps(
            data_log, indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                if not DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)

                else:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
            self.logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            # Ensure DOMAIN_NAME and PROJECT_NAME
            DOMAIN_NAME = self.ensure_service_name(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))

            PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
                                                  DOMAIN_ID)

            self.logger.debug("PROJECTS=%s" % json.dumps(PROJECTS, indent=3))

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "PROJECTS": PROJECTS
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return PROJECTS, DOMAIN_NAME, None

    def get_project(self,
                    DOMAIN_ID,
                    DOMAIN_NAME,
                    PROJECT_ID,
                    ADMIN_USER,
                    ADMIN_PASSWORD,
                    ADMIN_TOKEN):

        '''Ge Project detail of a domain

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - PROJECT_ID: id of project
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - project detail
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % "***", #ADMIN_PASSWORD,
            "ADMIN_TOKEN": self.get_extended_token(ADMIN_TOKEN)
        }
        self.logger.debug("FLOW get_project invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                 ADMIN_USER,
                                                 ADMIN_PASSWORD)
            self.logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            # Ensure DOMAIN_NAME and PROJECT_NAME
            DOMAIN_NAME = self.ensure_service_name(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))

            PROJECT_NAME = self.ensure_subservice_name(ADMIN_TOKEN,
                                                       DOMAIN_ID,
                                                       PROJECT_ID,
                                                       None)
            self.logger.addFilter(ContextFilterSubService(PROJECT_NAME))

            # PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
            #                                       DOMAIN_ID)
            # for project in PROJECTS:
            #     if project['id'] == PROJECT_ID:
            #         PROJECT = project

            try:
                PROJECT = self.idm.getProject(ADMIN_TOKEN, PROJECT_ID)
            except Exception, ex:
                PROJECT = {
                    'project': {
                        'description': PROJECT_NAME,
                        'domain_id': DOMAIN_ID,
                        'id': PROJECT_ID,
                        'name': '/' + PROJECT_NAME
                    }
                }
                if PROJECT_NAME.startswith('#'):
                    PROJECT['project']['name']=PROJECT_NAME
            self.logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "PROJECT": PROJECT
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return PROJECT, DOMAIN_NAME, PROJECT_NAME

    def update_project(self,
                       DOMAIN_ID,
                       DOMAIN_NAME,
                       PROJECT_ID,
                       PROJECT_NAME,
                       ADMIN_USER,
                       ADMIN_PASSWORD,
                       ADMIN_TOKEN,
                       NEW_SUBSERVICE_DESCRIPTION):

        '''Update Project detail of a domain

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - PROJECT_ID: id of project
        - PROJECT_NAME: name of project
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_SUBSERVICE_DESCRIPTION: New subservice description
        Return:
        - project detail
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % "***", #ADMIN_PASSWORD,
            "ADMIN_TOKEN": self.get_extended_token(ADMIN_TOKEN),
            "NEW_SUBSERVICE_DESCRIPTION": "%s" % NEW_SUBSERVICE_DESCRIPTION,
        }
        self.logger.debug("FLOW update_project invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                if not DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)
                else:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
            self.logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            # Ensure DOMAIN_NAME and PROJECT_NAME
            DOMAIN_NAME = self.ensure_service_name(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))

            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(ADMIN_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)
            PROJECT_NAME = self.ensure_subservice_name(ADMIN_TOKEN,
                                                       DOMAIN_ID,
                                                       PROJECT_ID,
                                                       PROJECT_NAME)
            self.logger.addFilter(ContextFilterSubService(PROJECT_NAME))

            PROJECT = self.idm.updateProject(ADMIN_TOKEN,
                                             DOMAIN_ID,
                                             PROJECT_ID,
                                             NEW_SUBSERVICE_DESCRIPTION)

            self.logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "PROJECT": PROJECT
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return PROJECT, DOMAIN_NAME, PROJECT_NAME

    def delete_project(self,
                       DOMAIN_ID,
                       DOMAIN_NAME,
                       PROJECT_ID,
                       PROJECT_NAME,
                       ADMIN_USER,
                       ADMIN_PASSWORD,
                       ADMIN_TOKEN):

        '''Delete Project of domain

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - PROJECT_ID: id of project
        - PROJECT_NAME: name of project
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % "***", #ADMIN_PASSWORD,
            "ADMIN_TOKEN": self.get_extended_token(ADMIN_TOKEN)
        }
        self.logger.debug("FLOW get_project invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:

            if not ADMIN_TOKEN:
                if not DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)
                else:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)

            # Ensure DOMAIN_NAME and PROJECT_NAME
            DOMAIN_NAME = self.ensure_service_name(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))

            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(ADMIN_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            PROJECT_NAME = self.ensure_subservice_name(ADMIN_TOKEN,
                                                       DOMAIN_ID,
                                                       PROJECT_ID,
                                                       PROJECT_NAME)
            self.logger.addFilter(ContextFilterSubService(PROJECT_NAME))

            self.logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            self.logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            self.logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            #
            # Delete all subscriptions
            #
            subscriptions_deleted = self.cb.deleteAllSubscriptions(
                                                              ADMIN_TOKEN,
                                                              DOMAIN_NAME,
                                                              PROJECT_NAME)
            if (len(subscriptions_deleted) > 0):
                self.logger.info("subscriptions deleted %s",
                                 subscriptions_deleted)

            #
            # Delete all rules in a subservice
            #
            rules_deleted = self.perseo.deleteAllRules(ADMIN_TOKEN,
                                                       DOMAIN_NAME,
                                                       PROJECT_NAME)
            if (len(rules_deleted) > 0):
                self.logger.info("rules deleted %s",
                                 rules_deleted)

            PROJECT = self.idm.disableProject(ADMIN_TOKEN,
                                              DOMAIN_ID,
                                              PROJECT_ID)

            self.idm.deleteProject(ADMIN_TOKEN,
                                   PROJECT_ID)

            self.logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "PROJECT": PROJECT
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return PROJECT, DOMAIN_NAME, PROJECT_NAME


    def activate_module(self,
                        DOMAIN_NAME,
                        DOMAIN_ID,
                        PROJECT_NAME,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SERVICE_USER_TOKEN,
                        IOTMODULE):

        '''Activate Module

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - PROJECT_ID: id of project
        - PROJECT_NAME: name of project
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - IOTMODULE: IoT Module to activate: STH, PERSEO
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % "***", #SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": self.get_extended_token(SERVICE_USER_TOKEN),
            "IOTMODULE": "%s" % IOTMODULE,
        }
        self.logger.debug("FLOW activate_module invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:

            if not SERVICE_USER_TOKEN:
                if not DOMAIN_ID:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken(
                        DOMAIN_NAME,
                        PROJECT_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)
                    PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                        DOMAIN_NAME,
                                                        PROJECT_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(
                        DOMAIN_ID,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            # Ensure DOMAIN_NAME and PROJECT_NAME
            DOMAIN_NAME = self.ensure_service_name(SERVICE_USER_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))

            PROJECT_NAME = self.ensure_subservice_name(SERVICE_USER_TOKEN,
                                                       DOMAIN_ID,
                                                       PROJECT_ID,
                                                       PROJECT_NAME)
            self.logger.addFilter(ContextFilterSubService(PROJECT_NAME))

            self.logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            self.logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            self.logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)


            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            REFERENCE_URL = self.get_endpoint_iot_module(IOTMODULE)

            #if not REFERENCE_URL:
            #    return self.composeErrorCode(ex)
            DURATION="P1Y"

            # Set default ATTRIBUTES for subscription
            ATTRIBUTES = []

            # Set default ENTITIES for subscription
            ENTITIES = [ {
                "idPattern": ".*"
            } ]

            # Set default Notify conditions
            NOTIFY_ATTRIBUTES = []
            NOTIFY_ATTRIBUTES.append("TimeInstant")
            NOTIFY_CONDITIONS = [ {
                "type": "ONCHANGE",
                "condValues": NOTIFY_ATTRIBUTES
            } ]

            self.logger.debug("Trying to subscribe moduleiot in CB...")
            cb_res = self.cb.subscribeContext(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                PROJECT_NAME,
                REFERENCE_URL,
                DURATION,
                ENTITIES,
                ATTRIBUTES,
                NOTIFY_ATTRIBUTES
            )
            self.logger.debug("subscribeContext res=%s" % json.dumps(cb_res,
                                                                     indent=3))
            subscriptionid = cb_res['subscriptionId']
            self.logger.debug("subscription id=%s" % subscriptionid)

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "subscriptionid": subscriptionid
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return subscriptionid, DOMAIN_NAME, PROJECT_NAME

    def deactivate_module(self,
                          DOMAIN_NAME,
                          DOMAIN_ID,
                          PROJECT_NAME,
                          PROJECT_ID,
                          SERVICE_USER_NAME,
                          SERVICE_USER_PASSWORD,
                          SERVICE_USER_TOKEN,
                          IOTMODULE):

        ''' Deactivate IoT Module

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - PROJECT_ID: id of project
        - PROJECT_NAME: name of project
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - IOTMODULE: IoT Module to activate: STH, PERSEO
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % "***", #SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": self.get_extended_token(SERVICE_USER_TOKEN),
            "IOTMODULE": "%s" % IOTMODULE,
        }
        self.logger.debug("FLOW deactivate_module invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:

            if not SERVICE_USER_TOKEN:
                if not DOMAIN_ID:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken(
                        DOMAIN_NAME,
                        PROJECT_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)
                    PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                        DOMAIN_NAME,
                                                        PROJECT_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(
                        DOMAIN_ID,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)

            # Ensure DOMAIN_NAME and PROJECT_NAME
            DOMAIN_NAME = self.ensure_service_name(SERVICE_USER_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))

            PROJECT_NAME = self.ensure_subservice_name(SERVICE_USER_TOKEN,
                                                       DOMAIN_ID,
                                                       PROJECT_ID,
                                                       PROJECT_NAME)
            self.logger.addFilter(ContextFilterSubService(PROJECT_NAME))

            self.logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            self.logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            self.logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)

            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            REFERENCE_URL = self.get_endpoint_iot_module(IOTMODULE)

            self.logger.debug("Trying to get list subscriptions from CB...")
            cb_res = self.cb.getListSubscriptions(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                PROJECT_NAME
            )
            self.logger.debug("getListSubscriptions res=%s" % json.dumps(cb_res,
                                                                         indent=3))

            for sub in cb_res:
                subs_url = self.cb.get_subscription_callback_endpoint(sub)
                subscriptionid = sub['id']
                if subs_url.startswith(REFERENCE_URL):

                    self.cb.unsubscribeContext(SERVICE_USER_TOKEN,
                                               DOMAIN_NAME,
                                               PROJECT_NAME,
                                               sub['id'])
                    break

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "subscriptionid": subscriptionid
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return subscriptionid, DOMAIN_NAME, PROJECT_NAME


    def list_activated_modules(self,
                               DOMAIN_NAME,
                               DOMAIN_ID,
                               PROJECT_NAME,
                               PROJECT_ID,
                               SERVICE_USER_NAME,
                               SERVICE_USER_PASSWORD,
                               SERVICE_USER_TOKEN):

        '''List Activated IoT Modules

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - PROJECT_ID: id of project
        - PROJECT_NAME: name of project
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % "***", #SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": self.get_extended_token(SERVICE_USER_TOKEN),
        }
        self.logger.debug("FLOW list_activated_modules invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_USER_TOKEN:
                if not DOMAIN_ID:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken(
                        DOMAIN_NAME,
                        PROJECT_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)
                    PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                        DOMAIN_NAME,
                                                        PROJECT_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(
                        DOMAIN_ID,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)

            # Ensure DOMAIN_NAME and PROJECT_NAME
            DOMAIN_NAME = self.ensure_service_name(SERVICE_USER_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))

            PROJECT_NAME = self.ensure_subservice_name(SERVICE_USER_TOKEN,
                                                       DOMAIN_ID,
                                                       PROJECT_ID,
                                                       PROJECT_NAME)
            self.logger.addFilter(ContextFilterSubService(PROJECT_NAME))

            self.logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            self.logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            self.logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)

            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            self.logger.debug("Trying to get list subscriptions from CB...")
            cb_res = self.cb.getListSubscriptions(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                PROJECT_NAME
            )
            self.logger.debug("getListSubscriptions res=%s" % json.dumps(cb_res, indent=3))
            modules = self.cb.extract_modules_from_subscriptions(self, IOTMODULES, cb_res)
            self.logger.debug("modules=%s" % json.dumps(modules, indent=3))

        except Exception, ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "modules": modules
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return modules, DOMAIN_NAME, PROJECT_NAME
