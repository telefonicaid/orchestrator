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
                         SERVICE_USER_TOKEN,
                         ENTITY_TYPE=None,
                         ENTITY_ID=None
                         IS_PATTERN=None,
                         ATT_NAME=None,
                         ATT_PROVIDER=None,
                         ATT_ENDPOINT=None,
                         ATT_METHOD=None,
                         ATT_AUTHENTICATION=None,
                         ATT_MAPPING=None,
                         ATT_TIMEOUT=None
                       ):

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
        - ENTITY_TYPE:   (optional, just for Device configuration)
        - ENTITY_ID:
        - IS_PATTERN
        - ATT_NAME=
        - ATT_PROVIDER
        - ATT_ENDPOINT
        - ATT_METHOD
        - ATT_AUTHENTICATION
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
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN
            "ENTITY_TYPE": "%s" % ENTITY_TYPE,
            "ENTITY_ID": "%s" % ENTITY_ID,
            "IS_PATTERN": "%s" % IS_PATTERN,
            "ATT_NAME": "%s" % ATT_NAME,
            "ATT_PROVIDER": "%s" % ATT_PROVIDER,
            "ATT_METHOD": "%s" % ATT_METHOD,
            "ATT_AUTHENTICATION": "%s" % ATT_AUTHENTICATION,
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
                                           # ID: S-001
                                           # TYPE: service
                                           # isPattern: false
                                           ENTITY_TYPE,
                                           ENTITY_ID,
                                           IS_PATTERN,
                                           ATTRIBUTES=[
                                           # name: TheService
                                           # provider: ThirdParty
                                           # endpint: http://thirdparty
                                           # method: GET
                                           # authentication: context-adapter | third-party
                                           # mapping: [...]
                                           # timeout: 120
                                           {
                                               "name": "name",
                                               "type": "string",
                                               "value": NAME
                                           },
                                           {
                                               "name": "provider",
                                               "type": "string",
                                               "value": PROVIDER
                                           },
                                           {
                                               "name": "endpoint",
                                               "type": "string",
                                               "value": ENDPOINT
                                           },
                                           {
                                               "name": "method",
                                               "type": "string",
                                               "value": METHOD
                                           },
                                           {
                                               "name": "authentication",
                                               "type": "string",
                                               "value": AUTHENTICATION
                                           },
                                           {
                                               "name": "mapping",
                                               "type": "string",
                                               "value": MAPPING
                                           },
                                           {
                                               "name": "timeout",
                                               "type": "integer",
                                               "value": TIMEOUT
                                           },
                                               ],
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

            res_iota = self.iota.registerDevice(SERVICE_USER_TOKEN,
                                                SERVICE_NAME,
                                                SUBSERVICE_NAME,
                                                DEVICE_ID,
                                                PROTOCOL,
                                                # resource: ???
                                                # service: client_a
                                                # service_path: /some_area
                                                # entity_name: <device_id> XXX
                                                # entity_type: button
                                                # timeozne: America/Santiago
                                                # lazy: lazy_op_status: string
                                        )

            # call CB
            res_cb = self.cb.updateContext(SERVICE_USER_TOKEN,
                                           SERVICE_NAME,
                                           SUBSERVICE_NAME,
                                           ENTITY_TYPE,
                                           ENTITY_ID,
                                           IS_PATTERN,
                                           # id: <device_id>XXX
                                           # type: button
                                           # isPattern: flase
                                           ATTRIBUTES=[
                                           # internal_id: <device_id>
                                           # external_id: ZZZZ
                                           # ccid: AAA
                                           # imei: 1234567789
                                           # imsi: 4566789034
                                           # interaction_tupe: synchronous
                                           # service_id: S-001
                                           # geolocation: 44.0,-3.34
                                           {
                                               "name": "internal_id",
                                               "type": "string",
                                               "value": INTERNAL_ID
                                           },
                                           {
                                               "name": "external_id",
                                               "type": "string",
                                               "value": EXTERNAL_ID
                                           },
                                           {
                                               "name": "ccid",
                                               "type": "string",
                                               "value": CCID
                                           },
                                           {
                                               "name": "imei",
                                               "type": "string",
                                               "value": IMEI
                                           },
                                           {
                                               "name": "imsi",
                                               "type": "string",
                                               "value": IMSI
                                           },
                                           {
                                               "name": "interaction_type",
                                               "type": "string",
                                               "value": INTERACTION_TYPE
                                           },
                                           {
                                               "name": "service_id",
                                               "type": "string",
                                               "value": SERVICE_ID
                                           },
                                           {
                                               "name": "geolocation",
                                               "type": "string",
                                               "value": GEOLOCATION
                                           },
                                               ]
                                               )
            # TODO: extract info from res_cb

            # call CB
            res_cb = self.cb.registerContext(SERVICE_USER_TOKEN,
                                    SERVICE_NAME,
                                    SUBSERVICE_NAME,
                                    # entities: <device_id>XXX:button
                                    ENTITIES= DEVICE_ID + 'button',
                                    ATTRIBUTES=[
                                            # aux_external_id,
                                            # aux_op_action,
                                            # aux_op_extra:
                                            # aux_op_status
                                           {
                                               "name": "aux_external_id",
                                               "type": "string",
                                               "value": AUX_EXTERNAL_ID
                                           },
                                           {
                                               "name": "aux_op_action",
                                               "type": "string",
                                               "value": AUX_OP_ACTION
                                           },
                                           {
                                               "name": "aux_op_extra",
                                               "type": "string",
                                               "value": AUX_OP_EXTRA
                                           },
                                           {
                                               "name": "aux_op_status",
                                               "type": "string",
                                               "value": AUX_OP_STATUS
                                           },
                                    ],
                                    # providin_appligation: http://the_context_adapter.com
                                    APP,
                                    # duration: P1M
                                    DURATION
                                    )
            # TODO: extract info from res_cb

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {

        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        # return  ?
