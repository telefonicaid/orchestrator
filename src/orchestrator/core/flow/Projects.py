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
                         DOMAIN_NAME,
                         DOMAIN_ID,
                         PROJECT_NAME,
                         PROJECT_ID,
                         SERVICE_USER_NAME,
                         SERVICE_USER_PASSWORD,
                         SERVICE_USER_TOKEN,
                         ENTITY_TYPE,
                         ENTITY_ID,
                         ATT_NAME,
                         ATT_PROVIDER,
                         ATT_ENDPOINT,
                         ATT_METHOD,
                         ATT_AUTHENTICATION,
                         ATT_INTERACTION_TYPE,
                         ATT_MAPPING,
                         ATT_TIMEOUT
                       ):

        '''Register entity Service (in CB)

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - PROJECT_ID: id of project
        - PROJECT_NAME: name of project
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - ENTITY_TYPE:   (optional, just for Device configuration)
        - ENTITY_ID:
        - ATT_NAME
        - ATT_PROVIDER
        - ATT_ENDPOINT
        - ATT_METHOD
        - ATT_AUTHENTICATION
        - ATT_INTERACTION_TYPE
        - ATT_MAPPING
        - ATT_TIMEOUT
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
            "ENTITY_TYPE": "%s" % ENTITY_TYPE,
            "ENTITY_ID": "%s" % ENTITY_ID,
            "ATT_NAME": "%s" % ATT_NAME,
            "ATT_PROVIDER": "%s" % ATT_PROVIDER,
            "ATT_ENDPOINT": "%s" % ATT_ENDPOINT,
            "ATT_METHOD": "%s" % ATT_METHOD,
            "ATT_AUTHENTICATION": "%s" % ATT_AUTHENTICATION,
            "ATT_INTERACTION_TYPE": "%s" % ATT_INTERACTION_TYPE,
            "ATT_MAPPING": "%s" % ATT_MAPPING,
            "ATT_TIMEOUT": "%s" % ATT_TIMEOUT
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
            # TODO: Ensure DOMAIN_NAME and PROJECT_NAME
            # get DOMAIN_NAME from SERVICE_USER_TOKEN

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)


            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            IS_PATTERN="false"
            ATTRIBUTES=[
                {
                    "name": "name",
                    "type": "string",
                    "value": ATT_NAME
                },
                {
                    "name": "provider",
                    "type": "string",
                    "value": ATT_PROVIDER
                },
                {
                    "name": "endpoint",
                    "type": "string",
                    "value": ATT_ENDPOINT
                },
                {
                    "name": "method",
                    "type": "string",
                    "value": ATT_METHOD
                },
                {
                    "name": "authentication",
                    "type": "string",
                    "value": ATT_AUTHENTICATION
                },
                {
                    "name": "interaction_type",
                    "type": "string",
                    "value": ATT_INTERACTION_TYPE
                },
                {
                    "name": "mapping",
                    "type": "string",
                    "value": ATT_MAPPING
                },
                {
                    "name": "timeout",
                    "type": "integer",
                    "value": ATT_TIMEOUT
                }
            ]

            # call CB
            cb_res = self.cb.updateContext(SERVICE_USER_TOKEN,
                                           DOMAIN_NAME,
                                           PROJECT_NAME,
                                           ENTITY_TYPE,
                                           ENTITY_ID,
                                           IS_PATTERN,
                                           ATTRIBUTES
                                        )

            logger.debug("updateContext res=%s" % cb_res)

            for r in cb_res['contextResponses']:
                # Check ContextBroker status response
                if r['statusCode']['code'] != '200':
                    raise Exception(r['statusCode']['reasonPhrase'])

            logger.debug("ENTITY_ID=%s" % ENTITY_ID)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ENTITY_ID": ENTITY_ID
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))
        return ENTITY_ID


    def register_device(self,
                        DOMAIN_NAME,
                        DOMAIN_ID,
                        PROJECT_NAME,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SERVICE_USER_TOKEN,
                        DEVICE_ID,
                        ENTITY_TYPE,
                        PROTOCOL,
                        ATT_INTERNAL_ID,
                        ATT_CCID,
                        ATT_IMEI,
                        ATT_IMSI,
                        ATT_INTERACTION_TYPE,
                        ATT_SERVICE_ID,
                        ATT_GEOLOCATION
                        ):

        '''Register Device in IOTA

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_NAME: Service name
        - DOMAIN_ID: Service id
        - PROJECT_NAME: SubService name
        - PROJECT_ID: SubService name
        - SERVICE_USER_NAME: Service admin username
        - SERVICE_USER_PASSWORD: Service admin password
        - SERVICE_USER_TOKEN: Service admin token
        - DEVICE_ID: Device ID
        - ENTITY_TYPE: Entity Type
        - PROTOCOL: Protocol of the device
        - ATT_INTERNAL_ID
        - ATT_CCID
        - ATT_IMEI
        - ATT_IMSI
        - ATT_INTERACTION_TYPE
        - ATT_SERVICE_ID
        - ATT_GEOLOCATION
        '''
        data_log = {
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
            "DEVICE_ID": "%s" % DEVICE_ID,
            "PROTOCOL": "%s" % PROTOCOL,
            "ENTITY_TYPE": "%s" % ENTITY_TYPE,
            "ATT_INTERNAL_ID": "%s" % ATT_INTERNAL_ID,
            "ATT_CCID": "%s" % ATT_CCID,
            "ATT_IMEI": "%s" % ATT_IMEI,
            "ATT_IMSI": "%s" % ATT_IMSI,
            "ATT_INTERACTION_TYPE": "%s" % ATT_INTERACTION_TYPE,
            "ATT_SERVICE_ID": "%s" % ATT_SERVICE_ID,
            "ATT_GEOLOCATION": "%s" % ATT_GEOLOCATION
        }
        logger.debug("register_device with: %s" % json.dumps(data_log, indent=3))
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
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)


            # TODO: ensure DOMAIN_NAME and PROJECT_NAME

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)


            #
            # 1. Call IOTA for register button
            #
            TIMEZONE = "Europe/Madrid" # TODO: get from django conf
            ENTITY_NAME = DEVICE_ID
            LAZY=[]
            ATTRIBUTES=[]
            STATIC_ATTRIBUTES = []
            INTERNAL_ATTRIBUTES = []
            COMMANDS = []

            if PROTOCOL == "TT_BLACKBUTTON":
                if ATT_INTERACTION_TYPE == None:
                    ATT_INTERACTION_TYPE = "synchronous"
                ATTRIBUTES = [
                    {
                        "name": "internalId",
                        "type": "string"
                    },
                    {
                        "name": "last_operation",
                        "type": "string"
                    },
                    {
                        "name": "op_status",
                        "type": "string"
                    },
                    {
                        "name": "op_result",
                        "type": "string"
                    },
                    {
                        "name": "op_action",
                        "type": "string"
                    },
                    {
                        "name": "op_extra",
                        "type": "string"
                    }
                    ]

                STATIC_ATTRIBUTES=[
                    {
                        "name": "internal_id",
                        "type": "string",
                        "value": ATT_INTERNAL_ID
                    },
                    {
                        "name": "ccid",
                        "type": "string",
                        "value": ATT_CCID
                    },
                    {
                        "name": "imei",
                        "type": "string",
                        "value": ATT_IMEI
                    },
                    {
                        "name": "imsi",
                        "type": "string",
                        "value": ATT_IMSI
                    },
                    {
                        "name": "interaction_type",
                        "type": "string",
                        "value": ATT_INTERACTION_TYPE
                    },
                    {
                        "name": "aux_interaction_type",
                        "type": "string",
                        "value": ATT_INTERACTION_TYPE
                    },
                    {
                        "name": "service_id",
                        "type": "string",
                        "value": ATT_SERVICE_ID
                    },
                    {
                        "name": "geolocation",
                        "type": "string",
                        "value": ATT_GEOLOCATION
                    }
                    ]


                if ATT_INTERACTION_TYPE == "synchronous":
                    LAZY = [
                        {
                            "name": "lazy_op_result",
                            "type": "string"
                        }
                    ]

            iota_res = self.iota.registerDevice(SERVICE_USER_TOKEN,
                                                DOMAIN_NAME,
                                                PROJECT_NAME,
                                                DEVICE_ID,
                                                PROTOCOL,
                                                ENTITY_NAME,
                                                ENTITY_TYPE,
                                                TIMEZONE,
                                                ATTRIBUTES,
                                                STATIC_ATTRIBUTES,
                                                COMMANDS,
                                                INTERNAL_ATTRIBUTES,
                                                LAZY
                                        )
            logger.debug("registerDevice res=%s" % iota_res)


            #
            # 2. Call ContextBroker for register Context Adapter
            #

            ATTRIBUTES = []
            APP="http://localhost"
            DURATION="P1M"
            ENTITIES=[]

            if PROTOCOL == "TT_BLACKBUTTON":
                APP=self.ca_endpoint
                IS_PATTERN="false"
                DURATION="P1M"
                ENTITIES = [
                    {
                        "type": ENTITY_TYPE,
                        "isPattern": IS_PATTERN,
                        "id": DEVICE_ID
                    }
                ]
                ATTRIBUTES=[
                    {
                        "name": "aux_op_action",
                        "type": "string",
                        "isDomain": "false"
                    },
                    {
                        "name": "aux_op_extra",
                        "type": "string",
                        "isDomain": "false"
                    },
                    {
                        "name": "aux_op_status",
                        "type": "string",
                        "isDomain": "false"
                    },
                    {
                        "name": "aux_interaction_type",
                        "type": "string",
                        "isDomain": "false"
                    },
                    {
                        "name": "aux_service_id",
                        "type": "string",
                        "isDomain": "false"
                    }
                ]


            cb_res = self.cb.registerContext(SERVICE_USER_TOKEN,
                                             DOMAIN_NAME,
                                             PROJECT_NAME,
                                             ENTITIES,
                                             ATTRIBUTES,
                                             APP,
                                             DURATION
                                             )
            logger.debug("registerContext res=%s" % cb_res)
            registrationid = cb_res['registrationId']
            logger.debug("registration id=%s" % registrationid)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "registrationid": registrationid
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return  registrationid
