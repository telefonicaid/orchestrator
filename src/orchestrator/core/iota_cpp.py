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
import os
import logging

from orchestrator.common.util import RestOperations
from orchestrator.core.iota import IoTAOperations

logger = logging.getLogger('orchestrator_core')

class IoTACppOperations(object):
    '''
       IoT platform: IoTAgent
    '''

    def __init__(self,
                 IOTA_PROTOCOL=None,
                 IOTA_HOST=None,
                 IOTA_PORT=None):

        self.IOTA_PROTOCOL = IOTA_PROTOCOL
        self.IOTA_HOST = IOTA_HOST
        self.IOTA_PORT = IOTA_PORT

        self.IoTACppRestOperations = RestOperations(IOTA_PROTOCOL,
                                                    IOTA_HOST,
                                                    IOTA_PORT)

    def checkIoTA(self):
        res = self.IoTACppRestOperations.rest_request(
            url='/iot/',
            method='GET',
            data=None)
        assert res.code == 404, (res.code, res.msg)
        pass


    def registerService(self,
                        SERVICE_USER_TOKEN,
                        SERVICE_NAME,
                        SUBSERVICE_NAME,
                        PROTOCOL,
                        ENTITY_TYPE,
                        APIKEY,
                        TRUSTTOKENID,
                        CBROKER_ENDPOINT,
                        MAPPING_ATTRIBUTES=[],
                        STATIC_ATTRIBUTES=[]):
        body_data = {
            services : [
                {
                    "protocol": [PROTOCOL],
                    "entity_type": ENTITY_TYPE,
                    "apikey": APIKEY,
                    "token": TRUSTOKENID,
                    "cbroker": CBROKER_ENDPOINT,
                    "attributes": MAPPING_ATTRIBUTES,
                    "static_attributes": STATIC_ATTRIBUTES,
                }
            ]
        }

        logger.debug("POST to iot/services with: %s" % json.dumps(body_data,
                                                                  indent=3))

        res = self.IoTACppRestOperations.rest_request(
            url='/iot/services',
            method='POST',
            data=body_data,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def getServices(self,
                    SERVICE_USER_TOKEN,
                    SERVICE_NAME,
                    SUBSERVICE_NAME):

        logger.debug("GET to iot/services ")

        res = self.IoTACppRestOperations.rest_request(
            url='/iot/services',
            method='GET',
            data=None,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def registerDevice(self,
                       SERVICE_USER_TOKEN,
                       SERVICE_NAME,
                       SUBSERVICE_NAME,
                       DEVICE_ID,
                       PROTOCOL,
                       ENTITY_NAME,
                       ENTITY_TYPE,
                       TIMEZONE,
                       ATTRIBUTES=[],
                       STATIC_ATTRIBUTES=[],
                       COMMANDS=[],
                       INTERNAL_ATTRIBUTES=[],
                       LAZY=[]):

        body_data = {
            "devices": [
                {
                    "device_id": DEVICE_ID,
                    "protocol": PROTOCOL,
                    "service": SERVICE_NAME,
                    "service_path": SUBSERVICE_NAME,
                    "entity_name": ENTITY_NAME,
                    "entity_type": ENTITY_TYPE,
                    "timezone": TIMEZONE,
                    "attributes": ATTRIBUTES,
                    "static_attributes": STATIC_ATTRIBUTES,
                    "commands": COMMANDS,
                    "internal_attributes": INTERNAL_ATTRIBUTES,
                    "lazy": LAZY
                }
            ]
        }

        logger.debug("POST to iot/devices with: %s" % json.dumps(body_data,
                                                                 indent=3))

        res = self.IoTACppRestOperations.rest_request(
            url='/iot/devices',
            method='POST',
            data=body_data,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 201, (res.code, res.msg)

        # TODO get Location ?
        # TODO return something?
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def getDevices(self,
                   SERVICE_USER_TOKEN,
                   SERVICE_NAME,
                   SUBSERVICE_NAME):

        logger.debug("GET to iot/devices")

        res = self.IoTACppRestOperations.rest_request(
            url='/iot/devices',
            method='GET',
            data=None,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 200, (res.code, res.msg)

        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def unregisterDevice(self,
                         SERVICE_USER_TOKEN,
                         SERVICE_NAME,
                         SUBSERVICE_NAME,
                         DEVICE_ID):

        logger.debug("DELETE to iot/devices with: %s" % DEVICE_ID)

        res = self.IoTACppRestOperations.rest_request(
            url='/iot/devices/%s' % DEVICE_ID,
            method='DELETE',
            data=None,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 204, (res.code, res.msg)


    def deleteAllDevices(self,
                         SERVICE_USER_TOKEN,
                         SERVICE_NAME,
                         SUBSERVICE_NAME=""):
        #
        # 1. Get devices
        #
        devices_deleted = []

        logger.debug("Getting devices for %s %s" % (SERVICE_NAME,
                                                    SUBSERVICE_NAME))
        try:
            devices = self.getDevices(SERVICE_USER_TOKEN,
                                      SERVICE_NAME,
                                      SUBSERVICE_NAME)
            # Check devices returned: IOTA returns devices into dict before some versions
            if 'devices' in devices:
                devices = devices['devices']
        except Exception, ex:
            logger.error("%s trying getDevices from IOTA: %s/%s" % (ex,
                                                            SERVICE_NAME,
                                                            SUBSERVICE_NAME))
            return devices_deleted

        for device in devices:
            #
            # 2. Unregister each device
            #
            # Get device_id: IOTA returns device_id in a field depending on version
            device_id = None
            if 'device_id' in device:
                device_id = device['device_id']
            if 'id' in device:
                device_id = device['id']

            logger.debug("Unregistering device: %s" % device_id)
            try:
                self.unregisterDevice(SERVICE_USER_TOKEN,
                                      SERVICE_NAME,
                                      SUBSERVICE_NAME,
                                      device_id)
                devices_deleted.append(device_id)
            except Exception, ex:
                logger.error("%s trying to unregister device: %s" % (ex,
                                                            device_id))

        return devices_deleted
