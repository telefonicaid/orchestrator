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
from orchestrator.common.util import CSVOperations

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

            if not PROJECT_NAME:
                logger.debug("Not PROJECT_NAME provided, getting it from token")
                PROJECT_NAME = self.idm.getProjectNameFromToken(
                    ADMIN_TOKEN,
                    DOMAIN_ID,
                    PROJECT_ID)

            #
            # Delete all devices
            #
            devices_deleted = self.iota.deleteAllDevices(ADMIN_TOKEN,
                                                         DOMAIN_NAME,
                                                         PROJECT_NAME)
            if (len(devices_deleted) > 0):
                logger.info("devices deleted %s", devices_deleted)


            #
            # Delete all subscriptions
            #
            subscriptions_deleted = self.cb.deleteAllSubscriptions(
                                                              ADMIN_TOKEN,
                                                              DOMAIN_NAME,
                                                              PROJECT_NAME)
            if (len(subscriptions_deleted) > 0):
                logger.info("subscriptions deleted %s", subscriptions_deleted)

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
                         PROTOCOL,
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
        - PROTOCOL:
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
            "PROTOCOL": "%s" % PROTOCOL,
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
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken(
                        DOMAIN_NAME,
                        PROJECT_NAME,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(SERVICE_USER_TOKEN,
                                                     DOMAIN_NAME)
                    PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEM,
                                                        DOMAIN_NAME,
                                                        ROJECT_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(
                        DOMAIN_ID,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            # Ensure DOMAIN_NAME and PROJECT_NAME
            if not DOMAIN_NAME:
                logger.debug("Not DOMAIN_NAME provided, getting it from token")
                DOMAIN_NAME = self.idm.getDomainNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID)
            if not PROJECT_NAME:
                logger.debug("Not PROJECT_NAM provided, getting it from token")
                PROJECT_NAME = self.idm.getProjectNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID,
                    PROJECT_ID)

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)


            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            #
            # 1. Register Entity Service in CB
            #
            IS_PATTERN="false"
            ACTION="APPEND"
            ATTRIBUTES=[]
            STATIC_ATTRIBUTES=[]

            if ATT_NAME and ATT_NAME != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "name",
                        "type": "string",
                        "value": ATT_NAME
                    })
            if ATT_PROVIDER and ATT_PROVIDER != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "provider",
                        "type": "string",
                        "value": ATT_PROVIDER
                    })
            if ATT_ENDPOINT and ATT_ENDPOINT != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "endpoint",
                        "type": "string",
                        "value": ATT_ENDPOINT
                    })
            if ATT_METHOD and ATT_METHOD != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "method",
                        "type": "string",
                        "value": ATT_METHOD
                    })
            if ATT_AUTHENTICATION and ATT_AUTHENTICATION != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "authentication",
                        "type": "string",
                        "value": ATT_AUTHENTICATION
                    })
            if ATT_INTERACTION_TYPE and ATT_INTERACTION_TYPE != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "interaction_type",
                        "type": "string",
                        "value": ATT_INTERACTION_TYPE
                    })
            if ATT_MAPPING and ATT_MAPPING != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "mapping",
                        "type": "string",
                        "value": ATT_MAPPING
                    })
            if ATT_TIMEOUT and ATT_TIMEOUT != "":
                STATIC_ATTRIBUTES.append(
                    {
                        "name": "timeout",
                        "type": "integer",
                        "value": ATT_TIMEOUT
                    })

            # call CB
            cb_res = self.cb.updateContext(SERVICE_USER_TOKEN,
                                           DOMAIN_NAME,
                                           PROJECT_NAME,
                                           ENTITY_TYPE,
                                           ENTITY_ID,
                                           ACTION,
                                           IS_PATTERN,
                                           STATIC_ATTRIBUTES
                                        )

            logger.debug("updateContext res=%s" % cb_res)

            for r in cb_res['contextResponses']:
                # Check ContextBroker status response
                if r['statusCode']['code'] != '200':
                    raise Exception(r['statusCode']['reasonPhrase'])

            logger.debug("ENTITY_ID=%s" % ENTITY_ID)


            #
            # 2. Subscribe Context Adapter in ContextBroker
            #
            DURATION="P1M"
            REFERENCE_URL="http://localhost"
            ENTITIES=[]
            ATTRIBUTES = []
            NOTIFY_CONDITIONS = []

            if PROTOCOL == "TT_BLACKBUTTON":
                ENTITY_TYPE="BlackButton"
                REFERENCE_URL = self.ca_endpoint + '/notify' #"http://<ip_ca>:<port_ca>/"
                ENTITIES = [
                    {
                        "type": ENTITY_TYPE,
                        "isPattern": "true",
                        "id": ".*"
                    }
                ]
                ATTRIBUTES=[
                    "op_action",
                    "op_extra",
                    "op_status",
                    "interaction_type",
                    "service_id",
                    "TimeInstant"
                ]
                NOTIFY_CONDITIONS = [
                    {
                        "type": "ONCHANGE",
                        "condValues": [
                            "op_status",
                            "TimeInstant"
                        ]
                    }
                ]

            cb_res = self.cb.subscribeContext(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                PROJECT_NAME,
                REFERENCE_URL,
                DURATION,
                ENTITIES,
                ATTRIBUTES,
                NOTIFY_CONDITIONS
            )
            logger.debug("subscribeContext res=%s" % cb_res)
            subscriptionid_ca = cb_res['subscribeResponse']['subscriptionId']
            logger.debug("subscription id ca=%s" % subscriptionid_ca)



            #
            # 3.1 Subscribe Cygnus
            #
            DURATION="P1M"
            ENTITIES=[]
            ATTRIBUTES=[]
            NOTIFY_CONDITIONS=[]
            REFERENCE_URL="http://localhost"
            if PROTOCOL == "TT_BLACKBUTTON":
                ENTITY_TYPE="BlackButton"
                #"http://<ip_ca>:<port_ca>/"
                REFERENCE_URL=self.cygnus_endpoint + '/notify'
                ENTITIES = [
                    {
                        "type": ENTITY_TYPE,
                        "isPattern": "true",
                        "id": ".*"
                    }
                ]
                ATTRIBUTES=[
                        "internal_id",
                        "last_operation",
                        "op_status",
                        "op_result",
                        "op_action",
                        "op_extra",
                        "sleepcondition",
                        "sleeptime",
                        "iccid",
                        "imei",
                        "imsi",
                        "interaction_type",
                        "service_id",
                        "geolocation"

                ]
                NOTIFY_CONDITIONS = [
                    {
                        "type": "ONCHANGE",
                        "condValues": [
                            "op_status",  # reduntant?
                            "TimeInstant"
                        ]
                    }
                ]

            if PROTOCOL == "PDI-IoTA-ThinkingThings":
                ENTITY_TYPE="Thing"
                REFERENCE_URL = self.cygnus_endpoint + '/notify'
                ENTITIES = [
                    {
                        "type": ENTITY_TYPE,
                        "isPattern": "true",
                        "id": ".*"
                    }
                ]
                ATTRIBUTES=[
                    "mcc",
                    "mnc"
                    "lac"
                    "cellid",
                    "dbm",
                    "temperature",
                    "humidity",
                    "luminance",
                    "voltage",
                    "state",
                    "charger"
                    "charging",
                    "mode",
                    "desconnection",
                    "sleepcondition",
                    "color",
                    "melody",
                    "sleeptime",
                ]
                NOTIFY_CONDITIONS = [
                    {
                        "type": "ONCHANGE",
                        "condValues": [
                            "humidity",
                            "temperature",
                            "state"
                        ]
                    }
                ]

            if len(ENTITIES) > 0:
                cb_res = self.cb.subscribeContext(
                    SERVICE_USER_TOKEN,
                    DOMAIN_NAME,
                    PROJECT_NAME,
                    REFERENCE_URL,
                    DURATION,
                    ENTITIES,
                    ATTRIBUTES,
                    NOTIFY_CONDITIONS
                    )
                logger.debug("subscribeContext res=%s" % cb_res)
                subscriptionid_cyg = cb_res['subscribeResponse']['subscriptionId']
                logger.debug("registration id cygnus=%s" % subscriptionid_cyg)

            #
            # 3.2 Subscribe Short Term Historic (STH)
            #
            REFERENCE_URL = "http://localhost"
            if PROTOCOL == "TT_BLACKBUTTON":
                REFERENCE_URL = self.sth_endpoint + '/notify'

            if PROTOCOL == "PDI-IoTA-ThinkingThings":
                REFERENCE_URL = self.sth_endpoint + '/notify'

            if len(ENTITIES) > 0:
                cb_res = self.cb.subscribeContext(
                    SERVICE_USER_TOKEN,
                    DOMAIN_NAME,
                    PROJECT_NAME,
                    REFERENCE_URL,
                    DURATION,
                    ENTITIES,
                    ATTRIBUTES,
                    NOTIFY_CONDITIONS
                    )
                logger.debug("subscribeContext res=%s" % cb_res)
                subscriptionid_sth = cb_res['subscribeResponse']['subscriptionId']
                logger.debug("registration id sth=%s" % subscriptionid_sth)


            #
            # 3.3 Perseo
            #
            REFERENCE_URL = "http://localhost"
            if PROTOCOL == "TT_BLACKBUTTON":
                REFERENCE_URL = self.perseo_endpoint + '/notify'

            if PROTOCOL == "PDI-IoTA-ThinkingThings":
                REFERENCE_URL = self.perseo_endpoint + '/notify'

            if len(ENTITIES) > 0:
                cb_res = self.cb.subscribeContext(
                    SERVICE_USER_TOKEN,
                    DOMAIN_NAME,
                    PROJECT_NAME,
                    REFERENCE_URL,
                    DURATION,
                    ENTITIES,
                    ATTRIBUTES,
                    NOTIFY_CONDITIONS
                    )
                logger.debug("subscribeContext res=%s" % cb_res)
                subscriptionid_perseo = cb_res['subscribeResponse']['subscriptionId']
                logger.debug("registration id perseo=%s" % subscriptionid_perseo)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ENTITY_ID": ENTITY_ID,
            "subscriptionid_ca": subscriptionid_ca,
            "subscriptionid_cyg": subscriptionid_cyg,
            "subscriptionid_sth": subscriptionid_sth,
            "subscriptionid_perseo": subscriptionid_perseo
        }
        logger.info("Summary report : %s" % json.dumps(data_log,
                                                       indent=3))

        return subscriptionid_ca, subscriptionid_cyg, subscriptionid_sth, subscriptionid_perseo


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
                        ATT_ICCID,
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
        - ATT_ICCID: device attribute iccid
        - ATT_IMEI: device attribute imei
        - ATT_IMSI: device attribute imsi
        - ATT_INTERACTION_TYPE: device attribute interaction_type
        - ATT_SERVICE_ID: device attribute service_id
        - ATT_GEOLOCATION: device attribute geolocation
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
            "ENTITY_TYPE": "%s" % ENTITY_TYPE,
            "PROTOCOL": "%s" % PROTOCOL,
            "ATT_ICCID": "%s" % ATT_ICCID,
            "ATT_IMEI": "%s" % ATT_IMEI,
            "ATT_IMSI": "%s" % ATT_IMSI,
            "ATT_INTERACTION_TYPE": "%s" % ATT_INTERACTION_TYPE,
            "ATT_SERVICE_ID": "%s" % ATT_SERVICE_ID,
            "ATT_GEOLOCATION": "%s" % ATT_GEOLOCATION
        }
        logger.debug("register_device with: %s" % json.dumps(data_log,
                                                             indent=3))
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


            # Ensure DOMAIN_NAME and PROJECT_NAME
            if not DOMAIN_NAME:
                DOMAIN_NAME = self.idm.getDomainNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID)
            if not PROJECT_NAME:
                PROJECT_NAME = self.idm.getProjectNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID,
                    PROJECT_ID)

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
                        "name": "internal_id",
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
                        "name": "op_action",
                        "type": "string"
                    },
                    {
                        "name": "op_extra",
                        "type": "string"
                    },
                    {
                        "name": "sleepcondition",
                        "type": "string"
                    },
                    {
                        "name": "sleeptime",
                        "type": "string"
                    },
                    {
                        "name": "TimeInstant",
                        "type": "string"
                    }
                    ]

                # Ensure attributes are not empty
                if ATT_ICCID and ATT_ICCID != "":
                    STATIC_ATTRIBUTES.append(
                        {
                            "name": "iccid",
                            "type": "string",
                            "value": ATT_ICCID
                        })

                if ATT_IMEI and ATT_IMEI != "":
                    STATIC_ATTRIBUTES.append(
                        {
                            "name": "imei",
                            "type": "string",
                            "value": ATT_IMEI
                        })


                if ATT_IMSI and ATT_IMSI != "":
                    STATIC_ATTRIBUTES.append(
                        {
                            "name": "imsi",
                            "type": "string",
                            "value": ATT_IMSI
                        })

                if ATT_INTERACTION_TYPE and ATT_INTERACTION_TYPE != "":
                    STATIC_ATTRIBUTES.append(
                        {
                            "name": "interaction_type",
                            "type": "string",
                            "value": ATT_INTERACTION_TYPE
                        })

                if ATT_SERVICE_ID and ATT_SERVICE_ID != "":
                    STATIC_ATTRIBUTES.append(
                        {
                            "name": "service_id",
                            "type": "string",
                            "value": ATT_SERVICE_ID
                        })

                if ATT_GEOLOCATION and ATT_GEOLOCATION != "":
                    STATIC_ATTRIBUTES.append(
                        {
                            "name": "geolocation",
                            "type": "string",
                            "value": ATT_GEOLOCATION
                        })

                if ATT_INTERACTION_TYPE == "synchronous":
                    LAZY = [
                        {
                            "name": "op_result",
                            "type": "string"
                        }
                    ]
                if ATT_INTERACTION_TYPE == "asynchronous":
                    ATTRIBUTES.append(
                        {
                            "name": "op_result",
                            "type": "string"
                        })

            if PROTOCOL == "PDI-IoTA-ThinkingThings":
                if ATT_INTERACTION_TYPE == None:
                    ATT_INTERACTION_TYPE = "synchronous"
                ATTRIBUTES = [
                    {
                        "name": "mcc",
                        "type": "integer"
                    },
                    {
                        "name": "mnc",
                        "type": "integer"
                    },
                    {
                        "name": "lac",
                        "type": "integer"
                    },
                    {
                        "name": "cellid",
                        "type": "string"
                    },
                    {
                        "name": "dbm",
                        "type": "integer"
                    },
                    {
                        "name": "temperature",
                        "type": "float"
                    },
                    {
                        "name": "humidity",
                        "type": "float"
                    },
                    {
                        "name": "luminance",
                        "type": "float"
                    },
                    {
                        "name": "voltage",
                        "type": "float"
                    },
                    {
                        "name": "state",
                        "type": "integer"
                    },
                    {
                        "name": "charger",
                        "type": "integer"
                    },
                    {
                        "name": "charging",
                        "type": "integer"
                    },
                    {
                        "name": "mode",
                        "type": "integer"
                    },
                    {
                        "name": "desconnection",
                        "type": "integer"
                    },
                    {
                        "name": "sleepcondition",
                        "type": "string"
                    },
                    {
                        "name": "color",
                        "type": "string"
                    },
                    {
                        "name": "melody",
                        "type": "string"
                    },
                    {
                        "name": "sleeptime",
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


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {

        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DEVICE_ID


    def register_devices(self,
                        DOMAIN_NAME,
                        DOMAIN_ID,
                        PROJECT_NAME,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SERVICE_USER_TOKEN,
                        CSV_DEVICES):

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
        - CSV_DEVICES: CSV content

        '''
        data_log = {
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
            "CSV_DEVICES": "%s" % CSV_DEVICES
        }
        logger.debug("register_devices with: %s" % json.dumps(data_log,
                                                              indent=3))
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


            # Read CSV
            i, header, devices = CSVOperations.read_devices(CSV_DEVICES)
            DEVICES_ID = []
            num_devices = len(devices[header[i]])
            for n in range(num_devices):

                data_log = {
                    "DEVICE_ID" : devices['DEVICE_ID'][n],
                    "ENTITY_TYPE" : devices['ENTITY_TYPE'][n],
                    "PROTOCOL": devices['PROTOCOL'][n],
                    "ATT_ICCID" : devices['ATT_ICCID'][n],
                    "ATT_IMEI" : devices['ATT_IMEI'][n],
                    "ATT_IMSI" : devices['ATT_IMSI'][n],
                    "ATT_INTERACTION_TYPE" : devices['ATT_INTERACTION_TYPE'][n],
                    "ATT_SERVICE_ID" : devices['ATT_SERVICE_ID'][n],
                    "ATT_GEOLOCATION" : devices['ATT_GEOLOCATION'][n]
                }
                logger.debug("data%s" % data_log)
                # TODO: use IOTA bulk API
                res = self.register_device(
                    DOMAIN_NAME,
                    DOMAIN_ID,
                    PROJECT_NAME,
                    PROJECT_ID,
                    SERVICE_USER_NAME,
                    SERVICE_USER_PASSWORD,
                    SERVICE_USER_TOKEN,
                    devices['DEVICE_ID'][n],
                    devices['ENTITY_TYPE'][n],
                    devices['PROTOCOL'][n],
                    devices['ATT_ICCID'][n],
                    devices['ATT_IMEI'][n],
                    devices['ATT_IMSI'][n],
                    devices['ATT_INTERACTION_TYPE'][n],
                    devices['ATT_SERVICE_ID'][n],
                    devices['ATT_GEOLOCATION'][n]
                )
                DEVICES_ID.append(res)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "devices": DEVICES_ID
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DEVICES_ID

    def unregister_device(self,
                        DOMAIN_NAME,
                        DOMAIN_ID,
                        PROJECT_NAME,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SERVICE_USER_TOKEN,
                        DEVICE_ID,
                        ):

        '''Unregister Device in IOTA

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
        }
        logger.debug("unregister_device with: %s" % json.dumps(data_log,
                                                             indent=3))
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


            # Ensure DOMAIN_NAME and PROJECT_NAME
            if not DOMAIN_NAME:
                DOMAIN_NAME = self.idm.getDomainNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID)
            if not PROJECT_NAME:
                PROJECT_NAME = self.idm.getProjectNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID,
                    PROJECT_ID)

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)

            iota_res = self.iota.unregisterDevice(
                                                SERVICE_USER_TOKEN,
                                                DOMAIN_NAME,
                                                PROJECT_NAME,
                                                DEVICE_ID)
            logger.debug("unregisterDevice res=%s" % iota_res)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {

        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        #return DEVICE_ID


    def activate_module(self,
                        DOMAIN_NAME,
                        DOMAIN_ID,
                        PROJECT_NAME,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD,
                        SERVICE_USER_TOKEN,
                        MODULE_NAME):

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
        - MODULE_NAME: Module to activate: STH, CYGNUS, CKAN, CEP
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_PASSWORD": "%s" % SERVICE_USER_PASSWORD,
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
            "MODULE_NAME": "%s" % MODULE_NAME,
        }
        logger.debug("activate_module invoked with: %s" % json.dumps(data_log,
                                                                     indent=3))

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
                    PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEM,
                                                        DOMAIN_NAME,
                                                        ROJECT_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(
                        DOMAIN_ID,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            # Ensure DOMAIN_NAME and PROJECT_NAME
            if not DOMAIN_NAME:
                logger.debug("Not DOMAIN_NAME provided, getting it from token")
                DOMAIN_NAME = self.idm.getDomainNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID)
            if not PROJECT_NAME:
                logger.debug("Not PROJECT_NAM provided, getting it from token")
                PROJECT_NAME = self.idm.getProjectNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID,
                    PROJECT_ID)

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)


            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)

            if MODULE_NAME in ["STH", "sth"]:
                REFERENCE_URL = self.sth_endpoint + '/notify'
            if MODULE_NAME in ["CYGNUS", "cygnus"]:
                REFERENCE_URL = self.cygnus_endpoint + '/notify'
            if MODULE_NAME in ["CEP", "cep"]:
                REFERENCE_URL = self.cep_endpoint + '/notify'

            #if not REFERENCE_URL:
            #    return self.composeErrorCode(ex)

            # Set default ATTRIBUTES for subscription
            ATTRIBUTES = []
            db_res = self.cb.getContextTypes(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                PROJECT_NAME,
                ENTITY_TYPE)
            for entity_type in cb_res:
                ATTRIBUTES.append(entity_type["attributes"])

            # Set default ENTITIES for subscription
            ENTITIES = [ {
                "isPattern": "true",
                "id": ".*"
            } ]

            # Set default Notify conditions
            NOTIFY_ATTRIBUTES = ATTRIBUTES
            NOTIFY_ATTRIBUTES.append("TimeInstant")
            NOTIFY_CONDITIONS = [ {
                "type": "ONCHANGE",
                "condValues": NOTIFY_ATTRIBUTES
            } ]

            cb_res = self.cb.subscribeContext(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                PROJECT_NAME,
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

        return subscriptionid


    def list_modules_actives(self,
                             DOMAIN_NAME,
                             DOMAIN_ID,
                             PROJECT_NAME,
                             PROJECT_ID,
                             SERVICE_USER_NAME,
                             SERVICE_USER_PASSWORD,
                             SERVICE_USER_TOKEN):

        '''List Modules Actives

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
            "SERVICE_USER_TOKEN": "%s" % SERVICE_USER_TOKEN,
        }
        logger.debug("list_modules_actives invoked with: %s" % json.dumps(data_log,
                                                                          indent=3))

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
                    PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEM,
                                                        DOMAIN_NAME,
                                                        ROJECT_NAME)

                else:
                    SERVICE_USER_TOKEN = self.idm.getScopedProjectToken2(
                        DOMAIN_ID,
                        PROJECT_ID,
                        SERVICE_USER_NAME,
                        SERVICE_USER_PASSWORD)
            # Ensure DOMAIN_NAME and PROJECT_NAME
            if not DOMAIN_NAME:
                logger.debug("Not DOMAIN_NAME provided, getting it from token")
                DOMAIN_NAME = self.idm.getDomainNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID)
            if not PROJECT_NAME:
                logger.debug("Not PROJECT_NAME provided, getting it from token")
                PROJECT_NAME = self.idm.getProjectNameFromToken(
                    SERVICE_USER_TOKEN,
                    DOMAIN_ID,
                    PROJECT_ID)

            logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
            logger.debug("PROJECT_NAME=%s" % PROJECT_NAME)
            logger.debug("SERVICE_USER_TOKEN=%s" % SERVICE_USER_TOKEN)


            if not PROJECT_ID:
                PROJECT_ID = self.idm.getProjectId(SERVICE_USER_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)


            # TODO: Search for subscriptions about: STH, CKAN, CYGNUS, CEP

            cb_res = self.cb.getListSubscriptions(
                SERVICE_USER_TOKEN,
                DOMAIN_NAME,
                PROJECT_NAME
            )
            modules = []
            for sub in cb_res:
                if sub["notification"]["callback"].startswith(self.sth_endpoint):
                    modules.append({"module": "sth"})
                if sub["notification"]["callback"].startswith(self.cygnus_endpoint):
                    modules.append({"module": "cygnus"})
                if sub["notification"]["callback"].startswith(self.cep_endpoint):
                    modules.append({"module": "cep"})

            logger.debug("modules=%s" % modules)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        return modules
