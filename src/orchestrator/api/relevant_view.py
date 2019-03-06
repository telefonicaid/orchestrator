#
# Copyright 2019 Telefonica Espana
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

from django.conf import settings

from orchestrator.core.flow.Relevant import Relevant
from orchestrator.api import parsers
from orchestrator.api.iotconf import IoTConf
from orchestrator.api.stats import Stats

class Relevant_RESTView(APIView, IoTConf):
    """
    { Read } Relevant

    """
    schema_name = "Relevant"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id, subservice_id=None):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            if not subservice_id:
                flow = Relevant(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                SPLUNK_PROTOCOL=self.SPLUNK_PROTOCOL,
                                SPLUNK_HOST=self.SPLUNK_HOST,
                                SPLUNK_PORT=self.SPLUNK_PORT,
                                SPLUNK_USER=self.SPLUNK_USER,
                                SPLUNK_PASSWORD=self.SPLUNK_PASSWORD,
                                CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                relvant, service_name, subservice_name = flow.getRelevant(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("COMPONENT", None)
                )
            else:
                flow = Relevant(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                SPLUNK_PROTOCOL=self.SPLUNK_PROTOCOL,
                                SPLUNK_HOST=self.SPLUNK_HOST,
                                SPLUNK_PORT=self.SPLUNK_PORT,
                                SPLUNK_USER=self.SPLUNK_USER,
                                SPLUNK_PASSWORD=self.SPLUNK_PASSWORD,
                                CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                modules, service_name, subservice_name = flow.getRelevant(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME", None),
                    request.data.get("SUBSERVICE_ID",  subservice_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("COMPONENT", None)                    
                )
            result = {}
            if 'error' not in modules:
                result['actived_modules'] = modules
                Stats.num_get_module_activation += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                result = modules
                Stats.num_flow_errors += 1
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})

        except ParseError as error:
            Stats.num_api_errors += 1
            response = Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response


