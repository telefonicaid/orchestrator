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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.throttling import AnonRateThrottle

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
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
from orchestrator.api import parsers


logger = logging.getLogger('orchestrator_api')


class Stats(object):

    # Start Time
    uptime = datetime.utcnow()

    # All stats
    num_post_service = 0
    num_get_service = 0
    num_put_service = 0
    num_delete_service = 0

    num_post_subservice = 0
    num_get_subservice = 0
    num_put_subservice = 0
    num_delete_subservice = 0

    num_delete_user = 0
    num_put_user = 0
    num_get_user = 0
    num_post_user = 0

    num_get_userlist = 0
    num_post_userlist = 0

    num_delete_role = 0
    num_post_role = 0
    num_get_role = 0

    num_delete_roleassignment = 0
    num_post_roleassignment = 0
    num_get_roleassignment = 0

    num_post_trust = 0

    num_post_device = 0
    num_delete_device = 0

    num_post_devices = 0
    num_post_entity_service = 0

    num_get_module_activation = 0
    num_post_module_activation = 0
    num_delete_module_activation = 0

    num_api_errors = 0
    num_flow_errors = 0



class IoTConf(Stats):
    throttle_classes = (AnonRateThrottle,)

    # Class to extract Keystone/Keypass conf from django settings
    def __init__(self):
        try:
            self.KEYSTONE_PROTOCOL = settings.KEYSTONE['protocol']
            self.KEYSTONE_HOST = settings.KEYSTONE['host']
            self.KEYSTONE_PORT = settings.KEYSTONE['port']

            self.KEYPASS_PROTOCOL = settings.KEYPASS['protocol']
            self.KEYPASS_HOST = settings.KEYPASS['host']
            self.KEYPASS_PORT = settings.KEYPASS['port']

            self.IOTA_PROTOCOL = settings.IOTA['protocol']
            self.IOTA_HOST = settings.IOTA['host']
            self.IOTA_PORT = settings.IOTA['port']

            self.ORION_PROTOCOL = settings.ORION['protocol']
            self.ORION_HOST = settings.ORION['host']
            self.ORION_PORT = settings.ORION['port']

            self.CA_PROTOCOL = settings.CA['protocol']
            self.CA_HOST = settings.CA['host']
            self.CA_PORT = settings.CA['port']

        except KeyError:
            logger.error("keystone / keypass or other endpoint conf error")
            raise ImproperlyConfigured("keystone / Keypass or other endpoint conf")

    # Get Django status error from simple HTTP error code
    def getStatusFromCode(self, code):
        if code == 400:
            rstatus = status.HTTP_400_BAD_REQUEST
        elif code == 401:
            rstatus = status.HTTP_401_UNAUTHORIZED
        elif code == 404:
            rstatus = status.HTTP_404_NOT_FOUND
        elif code == 403:
            rstatus = status.HTTP_403_FORBIDDEN
        elif code == 409:
            rstatus = status.HTTP_409_CONFLICT
        else:
            rstatus = status.HTTP_400_BAD_REQUEST
        return rstatus


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
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT)
            if not service_id:
                # Get all domains
                result = flow.domains(
                    request.DATA.get("DOMAIN_NAME", None),
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN",
                                     HTTP_X_AUTH_TOKEN))
            else:
                # Get detail of one domains
                result = flow.get_domain(
                    request.DATA.get("DOMAIN_ID", service_id),
                    request.DATA.get("DOMAIN_NAME", None),
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN",
                                     HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                Stats.num_get_service += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, service_id=None):
        self.schema_name = "ServiceList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA # json validation
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT)
            result = flow.update_domain(
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("NEW_SERVICE_DESCRIPTION", None))
            if 'error' not in result:
                Stats.num_put_service += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, service_id=None):
        self.schema_name = "ServiceList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           self.KEYPASS_PROTOCOL,
                           self.KEYPASS_HOST,
                           self.KEYPASS_PORT,
                           self.IOTA_PROTOCOL,
                           self.IOTA_HOST,
                           self.IOTA_PORT)
            result = flow.delete_domain(
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                Stats.num_delete_service += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class ServiceCreate_RESTView(ServiceList_RESTView):
    """
    { Create } Service

    """

    schema_name = "ServiceCreate"

    def __init__(self):
        ServiceList_RESTView.__init__(self)

    def post(self, request, *args, **kw):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = CreateNewService(self.KEYSTONE_PROTOCOL,
                                    self.KEYSTONE_HOST,
                                    self.KEYSTONE_PORT,
                                    self.KEYPASS_PROTOCOL,
                                    self.KEYPASS_HOST,
                                    self.KEYPASS_PORT)
            result = flow.createNewService(
                request.DATA.get("DOMAIN_NAME", None),
                request.DATA.get("DOMAIN_ADMIN_USER", None),
                request.DATA.get("DOMAIN_ADMIN_PASSWORD", None),
                request.DATA.get("DOMAIN_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.DATA.get("NEW_SERVICE_NAME"),
                request.DATA.get("NEW_SERVICE_DESCRIPTION"),
                request.DATA.get("NEW_SERVICE_ADMIN_USER"),
                request.DATA.get("NEW_SERVICE_ADMIN_PASSWORD"),
                request.DATA.get("NEW_SERVICE_ADMIN_EMAIL", None))

            if 'token' in result:
                Stats.num_post_service += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


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
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT)
            if service_id:
                if not subservice_id:
                    result = flow.projects(
                        service_id,
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN))
                else:
                    # Get detail of subservice
                    result = flow.get_project(
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SUBSERVICE_ID", subservice_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN))
            else:
                # Really service_id is not mandatory already in urls?
                result = {'error':  "ERROR not service_id provided",
                          "code": "400"}

            if 'error' not in result:
                Stats.num_get_subservice += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, service_id=None, subservice_id=None):

        self.schema_name = "SubServiceList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            # request.DATA # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT)
            if service_id:
                if subservice_id:
                    result = flow.update_project(
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SUBSERVICE_ID", subservice_id),
                        request.DATA.get("SUBSERVICE_NAME", None),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.DATA.get("NEW_SUBSERVICE_DESCRIPTION", None))
            else:
                # Really service_id is not mandatory already in urls?
                result['error'] = "ERROR not service_id provided"

            if 'error' not in result:
                Stats.num_put_subservice += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, service_id=None, subservice_id=None):
        self.schema_name = "SubServiceList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            # request.DATA # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            self.KEYPASS_PROTOCOL,
                            self.KEYPASS_HOST,
                            self.KEYPASS_PORT,
                            self.IOTA_PROTOCOL,
                            self.IOTA_HOST,
                            self.IOTA_PORT)
            if service_id:
                    result = flow.delete_project(
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SUBSERVICE_ID", subservice_id),
                        request.DATA.get("SUBSERVICE_NAME", None),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN))
            else:
                # Really service_id is not mandatory already in urls?
                result['error'] = "ERROR not service_id provided"

            if 'error' not in result:
                Stats.num_delete_subservice += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class SubServiceCreate_RESTView(SubServiceList_RESTView):
    """
    { Create } SubService
    """
    schema_name = "SubServiceCreate"

    def __init__(self):
        SubServiceList_RESTView.__init__(self)

    def post(self, request, service_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = CreateNewSubService(self.KEYSTONE_PROTOCOL,
                                       self.KEYSTONE_HOST,
                                       self.KEYSTONE_PORT,
                                       None,
                                       None,
                                       None,
                                       self.IOTA_PROTOCOL,
                                       self.IOTA_HOST,
                                       self.IOTA_PORT,
                                       self.ORION_PROTOCOL,
                                       self.ORION_HOST,
                                       self.ORION_PORT)

            result = flow.createNewSubService(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.DATA.get("NEW_SUBSERVICE_NAME", None),
                request.DATA.get("NEW_SUBSERVICE_DESCRIPTION", None),
                request.DATA.get("NEW_SUBSERVICE_ADMIN_USER", None),
                request.DATA.get("NEW_SUBSERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("NEW_SUBSERVICE_ADMIN_EMAIL", None)
                )

            # TODO: see optional values for register entity service
            if 'id' in result and request.DATA.get("ENTITY_ID", None):
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.IOTA_PROTOCOL,
                                self.IOTA_HOST,
                                self.IOTA_PORT,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.CA_PROTOCOL,
                                self.CA_HOST,
                                self.CA_PORT
                                )

                result2 = flow.register_service(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("NEW_SUBSERVICE_NAME", None),
                    result['id'],
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("ENTITY_TYPE", None),
                    request.DATA.get("ENTITY_ID", None),
                    request.DATA.get("PROTOCOL", None),
                    request.DATA.get("ATT_NAME", None),
                    request.DATA.get("ATT_PROVIDER", None),
                    request.DATA.get("ATT_ENDPOINT", None),
                    request.DATA.get("ATT_METHOD", None),
                    request.DATA.get("ATT_AUTHENTICATION", None),
                    request.DATA.get("ATT_INTERACTION_TYPE", None),
                    request.DATA.get("ATT_MAPPING", None),
                    request.DATA.get("ATT_TIMEOUT", None)
                    )
                # Accumulate previous result
                if ('error' not in result2):
                    result['subscriptionid_ca'] = result2['subscriptionid_ca']
                    result['subscriptionid_sth'] = result2['subscriptionid_sth']
                    result['subscriptionid_perseo'] = result2['subscriptionid_perseo']
                else:
                    result['error'] = result2['error']

            # TODO: see optional values for register device
            if 'id' in result and request.DATA.get("DEVICE_ID", None):
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.IOTA_PROTOCOL,
                                self.IOTA_HOST,
                                self.IOTA_PORT,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.CA_PROTOCOL,
                                self.CA_HOST,
                                self.CA_PORT)
                result_rd = flow.register_device(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("NEW_SUBSERVICE_NAME", None),
                    result['id'],
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("DEVICE_ID", None),
                    request.DATA.get("ENTITY_TYPE", None),
                    request.DATA.get("ENTITY_NAME", request.DATA.get("DEVICE_ID", None)),
                    request.DATA.get("PROTOCOL", None),
                    request.DATA.get("ATT_ICCID", None),
                    request.DATA.get("ATT_IMEI", None),
                    request.DATA.get("ATT_IMSI", None),
                    request.DATA.get("ATT_INTERACTION_TYPE", None),
                    request.DATA.get("ATT_SERVICE_ID", None),
                    request.DATA.get("ATT_GEOLOCATION", None)
                    )

            if 'id' in result and ('error' not in result):
                Stats.num_post_subservice += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class User_RESTView(APIView, IoTConf):
    """
    { Read, Update, Delete } Users

    """
    schema_name = "User"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def delete(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = RemoveUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)
            result = flow.removeUser(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("USER_NAME", None),
                request.DATA.get("USER_ID", user_id))
            if 'error' not in result:
                Stats.num_delete_user += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = UpdateUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)
            result = flow.updateUser(
                request.DATA.get("SERVICE_NAME"),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("USER_NAME"),
                request.DATA.get("USER_ID", user_id),
                request.DATA.get("USER_DATA_VALUE"))
            if 'error' not in result:
                Stats.num_put_user += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0}'.format(error.message),
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Users(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)
            result = flow.user(request.DATA.get("SERVICE_ID",  service_id),
                               request.DATA.get("USER_ID", user_id),
                               request.DATA.get("SERVICE_ADMIN_USER", None),
                               request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                               request.DATA.get("SERVICE_ADMIN_TOKEN",
                                                HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                Stats.num_get_user += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = UpdateUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)

            result = flow.changeUserPassword(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("USER_ID", user_id),
                request.DATA.get("SERVICE_USER_NAME", None),
                request.DATA.get("SERVICE_USER_PASSWORD", None),
                request.DATA.get("SERVICE_USER_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.DATA.get("NEW_USER_PASSWORD", None),
                )
            if 'error' not in result:
                Stats.num_post_user += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class UserList_RESTView(APIView, IoTConf):
    """
    { Read, Create } Users into a Service

    """
    schema_name = "UserList"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        index = request.GET.get('index', None)
        count = request.GET.get('count', None)

        try:
            request.DATA  # json validation
            flow = Users(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)

            result = flow.users(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("START_INDEX", index),
                request.DATA.get("COUNT", count))

            if 'error' not in result:
                Stats.num_get_userlist += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, service_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = CreateNewServiceUser(self.KEYSTONE_PROTOCOL,
                                        self.KEYSTONE_HOST,
                                        self.KEYSTONE_PORT)
            result = flow.createNewServiceUser(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.DATA.get("NEW_SERVICE_USER_NAME", None),
                request.DATA.get("NEW_SERVICE_USER_PASSWORD", None),
                request.DATA.get("NEW_SERVICE_USER_EMAIL", None),
                request.DATA.get("NEW_SERVICE_USER_DESCRIPTION", None))
            if 'id' in result:
                Stats.num_post_userlist += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class Role_RESTView(APIView, IoTConf):
    """
    { Delete } Roles in a Service

    """
    schema_name = "Role"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id, role_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation

            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           self.KEYPASS_PROTOCOL,
                           self.KEYPASS_HOST,
                           self.KEYPASS_PORT)

            result = flow.getDomainRolePolicies(
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("ROLE_NAME", None),
                request.DATA.get("ROLE_ID", role_id))

            return Response(result, status=status.HTTP_200_OK)

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, service_id, role_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)
            result = flow.removeRole(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("ROLE_NAME", None),
                request.DATA.get("ROLE_ID", role_id))
            if 'error' not in result:
                Stats.num_delete_role += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class RoleList_RESTView(APIView, IoTConf):
    """
    { Create, Read } Role into a Service

    """
    schema_name = "RoleList"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id):
        self.schema_name = "RoleList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = CreateNewServiceRole(self.KEYSTONE_PROTOCOL,
                                        self.KEYSTONE_HOST,
                                        self.KEYSTONE_PORT)
            result = flow.createNewServiceRole(
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("NEW_ROLE_NAME", None),
                request.DATA.get("XACML_POLICY", None))
            if 'error' not in result:
                Stats.num_post_role += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, service_id=None):
        self.schema_name = "RoleAssignmentList"  # Like that scheme!
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        index = request.GET.get('index', None)
        count = request.GET.get('count', None)
        try:
            request.DATA  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)
            result = flow.roles(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("START_INDEX", index),
                request.DATA.get("COUNT", count))

            if 'error' not in result:
                Stats.num_get_role += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class AssignRoleUser_RESTView(APIView, IoTConf):
    """
   { Read, Update, Delete} User Role Assignments in a Service or Subservice

    """
    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        self.schema_name = "RoleAssignmentList"
        user_id = request.GET.get('user_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        effective = request.GET.get('effective', False) == "true"

        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        flow = Roles(self.KEYSTONE_PROTOCOL,
                     self.KEYSTONE_HOST,
                     self.KEYSTONE_PORT)
        result = flow.roles_assignments(
            request.DATA.get("SERVICE_ID", service_id),
            request.DATA.get("SERVICE_NAME",None),
            request.DATA.get("SUBSERVICE_ID", subservice_id),
            request.DATA.get("SUBSERVICE_NAME", None),
            request.DATA.get("ROLE_ID", role_id),
            request.DATA.get("ROLE_NAME", None),
            request.DATA.get("USER_ID", user_id),
            request.DATA.get("USER_NAME", None),
            request.DATA.get("SERVICE_ADMIN_USER", None),
            request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
            request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
            request.DATA.get("EFFECTIVE", effective))

        if 'error' not in result:
            Stats.num_get_roleassignment += 1
            return Response(result, status=status.HTTP_200_OK)
        else:
            Stats.num_flow_errors += 1
            return Response(result['error'],
                            status=self.getStatusFromCode(result['code']))

    def post(self, request, service_id):
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        user_id = request.GET.get('user_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.DATA.get('INHERIT', False) is True)
        try:
            request.DATA  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)

            if not (request.DATA.get("SUBSERVICE_NAME", None) or
                    request.DATA.get("SUBSERVICE_ID", subservice_id)):
                if inherit:
                    result = flow.assignInheritRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME", None),
                        request.DATA.get("ROLE_ID", role_id),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", user_id))
                else:
                    result = flow.assignRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME", None),
                        request.DATA.get("ROLE_ID", role_id),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", user_id))
            else:
                result = flow.assignRoleSubServiceUser(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SUBSERVICE_NAME", None),
                    request.DATA.get("SUBSERVICE_ID", subservice_id),
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("ROLE_NAME", None),
                    request.DATA.get("ROLE_ID", role_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_ID", user_id))
            if 'error' not in result:
                Stats.num_post_roleassignment += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, service_id):
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        user_id = request.GET.get('user_id', None)
        subservice_id = request.GET.get('subservice_id', None)
        role_id = request.GET.get('role_id', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.DATA.get('INHERIT', False) is True)
        try:
            request.DATA  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)

            if not (request.DATA.get("SUBSERVICE_NAME", None) or
                    request.DATA.get("SUBSERVICE_ID", subservice_id)):
                if inherit:
                    result = flow.revokeInheritRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME"),
                        request.DATA.get("ROLE_ID", role_id),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", user_id))
                else:
                    result = flow.revokeRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME"),
                        request.DATA.get("ROLE_ID", role_id),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", user_id))
            else:
                result = flow.revokeRoleSubServiceUser(
                    request.DATA.get("SERVICE_NAME"),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SUBSERVICE_NAME"),
                    request.DATA.get("SUBSERVICE_ID", subservice_id),
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("ROLE_NAME", None),
                    request.DATA.get("ROLE_ID", role_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_ID", user_id))
            if 'error' not in result:
                Stats.num_delete_roleassignment += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class Trust_RESTView(APIView, IoTConf):
    """
    { Creates }  a Trust Token 

    """
    schema_name = "Trust"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = CreateTrustToken(self.KEYSTONE_PROTOCOL,
                                    self.KEYSTONE_HOST,
                                    self.KEYSTONE_PORT)
            result = flow.createTrustToken(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SUBSERVICE_NAME", None),
                request.DATA.get("SUBSERVICE_ID", None),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("ROLE_NAME", None),
                request.DATA.get("ROLE_ID", None),
                request.DATA.get("TRUSTEE_USER_NAME", None),
                request.DATA.get("TRUSTEE_USER_ID", None),
                request.DATA.get("TRUSTOR_USER_NAME", None),
                request.DATA.get("TRUSTOR_USER_ID", None)
            )
            if 'error' not in result:
                Stats.num_post_trust += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class SubServiceIoTADevice_RESTView(APIView, IoTConf):
    """
    { Create, Delete} Device in a Service or a Subservice

    """
    schema_name = "IoTADevice"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id, subservice_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            None,
                            None,
                            None,
                            self.IOTA_PROTOCOL,
                            self.IOTA_HOST,
                            self.IOTA_PORT,
                            self.ORION_PROTOCOL,
                            self.ORION_HOST,
                            self.ORION_PORT,
                            self.CA_PROTOCOL,
                            self.CA_HOST,
                            self.CA_PORT)
            result = flow.register_device(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SUBSERVICE_NAME", None),
                request.DATA.get("SUBSERVICE_ID",  subservice_id),
                request.DATA.get("SERVICE_USER_NAME", None),
                request.DATA.get("SERVICE_USER_PASSWORD", None),
                request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("DEVICE_ID", None),
                request.DATA.get("ENTITY_TYPE", None),
                request.DATA.get("ENTITY_NAME", request.DATA.get("DEVICE_ID", None)),
                request.DATA.get("PROTOCOL", None),
                request.DATA.get("ATT_ICCID", None),
                request.DATA.get("ATT_IMEI", None),
                request.DATA.get("ATT_IMSI", None),
                request.DATA.get("ATT_INTERACTION_TYPE", None),
                request.DATA.get("ATT_SERVICE_ID", None),
                request.DATA.get("ATT_GEOLOCATION", None)
            )
            if 'error' not in result:
                Stats.num_post_device += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, service_id, subservice_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            None,
                            None,
                            None,
                            self.IOTA_PROTOCOL,
                            self.IOTA_HOST,
                            self.IOTA_PORT,
                            self.ORION_PROTOCOL,
                            self.ORION_HOST,
                            self.ORION_PORT,
                            self.CA_PROTOCOL,
                            self.CA_HOST,
                            self.CA_PORT)
            result = flow.unregister_device(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SUBSERVICE_NAME", None),
                request.DATA.get("SUBSERVICE_ID",  subservice_id),
                request.DATA.get("SERVICE_USER_NAME", None),
                request.DATA.get("SERVICE_USER_PASSWORD", None),
                request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("DEVICE_ID", None)
            )
            if 'error' not in result:
                Stats.num_delete_device += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class SubServiceIoTADevices_RESTView(APIView, IoTConf):
    """
    { Creates } Devices in a Service or SubService from a CSV

    """
    schema_name = "IoTADevices"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id, subservice_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            None,
                            None,
                            None,
                            self.IOTA_PROTOCOL,
                            self.IOTA_HOST,
                            self.IOTA_PORT,
                            self.ORION_PROTOCOL,
                            self.ORION_HOST,
                            self.ORION_PORT,
                            self.CA_PROTOCOL,
                            self.CA_HOST,
                            self.CA_PORT)
            result = flow.register_devices(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SUBSERVICE_NAME", None),
                request.DATA.get("SUBSERVICE_ID",  subservice_id),
                request.DATA.get("SERVICE_USER_NAME", None),
                request.DATA.get("SERVICE_USER_PASSWORD", None),
                request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("CSV_DEVICES", None),
            )
            if 'error' not in result:
                Stats.num_post_devices += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class SubServiceIoTAService_RESTView(APIView, IoTConf):
    """
    { Create } Service Entity for  IoTA Service or SubService

    """
    schema_name = "IoTAService"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id, subservice_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT,
                            None,
                            None,
                            None,
                            self.IOTA_PROTOCOL,
                            self.IOTA_HOST,
                            self.IOTA_PORT,
                            self.ORION_PROTOCOL,
                            self.ORION_HOST,
                            self.ORION_PORT,
                            self.CA_PROTOCOL,
                            self.CA_HOST,
                            self.CA_PORT)
            result = flow.register_service(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SUBSERVICE_NAME", None),
                request.DATA.get("SUBSERVICE_ID",  subservice_id),
                request.DATA.get("SERVICE_USER_NAME", None),
                request.DATA.get("SERVICE_USER_PASSWORD", None),
                request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("ENTITY_TYPE", None),
                request.DATA.get("ENTITY_ID", None),
                request.DATA.get("PROTOCOL", None),
                request.DATA.get("ATT_NAME", None),
                request.DATA.get("ATT_PROVIDER", None),
                request.DATA.get("ATT_ENDPOINT", None),
                request.DATA.get("ATT_METHOD", None),
                request.DATA.get("ATT_AUTHENTICATION", None),
                request.DATA.get("ATT_INTERACTION_TYPE", None),
                request.DATA.get("ATT_MAPPING", None),
                request.DATA.get("ATT_TIMEOUT", None)
            )
            if 'error' not in result:
                Stats.num_post_entity_service += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class IOTModuleActivation_RESTView(APIView, IoTConf):
    """
    { Create, Read, Delete } IOT Module Activation

    """
    schema_name = "IOTModuleActivation"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id, subservice_id=None):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            if not subservice_id:
                flow = Domains(self.KEYSTONE_PROTOCOL,
                               self.KEYSTONE_HOST,
                               self.KEYSTONE_PORT,
                               None,
                               None,
                               None,
                               self.IOTA_PROTOCOL,
                               self.IOTA_HOST,
                               self.IOTA_PORT,
                               self.ORION_PROTOCOL,
                               self.ORION_HOST,
                               self.ORION_PORT,
                               self.CA_PROTOCOL,
                               self.CA_HOST,
                               self.CA_PORT)
                modules = flow.list_activated_modules(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_PASSWORD", None),
                    request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN)
                )
            else:
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.IOTA_PROTOCOL,
                                self.IOTA_HOST,
                                self.IOTA_PORT,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.CA_PROTOCOL,
                                self.CA_HOST,
                                self.CA_PORT)
                modules = flow.list_activated_modules(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SUBSERVICE_NAME", None),
                    request.DATA.get("SUBSERVICE_ID",  subservice_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_PASSWORD", None),
                    request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN)
                )
            result = {}
            if 'error' not in modules:
                result['actived_modules'] = modules
                Stats.num_get_module_activation += 1
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = modules
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, service_id, subservice_id=None, iot_module=None):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            if not subservice_id:
                flow = Domains(self.KEYSTONE_PROTOCOL,
                               self.KEYSTONE_HOST,
                               self.KEYSTONE_PORT,
                               None,
                               None,
                               None,
                               self.IOTA_PROTOCOL,
                               self.IOTA_HOST,
                               self.IOTA_PORT,
                               self.ORION_PROTOCOL,
                               self.ORION_HOST,
                               self.ORION_PORT,
                               self.CA_PROTOCOL,
                               self.CA_HOST,
                               self.CA_PORT)
                sub = flow.activate_module(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_PASSWORD", None),
                    request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("IOTMODULE", iot_module),
                )
            else:
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.IOTA_PROTOCOL,
                                self.IOTA_HOST,
                                self.IOTA_PORT,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.CA_PROTOCOL,
                                self.CA_HOST,
                                self.CA_PORT)
                sub = flow.activate_module(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SUBSERVICE_NAME", None),
                    request.DATA.get("SUBSERVICE_ID",  subservice_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_PASSWORD", None),
                    request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("IOTMODULE", iot_module),
                )
            result = {}
            result['subscriptionid'] = sub
            if 'error' not in result:
                Stats.num_post_module_activation += 1
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


    def delete(self, request, service_id, subservice_id=None, iot_module=None):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            if not subservice_id:
                flow = Domains(self.KEYSTONE_PROTOCOL,
                               self.KEYSTONE_HOST,
                               self.KEYSTONE_PORT,
                               None,
                               None,
                               None,
                               self.IOTA_PROTOCOL,
                               self.IOTA_HOST,
                               self.IOTA_PORT,
                               self.ORION_PROTOCOL,
                               self.ORION_HOST,
                               self.ORION_PORT,
                               self.CA_PROTOCOL,
                               self.CA_HOST,
                               self.CA_PORT)
                flow.deactivate_module(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_PASSWORD", None),
                    request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("IOTMODULE", iot_module),
                )
            else:
                flow = Projects(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                None,
                                None,
                                None,
                                self.IOTA_PROTOCOL,
                                self.IOTA_HOST,
                                self.IOTA_PORT,
                                self.ORION_PROTOCOL,
                                self.ORION_HOST,
                                self.ORION_PORT,
                                self.CA_PROTOCOL,
                                self.CA_HOST,
                                self.CA_PORT)
                flow.deactivate_module(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SUBSERVICE_NAME", None),
                    request.DATA.get("SUBSERVICE_ID",  subservice_id),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_PASSWORD", None),
                    request.DATA.get("SERVICE_USER_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("IOTMODULE", iot_module),
                )
            result = {}

            if 'error' not in result:
                Stats.num_delete_module_activation += 1
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                Stats.num_flow_errors += 1
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            Stats.num_api_errors += 1
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class OrchVersion_RESTView(APIView, IoTConf):
    """
     { Read } Orchestrator Statistics
    """

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request):

        #HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
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

                    "num_api_errors": self.num_api_errors,
                    "num_flow_errors": self.num_flow_errors

                }
            }

            # print it into a trace
            logger.info("Orchestrator statistics: %s" % json.dumps(
                result, indent=3))

            if 'error' not in result:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
