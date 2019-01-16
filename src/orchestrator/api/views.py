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
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

from django.conf import settings
from datetime import datetime

from orchestrator.core.flow.createNewService import CreateNewService
from orchestrator.core.flow.createNewSubService import CreateNewSubService
from orchestrator.core.flow.createNewServiceUser import CreateNewServiceUser
from orchestrator.core.flow.createNewServiceRole import CreateNewServiceRole
from orchestrator.core.flow.createTrustToken import CreateTrustToken
from orchestrator.core.flow.removeUser import RemoveUser
from orchestrator.core.flow.updateUser import UpdateUser
from orchestrator.core.flow.Domains import Domains
from orchestrator.core.flow.Projects import Projects
from orchestrator.core.flow.Roles import Roles
from orchestrator.core.flow.Users import Users
from orchestrator.core.flow.Groups import Groups
from orchestrator.api import parsers


from orchestrator.common.util import ContextFilterCorrelatorId
from orchestrator.common.util import ContextFilterTransactionId
from orchestrator.common.util import ContextFilterService
from orchestrator.common.util import ContextFilterSubService

from orchestrator.api.iotconf import IoTConf
from orchestrator.api.stats import Stats

logger = logging.getLogger('orchestrator_api')
logger.addFilter(ContextFilterCorrelatorId("n/a"))
logger.addFilter(ContextFilterTransactionId("n/a"))
logger.addFilter(ContextFilterService("None"))
logger.addFilter(ContextFilterSubService(""))







