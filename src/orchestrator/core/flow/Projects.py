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
                                                   DOMAIN_NAME,
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
                                                   DOMAIN_NAME,
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



    def register_service(self,
                       DOMAIN_ID,
                       DOMAIN_NAME,
                       PROJECT_ID,
                       PROJECT_NAME,
                       SERVICE_USER_NAME,
                       SERVICE_USER_PASSWORD,
                       SERVICE_USER_TOKEN):

        '''Register Service in IOTA

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
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN
        }
        logger.debug("register_service invoked with: %s" % json.dumps(data_log,
                                                                 indent=3))

        try:

            if not SERVICE_USER_TOKEN:
                if not DOMAIN_ID:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken(DOMAIN_NAME,
                                                                        PROJECT_NAME,
                                                                        SERVICE_USER_NAME,
                                                                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)
                    PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEM,
                                                        DOMAIN_NAME,
                                                        ROJECT_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(DOMAIN_ID,
                                                                         PROJECT_ID,
                                                                         SERVICE_USER_NAME,
                                                                         SERVICE_USER_PASSWORD)
                    #DOMAIN_NAME =
                    #PROJECT_NAME =
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)

            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            # call CB
            cb_res = self.cb.updateContext(SERVICE_USER_TOKEN,
                                           SERVICE_NAME,
                                           SUBSERVICE_NAME,
                                           ENTITY_TYPE,
                                           ENTITY_ID,
                                           ATTRIBUTES=[],

                                           # ID: S-001
                                           # TYPE: service
                                           # isPattern: false
                                           # name: TheService
                                           # provider: ThirdParty
                                           # endpint: http://thirdparty
                                           # method: GET
                                           # authentication: context-adapter | third-party
                                           # mapping: [...]
                                           # timeout: 120
                                           )

            DEVICE_ID = cb_res # TODO: extract DeviceID from ContextBroker response

            logger.debug("DEVICE_ID=%s" % DEVICE_ID)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DEVICE_ID": DEVICE_ID
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))
        return DEVICE_ID


    def register_device(self,
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

            # call CB
            self.cb.updateContext(SERVICE_USER_TOKEN,
                                  SERVICE_NAME,
                                  SUBSERVICE_NAME,
                                  ENTITY_TYPE,
                                  ENTITY_ID,
                                  ATTRIBUTES=[]
                                  )

            # call CB
            self.cb.registerContext(SERVICE_USER_TOKEN,
                                    SERVICE_NAME,
                                    SUBSERVICE_NAME,
                                    ENTITIES=[],
                                    ATTRIBUTES=[],
                                    APP="",
                                    DURATION="")

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {

        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        # return  ?
