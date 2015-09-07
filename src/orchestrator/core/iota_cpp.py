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

from orchestrator.common.util import RestOperations
from orchestrator.core.iota import IoTAOperations

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

        res = self.IoTACppRestOperations.rest_request(
            url='/iot/services',
            method='POST',
            data=body_data,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 201, (res.code, res.msg)


    def registerDevice(self,
                       SERVICE_USER_TOKEN,
                       SERVICE_NAME,
                       SUBSERVICE_NAME,
                       DEVICE_ID,
                       #PROTOCOL,
                       #RESOURCE,
                       ENTITY_NAME,
                       ENTITY_TYPE,
                       TIMEZONE,
                       LAZY):

        # TODO: Cpp IoTA and Node IoTA are going to converge with the same payload/args
        body_data = {
            "devices": [
                {
                     # resource: ???
                     # service: client_a
                     # service_path: /some_area
                     # entity_name: <device_id> XXX
                     # entity_type: button
                     # timeozne: America/Santiago
                     # lazy: lazy_op_status: string
                    "device_id": DEVICE_ID,
                    "entity_name": ENTITY_NAME,
                    "entity_type": ENTITY_TYPE,
                    "timezone": TIMEZONE,
                    # "attributes": [
                    #     {
                    #         "object_id": "source_data",
                    #         "name": "attr_name",
                    #         "type": "int"
                    #     }
                    # ],
                    # "static_attributes": [
                    #     {
                    #         "name": "att_name",
                    #         "type": "string",
                    #         "value": "value"
                    #     }
                    # ],
                    "lazy": LAZY
                }
            ]
        }

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