class ServiceList_RESTView(APIView, IoTConf):
    """
    { Read, Update, Delete } Service

    """
    schema_name = "ServiceList"
    parser_classes = (parsers.JSONSchemaParser,)


    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id=None):
        self.schema_name = "ServiceList"
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            if not service_id:
                # Get all domains
                result, service_name, subservice_name = flow.domains(
                    request.data.get("DOMAIN_NAME", None),
                    request.data.get("SERVICE_ADMIN_USER", None),
                    request.data.get("SERVICE_ADMIN_PASSWORD", None),
                    request.data.get("SERVICE_ADMIN_TOKEN",
                                     HTTP_X_AUTH_TOKEN))
            else:
                # Get detail of one domains
                result, service_name, subservice_name = flow.get_domain(
                    request.data.get("DOMAIN_ID", service_id),
                    request.data.get("DOMAIN_NAME", None),
                    request.data.get("SERVICE_ADMIN_USER", None),
                    request.data.get("SERVICE_ADMIN_PASSWORD", None),
                    request.data.get("SERVICE_ADMIN_TOKEN",
                                     HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                Stats.num_get_service += 1
                response = Response(result, status=status.HTTP_200_OK,
                                    headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


    def put(self, request, service_id=None):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "ServiceList"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data # json validation
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.update_domain(
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("NEW_SERVICE_DESCRIPTION", None))
            if 'error' not in result:
                Stats.num_put_service += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def delete(self, request, service_id=None):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "ServiceList"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           self.KEYPASS_PROTOCOL,
                           self.KEYPASS_HOST,
                           self.KEYPASS_PORT,
                           self.ORION_PROTOCOL,
                           self.ORION_HOST,
                           self.ORION_PORT,
                           self.PERSEO_PROTOCOL,
                           self.PERSEO_HOST,
                           self.PERSEO_PORT,
                           MONGODB_URI=self.MONGODB_URI,
                           TRANSACTION_ID=None,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.delete_domain(
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                Stats.num_delete_service += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

class ServiceCreate_RESTView(ServiceList_RESTView):
    """
    { Create } Service

    """

    schema_name = "ServiceCreate"

    def __init__(self):
        ServiceList_RESTView.__init__(self)

    def post(self, request, *args, **kw):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = CreateNewService(self.KEYSTONE_PROTOCOL,
                                    self.KEYSTONE_HOST,
                                    self.KEYSTONE_PORT,
                                    self.KEYPASS_PROTOCOL,
                                    self.KEYPASS_HOST,
                                    self.KEYPASS_PORT,
                                    MONGODB_URI=self.MONGODB_URI,
                                    TRANSACTION_ID=None,
                                    CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.createNewService(
                request.data.get("DOMAIN_NAME", None),
                request.data.get("DOMAIN_ADMIN_USER", None),
                request.data.get("DOMAIN_ADMIN_PASSWORD", None),
                request.data.get("DOMAIN_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.data.get("NEW_SERVICE_NAME"),
                request.data.get("NEW_SERVICE_DESCRIPTION"),
                request.data.get("NEW_SERVICE_ADMIN_USER"),
                request.data.get("NEW_SERVICE_ADMIN_PASSWORD"),
                request.data.get("NEW_SERVICE_ADMIN_EMAIL", None))
            if 'token' in result:
                Stats.num_post_service += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class SubServiceList_RESTView(APIView, IoTConf):
    """
    { Read, Modify, Delete } SubService

    """
    schema_name = "SubServiceList"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id=None, subservice_id=None):
        self.schema_name = "SubServiceList"
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            if service_id:
                if not subservice_id:
                    result, service_name, subservice_name = flow.projects(
                        service_id,
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN))
                else:
                    # Get detail of subservice
                    result, service_name, subservice_name = flow.get_project(
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SUBSERVICE_ID", subservice_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN))
            else:
                # Really service_id is not mandatory already in urls?
                result = {'error':  "ERROR not service_id provided",
                          "code": "400"}

            if 'error' not in result:
                Stats.num_get_subservice += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def put(self, request, service_id=None, subservice_id=None):
        self.schema_name = "SubServiceList"
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            # request.data # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            if service_id:
                if subservice_id:
                    result, service_name, subservice_name = flow.update_project(
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SUBSERVICE_ID", subservice_id),
                        request.data.get("SUBSERVICE_NAME", None),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("NEW_SUBSERVICE_DESCRIPTION", None))
            else:
                # Really service_id is not mandatory already in urls?
                result['error'] = "ERROR not service_id provided"

            if 'error' not in result:
                Stats.num_put_subservice += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def delete(self, request, service_id=None, subservice_id=None):
        self.schema_name = "SubServiceList"
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            # request.data # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            self.KEYPASS_PROTOCOL,
                            self.KEYPASS_HOST,
                            self.KEYPASS_PORT,
                            self.ORION_PROTOCOL,
                            self.ORION_HOST,
                            self.ORION_PORT,
                            self.PERSEO_PROTOCOL,
                            self.PERSEO_HOST,
                            self.PERSEO_PORT,
                            CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            if service_id:
                    result, service_name, subservice_name = flow.delete_project(
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SUBSERVICE_ID", subservice_id),
                        request.data.get("SUBSERVICE_NAME", None),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN))
            else:
                # Really service_id is not mandatory already in urls?
                result['error'] = "ERROR not service_id provided"

            if 'error' not in result:
                Stats.num_delete_subservice += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class SubServiceCreate_RESTView(SubServiceList_RESTView):
    """
    { Create } SubService
    """
    schema_name = "SubServiceCreate"

    def __init__(self):
        SubServiceList_RESTView.__init__(self)

    def post(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = CreateNewSubService(self.KEYSTONE_PROTOCOL,
                                       self.KEYSTONE_HOST,
                                       self.KEYSTONE_PORT,
                                       None,
                                       None,
                                       None,
                                       self.ORION_PROTOCOL,
                                       self.ORION_HOST,
                                       self.ORION_PORT,
                                       CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            result, service_name, subservice_name = flow.createNewSubService(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.data.get("NEW_SUBSERVICE_NAME", None),
                request.data.get("NEW_SUBSERVICE_DESCRIPTION", None),
                request.data.get("NEW_SUBSERVICE_ADMIN_USER", None),
                request.data.get("NEW_SUBSERVICE_ADMIN_PASSWORD", None),
                request.data.get("NEW_SUBSERVICE_ADMIN_EMAIL", None)
                )

            if 'id' in result and ('error' not in result):
                Stats.num_post_subservice += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

class User_RESTView(APIView, IoTConf):
    """
    { Read, Update, Delete } Users

    """
    schema_name = "User"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def delete(self, request, service_id, user_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = RemoveUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT,
                              CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.removeUser(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("USER_NAME", None),
                request.data.get("USER_ID", user_id))
            if 'error' not in result:
                Stats.num_delete_user += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def put(self, request, service_id, user_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = UpdateUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT,
                              CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.updateUser(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("USER_NAME", None),
                request.data.get("USER_ID", user_id),
                request.data.get("USER_DATA_VALUE"))
            if 'error' not in result:
                Stats.num_put_user += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                Stats.num_flow_errors += 1
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            Stats.num_api_errors += 1
            response = Response(
                'Input validation error - {0}'.format(error.message),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response

    def get(self, request, service_id, user_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Users(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.user(
                               request.data.get("SERVICE_ID",  service_id),
                               request.data.get("SERVICE_NAME", None),
                               request.data.get("USER_ID", user_id),
                               request.data.get("SERVICE_ADMIN_USER", None),
                               request.data.get("SERVICE_ADMIN_PASSWORD", None),
                               request.data.get("SERVICE_ADMIN_TOKEN",
                                                HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                Stats.num_get_user += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def post(self, request, service_id, user_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = UpdateUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT,
                              CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.changeUserPassword(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("USER_ID", user_id),
                request.data.get("SERVICE_USER_NAME", None),
                request.data.get("SERVICE_USER_PASSWORD", None),
                request.data.get("SERVICE_USER_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.data.get("NEW_USER_PASSWORD", None),
                )
            if 'error' not in result:
                Stats.num_post_user += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class UserList_RESTView(APIView, IoTConf):
    """
    { Read, Create } Users into a Service

    """
    schema_name = "UserList"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        index = request.GET.get('index', None)
        count = request.GET.get('count', None)

        try:
            request.data  # json validation
            flow = Users(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.users(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("START_INDEX", index),
                request.data.get("COUNT", count))

            if 'error' not in result:
                Stats.num_get_userlist += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def post(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = CreateNewServiceUser(self.KEYSTONE_PROTOCOL,
                                        self.KEYSTONE_HOST,
                                        self.KEYSTONE_PORT,
                                        CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.createNewServiceUser(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.data.get("NEW_SERVICE_USER_NAME", None),
                request.data.get("NEW_SERVICE_USER_PASSWORD", None),
                request.data.get("NEW_SERVICE_USER_EMAIL", None),
                request.data.get("NEW_SERVICE_USER_DESCRIPTION", None))
            if 'id' in result:
                Stats.num_post_userlist += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class Group_RESTView(APIView, IoTConf):
    """
    { Read, Update, Delete } Groups

    """
    schema_name = "Group"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def delete(self, request, service_id, group_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Groups(self.KEYSTONE_PROTOCOL,
                          self.KEYSTONE_HOST,
                          self.KEYSTONE_PORT,
                          CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.removeGroup(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("GROUP_NAME", None),
                request.data.get("GROUP_ID", group_id))
            if 'error' not in result:
                Stats.num_delete_group += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def put(self, request, service_id, group_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Groups(self.KEYSTONE_PROTOCOL,
                          self.KEYSTONE_HOST,
                          self.KEYSTONE_PORT,
                          CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.updateGroup(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("GROUP_NAME", None),
                request.data.get("GROUP_ID", group_id))
            if 'error' not in result:
                Stats.num_put_group += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                Stats.num_flow_errors += 1
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            Stats.num_api_errors += 1
            response = Response(
                'Input validation error - {0}'.format(error.message),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response

    def get(self, request, service_id, group_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Groups(self.KEYSTONE_PROTOCOL,
                          self.KEYSTONE_HOST,
                          self.KEYSTONE_PORT,
                          CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.group(
                                request.data.get("SERVICE_ID",  service_id),
                                request.data.get("SERVICE_NAME",  None),
                                request.data.get("GROUP_ID", group_id),
                                request.data.get("SERVICE_ADMIN_USER", None),
                                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                                request.data.get("SERVICE_ADMIN_TOKEN",
                                                 HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                Stats.num_get_group += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class GroupList_RESTView(APIView, IoTConf):
    """
    { Read, Create } Groups into a Service

    """
    schema_name = "GroupList"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        index = request.GET.get('index', None)
        count = request.GET.get('count', None)

        try:
            request.data  # json validation
            flow = Groups(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.groups(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("START_INDEX", index),
                request.data.get("COUNT", count))

            if 'error' not in result:
                Stats.num_get_grouplist += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def post(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Groups(self.KEYSTONE_PROTOCOL,
                          self.KEYSTONE_HOST,
                          self.KEYSTONE_PORT,
                          CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.createNewServiceGroup(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.data.get("NEW_SERVICE_GROUP_NAME", None),
                request.data.get("NEW_SERVICE_GROUP_DESCRIPTION", None))
            if 'id' in result:
                Stats.num_post_grouplist += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class Role_RESTView(APIView, IoTConf):
    """
    { Create, Read, Delete } Roles in a Service

    """
    schema_name = "Role"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id, role_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation

            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           self.KEYPASS_PROTOCOL,
                           self.KEYPASS_HOST,
                           self.KEYPASS_PORT,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.getDomainRolePolicies(
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("ROLE_NAME", None),
                request.data.get("ROLE_ID", role_id))

            if 'error' not in result:
                Stats.num_get_role_policies += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


    def post(self, request, service_id, role_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation

            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         self.KEYPASS_PROTOCOL,
                         self.KEYPASS_HOST,
                         self.KEYPASS_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            result, service_name, subservice_name = flow.setPolicyRole(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("ROLE_NAME", None),
                request.data.get("ROLE_ID", role_id),
                request.data.get("POLICY_FILE_NAME", None),
            )

            if 'error' not in result:
                Stats.num_post_role_policies += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def delete(self, request, service_id, role_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         self.KEYPASS_PROTOCOL,
                         self.KEYPASS_HOST,
                         self.KEYPASS_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            result, service_name, subservice_name = flow.removeRole(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("ROLE_NAME", None),
                request.data.get("ROLE_ID", role_id))

            if 'error' not in result:
                Stats.num_delete_role += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class RolePolicy_RESTView(APIView, IoTConf):
    """
    { Delete, Read } Role Policies in a Service

    """
    schema_name = "Role"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)


    def get(self, request, service_id, role_id, policy_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         self.KEYPASS_PROTOCOL,
                         self.KEYPASS_HOST,
                         self.KEYPASS_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            result, service_name, subservice_name = flow.getPolicyFromRole(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("ROLE_NAME", None),
                request.data.get("ROLE_ID", role_id),
                request.data.get("POLICY_NAME", policy_id))

            if 'error' not in result:
                Stats.num_get_policy_from_role += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def delete(self, request, service_id, role_id, policy_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         self.KEYPASS_PROTOCOL,
                         self.KEYPASS_HOST,
                         self.KEYPASS_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            result, service_name, subservice_name = flow.removePolicyFromRole(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("ROLE_NAME", None),
                request.data.get("ROLE_ID", role_id),
                request.data.get("POLICY_NAME", policy_id))

            if 'error' not in result:
                Stats.num_delete_policy_from_role += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class RoleList_RESTView(APIView, IoTConf):
    """
    { Create, Read } Role into a Service

    """
    schema_name = "RoleList"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "RoleList"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = CreateNewServiceRole(self.KEYSTONE_PROTOCOL,
                                        self.KEYSTONE_HOST,
                                        self.KEYSTONE_PORT,
                                        CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.createNewServiceRole(
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("NEW_ROLE_NAME", None),
                request.data.get("XACML_POLICY", None))
            if 'error' not in result:
                Stats.num_post_role += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def get(self, request, service_id=None):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "RoleAssignmentList"  # Like that scheme!
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        index = request.GET.get('index', None)
        count = request.GET.get('count', None)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.roles(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("START_INDEX", index),
                request.data.get("COUNT", count))

            if 'error' not in result:
                Stats.num_get_role += 1
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class AssignRoleUser_RESTView(APIView, IoTConf):
    """
   { Read, Update, Delete} User Role Assignments in a Service or Subservice

    """
    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "RoleAssignmentList"
        user_id = request.GET.get('user_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        effective = request.GET.get('effective', False) == "true"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)

        try:
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.roles_assignments(
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_NAME",None),
                request.data.get("SUBSERVICE_ID", subservice_id),
                request.data.get("SUBSERVICE_NAME", None),
                request.data.get("ROLE_ID", role_id),
                request.data.get("ROLE_NAME", None),
                request.data.get("USER_ID", user_id),
                request.data.get("USER_NAME", None),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("EFFECTIVE", effective))

            if 'error' not in result:
                Stats.num_get_roleassignment += 1
                response = Response(result, status=status.HTTP_200_OK,
                            headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def post(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        user_id = request.GET.get('user_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.data.get('INHERIT', False) is True)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            if not (request.data.get("SUBSERVICE_NAME", None) or
                    request.data.get("SUBSERVICE_ID", subservice_id)):
                if inherit:
                    result, service_name, subservice_name = flow.assignInheritRoleServiceUser(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME", None),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_USER_NAME", None),
                        request.data.get("SERVICE_USER_ID", user_id))
                else:
                    result, service_name, subservice_name = flow.assignRoleServiceUser(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME", None),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_USER_NAME", None),
                        request.data.get("SERVICE_USER_ID", user_id))
            else:
                result, service_name, subservice_name = flow.assignRoleSubServiceUser(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME", None),
                    request.data.get("SUBSERVICE_ID", subservice_id),
                    request.data.get("SERVICE_ADMIN_USER", None),
                    request.data.get("SERVICE_ADMIN_PASSWORD", None),
                    request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("ROLE_NAME", None),
                    request.data.get("ROLE_ID", role_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_ID", user_id))
            if 'error' not in result:
                Stats.num_post_roleassignment += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def delete(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        user_id = request.GET.get('user_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.data.get('INHERIT', False) is True)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            if not (request.data.get("SUBSERVICE_NAME", None) or
                    request.data.get("SUBSERVICE_ID", subservice_id)):
                if inherit:
                    result, service_name, subservice_name = flow.revokeInheritRoleServiceUser(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME"),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_USER_NAME", None),
                        request.data.get("SERVICE_USER_ID", user_id))
                else:
                    result, service_name, subservice_name = flow.revokeRoleServiceUser(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME"),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_USER_NAME", None),
                        request.data.get("SERVICE_USER_ID", user_id))
            else:
                result, service_name, subservice_name = flow.revokeRoleSubServiceUser(
                    request.data.get("SERVICE_NAME"),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME"),
                    request.data.get("SUBSERVICE_ID", subservice_id),
                    request.data.get("SERVICE_ADMIN_USER", None),
                    request.data.get("SERVICE_ADMIN_PASSWORD", None),
                    request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("ROLE_NAME", None),
                    request.data.get("ROLE_ID", role_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_ID", user_id))
            if 'error' not in result:
                Stats.num_delete_roleassignment += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class AssignRoleGroup_RESTView(APIView, IoTConf):
    """
   { Read, Update, Delete} Group Role Assignments in a Service or Subservice

    """
    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "RoleAssignmentList"
        group_id = request.GET.get('group_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        effective = request.GET.get('effective', False) == "true"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)

        try:
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.roles_assignments_groups(
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SERVICE_NAME",None),
                request.data.get("SUBSERVICE_ID", subservice_id),
                request.data.get("SUBSERVICE_NAME", None),
                request.data.get("ROLE_ID", role_id),
                request.data.get("ROLE_NAME", None),
                request.data.get("GROUP_ID", group_id),
                request.data.get("GROUP_NAME", None),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("EFFECTIVE", effective))

            if 'error' not in result:
                Stats.num_get_roleassignment += 1
                response = Response(result, status=status.HTTP_200_OK,
                            headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def post(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        group_id = request.GET.get('group_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.data.get('INHERIT', False) is True)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            if not (request.data.get("SUBSERVICE_NAME", None) or
                    request.data.get("SUBSERVICE_ID", subservice_id)):
                if inherit:
                    result, service_name, subservice_name = flow.assignInheritRoleServiceGroup(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME", None),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_GROUP_NAME", None),
                        request.data.get("SERVICE_GROUP_ID", group_id))
                else:
                    result, service_name, subservice_name = flow.assignRoleServiceGroup(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME", None),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_GROUP_NAME", None),
                        request.data.get("SERVICE_GROUP_ID", group_id))
            else:
                result, service_name, subservice_name = flow.assignRoleSubServiceGroup(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME", None),
                    request.data.get("SUBSERVICE_ID", subservice_id),
                    request.data.get("SERVICE_ADMIN_USER", None),
                    request.data.get("SERVICE_ADMIN_PASSWORD", None),
                    request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("ROLE_NAME", None),
                    request.data.get("ROLE_ID", role_id),
                    request.data.get("SERVICE_GROUP_NAME", None),
                    request.data.get("SERVICE_GROUP_ID", group_id))
            if 'error' not in result:
                Stats.num_post_roleassignment += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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

    def delete(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        group_id = request.GET.get('group_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.data.get('INHERIT', False) is True)
        try:
            request.data  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            if not (request.data.get("SUBSERVICE_NAME", None) or
                    request.data.get("SUBSERVICE_ID", subservice_id)):
                if inherit:
                    result, service_name, subservice_name = flow.revokeInheritRoleServiceGroup(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME"),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_GROUP_NAME", None),
                        request.data.get("SERVICE_GROUP_ID", group_id))
                else:
                    result, service_name, subservice_name = flow.revokeRoleServiceGroup(
                        request.data.get("SERVICE_NAME", None),
                        request.data.get("SERVICE_ID", service_id),
                        request.data.get("SERVICE_ADMIN_USER", None),
                        request.data.get("SERVICE_ADMIN_PASSWORD", None),
                        request.data.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.data.get("ROLE_NAME"),
                        request.data.get("ROLE_ID", role_id),
                        request.data.get("SERVICE_GROUP_NAME", None),
                        request.data.get("SERVICE_GROUP_ID", group_id))
            else:
                result, service_name, subservice_name = flow.revokeRoleSubServiceGroup(
                    request.data.get("SERVICE_NAME"),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME"),
                    request.data.get("SUBSERVICE_ID", subservice_id),
                    request.data.get("SERVICE_ADMIN_USER", None),
                    request.data.get("SERVICE_ADMIN_PASSWORD", None),
                    request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("ROLE_NAME", None),
                    request.data.get("ROLE_ID", role_id),
                    request.data.get("SERVICE_GROUP_NAME", None),
                    request.data.get("SERVICE_GROUP_ID", group_id))
            if 'error' not in result:
                Stats.num_delete_roleassignment += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class Trust_RESTView(APIView, IoTConf):
    """
    { Creates }  a Trust Token

    """
    schema_name = "Trust"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = CreateTrustToken(self.KEYSTONE_PROTOCOL,
                                    self.KEYSTONE_HOST,
                                    self.KEYSTONE_PORT,
                                    CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.createTrustToken(
                request.data.get("SERVICE_NAME", None),
                request.data.get("SERVICE_ID", service_id),
                request.data.get("SUBSERVICE_NAME", None),
                request.data.get("SUBSERVICE_ID", None),
                request.data.get("SERVICE_ADMIN_USER", None),
                request.data.get("SERVICE_ADMIN_PASSWORD", None),
                request.data.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.data.get("ROLE_NAME", None),
                request.data.get("ROLE_ID", None),
                request.data.get("TRUSTEE_USER_NAME", None),
                request.data.get("TRUSTEE_USER_ID", None),
                request.data.get("TRUSTOR_USER_NAME", None),
                request.data.get("TRUSTOR_USER_ID", None)
            )
            if 'error' not in result:
                Stats.num_post_trust += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class IOTModuleActivation_RESTView(APIView, IoTConf):
    """
    { Create, Read, Delete } IOT Module Activation

    """
    schema_name = "IOTModuleActivation"
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
                flow = Domains(self.KEYSTONE_PROTOCOL,
                               self.KEYSTONE_HOST,
                               self.KEYSTONE_PORT,
                               None,
                               None,
                               None,
                               self.ORION_PROTOCOL,
                               self.ORION_HOST,
                               self.ORION_PORT,
                               self.PERSEO_PROTOCOL,
                               self.PERSEO_HOST,
                               self.PERSEO_PORT,
                               CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                modules, service_name, subservice_name = flow.list_activated_modules(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN)
                )
            else:
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.PERSEO_PROTOCOL,
                                self.PERSEO_HOST,
                                self.PERSEO_PORT,
                                CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                modules, service_name, subservice_name = flow.list_activated_modules(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME", None),
                    request.data.get("SUBSERVICE_ID",  subservice_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN)
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

    def post(self, request, service_id, subservice_id=None, iot_module=None):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            if not subservice_id:
                flow = Domains(self.KEYSTONE_PROTOCOL,
                               self.KEYSTONE_HOST,
                               self.KEYSTONE_PORT,
                               None,
                               None,
                               None,
                               self.ORION_PROTOCOL,
                               self.ORION_HOST,
                               self.ORION_PORT,
                               self.PERSEO_PROTOCOL,
                               self.PERSEO_HOST,
                               self.PERSEO_PORT,
                               CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                sub, service_name, subservice_name = flow.activate_module(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("IOTMODULE", iot_module),
                )
            else:
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.PERSEO_PROTOCOL,
                                self.PERSEO_HOST,
                                self.PERSEO_PORT,
                                CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                sub, service_name, subservice_name = flow.activate_module(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME", None),
                    request.data.get("SUBSERVICE_ID",  subservice_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("IOTMODULE", iot_module),
                )
            result = {}
            result['subscriptionid'] = sub
            if 'error' not in result:
                Stats.num_post_module_activation += 1
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


    def delete(self, request, service_id, subservice_id=None, iot_module=None):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            if not subservice_id:
                flow = Domains(self.KEYSTONE_PROTOCOL,
                               self.KEYSTONE_HOST,
                               self.KEYSTONE_PORT,
                               None,
                               None,
                               None,
                               self.ORION_PROTOCOL,
                               self.ORION_HOST,
                               self.ORION_PORT,
                               self.PERSEO_PROTOCOL,
                               self.PERSEO_HOST,
                               self.PERSEO_PORT,
                               CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                result, service_name, subservice_name = flow.deactivate_module(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("IOTMODULE", iot_module),
                )
            else:
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.PERSEO_PROTOCOL,
                                self.PERSEO_HOST,
                                self.PERSEO_PORT,
                                CORRELATOR_ID=CORRELATOR_ID)
                CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
                result, service_name, subservice_name = flow.deactivate_module(
                    request.data.get("SERVICE_NAME", None),
                    request.data.get("SERVICE_ID", service_id),
                    request.data.get("SUBSERVICE_NAME", None),
                    request.data.get("SUBSERVICE_ID",  subservice_id),
                    request.data.get("SERVICE_USER_NAME", None),
                    request.data.get("SERVICE_USER_PASSWORD", None),
                    request.data.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.data.get("IOTMODULE", iot_module),
                )

            if 'error' not in result:
                Stats.num_delete_module_activation += 1
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
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


class OrchVersion_RESTView(APIView, IoTConf):
    """
     { Read } Orchestrator Statistics
    """

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        #HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        try:
            # Extract version and stats data
            result = {
                "version": settings.ORC_VERSION,
                "uptime": str(self.uptime),
                "IoTModules": settings.IOTMODULES,
                "API_stats": {
                    "num_post_service": self.num_post_service,
                    "num_get_service": self.num_get_service,
                    "num_put_service": self.num_put_service,
                    "num_delete_service": self.num_delete_service,

                    "num_post_subservice": self.num_post_subservice,
                    "num_get_subservice": self.num_get_subservice,
                    "num_put_subservice": self.num_put_subservice,
                    "num_delete_subservice": self.num_delete_subservice,

                    "num_delete_user": self.num_delete_user,
                    "num_put_user": self.num_put_user,
                    "num_get_user ": self.num_get_user,
                    "num_post_user": self.num_post_user,

                    "num_get_userlist": self.num_get_userlist,
                    "num_post_userlist": self.num_post_userlist,

                    "num_delete_role": self.num_delete_role,
                    "num_post_role": self.num_post_role,
                    "num_get_role": self.num_get_role,
                    "num_post_role_policies": self.num_post_role_policies,
                    "num_get_role_policies": self.num_get_role_policies,

                    "num_delete_policy_from_role": self.num_delete_policy_from_role,
                    "num_get_policy_from_role": self.num_get_policy_from_role,

                    "num_delete_roleassignment": self.num_delete_roleassignment,
                    "num_post_roleassignment": self.num_post_roleassignment,
                    "num_get_roleassignment": self.num_get_roleassignment,

                    "num_post_trust": self.num_post_trust,

                    "num_post_device": self.num_post_device,
                    "num_delete_device": self.num_delete_device,

                    "num_post_devices": self.num_post_devices,
                    "num_post_entity_service": self.num_post_entity_service,

                    "num_get_module_activation": self.num_get_module_activation,
                    "num_post_module_activation": self.num_post_module_activation,
                    "num_delete_module_activation": self.num_delete_module_activation,

                    "num_update_loglevel": self.num_update_loglevel,

                    "num_api_errors": self.num_api_errors,
                    "num_flow_errors": self.num_flow_errors

                }
            }

            # print it into a trace
            logger.info("Orchestrator statistics: %s" % json.dumps(
                result, indent=3))

            if 'error' not in result:
                response = Response(result, status=status.HTTP_200_OK)
            else:
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            response = Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response


class OrchLogLevel_RESTView(APIView, IoTConf):
    """
     { Update } Orchestrator LogLevel
    """

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)

        try:
            result = {
                "level":
                logging.getLevelName(
                    logging.getLogger('orchestrator_api').getEffectiveLevel())
            }
            response = Response(result, status=status.HTTP_200_OK,
                            headers={"Fiware-Correlator": CORRELATOR_ID})

        except ParseError as error:
            body = {
                "error": "%s" % error.detail
            }
            response = Response(
                json.dumps(body),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response

    def put(self, request):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        HTTP_X_AUTH_TOKEN = self.getXAuthToken(request)
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        logLevel = request.GET.get('level', None)

        try:
            # Check HTTP_X_AUTH_TOKEN: should belongs to default admin domain
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.domains(
                    "admin_domain",
                    request.data.get("SERVICE_ADMIN_USER", None),
                    request.data.get("SERVICE_ADMIN_PASSWORD", None),
                    request.data.get("SERVICE_ADMIN_TOKEN",
                                     HTTP_X_AUTH_TOKEN))

            if 'error' in result:
                raise ParseError(detail="wrong auth provided")
            else:
                result = None

            newLogLevel = logLevel.upper()
            if newLogLevel not in ["FATAL", "CRITICAL", "ERROR", "WARNING",
                                   "INFO", "DEBUG"]:
                raise ParseError(detail="not supported log level")

            LEVELS = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'FATAL': logging.FATAL,
                'CRITICAL': logging.CRITICAL
            }


            # Set loggers level to such log level
            logging.getLogger('django').setLevel(LEVELS[newLogLevel])
            logging.getLogger('django.request').setLevel(LEVELS[newLogLevel])
            logging.getLogger('orchestrator_api').setLevel(LEVELS[newLogLevel])
            logging.getLogger('orchestrator_core').setLevel(LEVELS[newLogLevel])

            # Set also handlers (console and file)) to such log level
            logging.getLogger('orchestrator_api').handlers[0].setLevel(LEVELS[newLogLevel])
            logging.getLogger('orchestrator_api').handlers[1].setLevel(LEVELS[newLogLevel])
            logging.getLogger('orchestrator_core').handlers[0].setLevel(LEVELS[newLogLevel])
            logging.getLogger('orchestrator_core').handlers[1].setLevel(LEVELS[newLogLevel])

            # print it into a trace
            logger.debug("Orchestrator has set logLevel to: %s" % json.dumps(
                logLevel, indent=3))

            Stats.num_update_loglevel += 1
            response = Response(result, status=status.HTTP_200_OK,
                            headers={"Fiware-Correlator": CORRELATOR_ID})


        except ParseError as error:
            body = {
                "error": "%s" % error.detail
            }
            response = Response(
                json.dumps(body),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response

class OrchMetrics_RESTView(APIView, IoTConf):
    """
     { Read, Update } Orchestrator Common Metrics
    """

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        reset = request.GET.get('reset', False) == "true"

        try:
            result = self.composeMetrics()

            if reset:
                self.resetMetrics()

            response = Response(result, status=status.HTTP_200_OK,
                            headers={"Fiware-Correlator": CORRELATOR_ID})

        except ParseError as error:
            body = {
                "error": "%s" % error.detail
            }
            response = Response(
                json.dumps(body),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response

    def delete(self, request):
        service_start = time.time()
        response = service_name = subservice_name = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)

        try:
            result = self.composeMetrics()
            self.resetMetrics()
            response = Response(result, status=status.HTTP_204_NO_CONTENT,
                            headers={"Fiware-Correlator": CORRELATOR_ID})

        except ParseError as error:
            body = {
                "error": "%s" % error.detail
            }
            response = Response(
                json.dumps(body),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        self.collectMetrics(service_start, service_name, subservice_name, request, response, flow)
        return response
