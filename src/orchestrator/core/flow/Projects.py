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
import logging
import json

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


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
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN
        }
        logger.debug("createNewService invoked with: %s" % json.dumps(
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
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
                                                  DOMAIN_ID)

            logger.debug("PROJECTS=%s" % PROJECTS)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "PROJECTS": PROJECTS
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return PROJECTS

    def get_project(self,
                    DOMAIN_ID,
                    PROJECT_ID,
                    ADMIN_USER,
                    ADMIN_PASSWORD,
                    ADMIN_TOKEN):

        '''Ge Project detail of a domain

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - PROJECT_ID: id of project
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - project detail
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN
        }
        logger.debug("get_project invoked with: %s" % json.dumps(data_log,
                                                                 indent=3))

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                 ADMIN_USER,
                                                 ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            PROJECT = self.idm.getProject(ADMIN_TOKEN,
                                          PROJECT_ID)
            # PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
            #                                       DOMAIN_ID)
            # for project in PROJECTS:
            #     if project['id'] == PROJECT_ID:
            #         PROJECT = project

            logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "PROJECT": PROJECT
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return PROJECT

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
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN,
            "NEW_SUBSERVICE_DESCRIPTION": "%s" % NEW_SUBSERVICE_DESCRIPTION,
        }
        logger.debug("update_project invoked with: %s" % json.dumps(
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
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(ADMIN_TOKEN,
                                                   PROJECT_NAME)

            PROJECT = self.idm.updateProject(ADMIN_TOKEN,
                                             DOMAIN_ID,
                                             PROJECT_ID,
                                             NEW_SUBSERVICE_DESCRIPTION)

            logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "PROJECT": PROJECT
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return PROJECT

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
            "ADMIN_PASSWORD": "%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN": "%s" % ADMIN_TOKEN
        }
        logger.debug("get_project invoked with: %s" % json.dumps(data_log,
                                                                 indent=3))

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
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(ADMIN_TOKEN,
                                                   PROJECT_NAME)

            PROJECT = self.idm.disableProject(ADMIN_TOKEN,
                                              DOMAIN_ID,
                                              PROJECT_ID)

            self.idm.deleteProject(ADMIN_TOKEN,
                                   PROJECT_ID)

            logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "PROJECT": PROJECT
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))
        return PROJECT
