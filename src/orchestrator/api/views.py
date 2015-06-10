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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import views

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

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
from orchestrator.api import negotiators, parsers


logger = logging.getLogger('orchestrator_api')


class IoTConf(object):
    # Class to extract Keystone/Keypass conf from django settings
    def __init__(self):
        try:
            self.KEYSTONE_PROTOCOL = settings.KEYSTONE['protocol']
            self.KEYSTONE_HOST = settings.KEYSTONE['host']
            self.KEYSTONE_PORT = settings.KEYSTONE['port']

            self.KEYPASS_PROTOCOL = settings.KEYPASS['protocol']
            self.KEYPASS_HOST = settings.KEYPASS['host']
            self.KEYPASS_PORT = settings.KEYPASS['port']

        except KeyError:
            logger.error("keystone or keypass conf error")
            raise ImproperlyConfigured("keystone or keypass conf")

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
    Lists of modifies and existent service

    """
    schema_name = "ServiceList"
    parser_classes = (parsers.JSONSchemaParser,)
    # content_negotiation_class = negotiators.IgnoreClientContentNegotiation

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

    def put(self, request, service_id=None):
        self.schema_name = "ServiceList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            # request.DATA # json validation
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

    def delete(self, request, service_id=None):
        self.schema_name = "ServiceList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            # request.DATA  # json validation
            flow = Domains(self.KEYSTONE_PROTOCOL,
                           self.KEYSTONE_HOST,
                           self.KEYSTONE_PORT,
                           self.KEYPASS_PROTOCOL,
                           self.KEYPASS_HOST,
                           self.KEYPASS_PORT)
            result = flow.delete_domain(
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))
            if 'error' not in result:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class ServiceCreate_RESTView(ServiceList_RESTView):
    """
    Creates a new service

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
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class SubServiceList_RESTView(APIView, IoTConf):
    """
    Modifies a SubService
    """
    schema_name = "SubServiceList"
    parser_classes = (parsers.JSONSchemaParser,)
    # content_negotiation_class = negotiators.IgnoreClientContentNegotiation

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
                    # TODO: get detail of subservice
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

    def delete(self, request, service_id=None, subservice_id=None):
        self.schema_name = "SubServiceList"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            # request.DATA # json validation
            flow = Projects(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT)
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
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class SubServiceCreate_RESTView(SubServiceList_RESTView):
    """
    Creates a new SubService into a Service
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
                                       self.KEYSTONE_PORT)
            result = flow.createNewSubService(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN",
                                 HTTP_X_AUTH_TOKEN),
                request.DATA.get("NEW_SUBSERVICE_NAME", None),
                request.DATA.get("NEW_SUBSERVICE_DESCRIPTION", None))

            if 'id' in result:
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class User_RESTView(APIView, IoTConf):
    """
    Modifies an Users of a Service

    """
    schema_name = "User"
    parser_classes = (parsers.JSONSchemaParser,)
    # content_negotiation_class = negotiators.IgnoreClientContentNegotiation

    def __init__(self):
        IoTConf.__init__(self)

    def delete(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            flow = RemoveUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)
            # TODO: use user_id
            result = flow.removeUser(
                request.DATA.get("SERVICE_NAME", None),
                request.DATA.get("SERVICE_ID", service_id),
                request.DATA.get("SERVICE_ADMIN_USER", None),
                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                request.DATA.get("USER_NAME", None),
                request.DATA.get("USER_ID", user_id))
            if 'error' not in result:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            request.DATA  # json validation
            # TODO: el usuario se edita a si mismo? NO
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
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
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

    def post(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        try:
            #request.DATA  # json validation
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


class UserList_RESTView(APIView, IoTConf):
    """
    Return a list of Users of a Service

    """
    schema_name = "UserList"
    parser_classes = (parsers.JSONSchemaParser,)
    # content_negotiation_class = negotiators.IgnoreClientContentNegotiation

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
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class Role_RESTView(APIView, IoTConf):
    """
    Modifies an Roles of a Service

    """
    schema_name = "Role"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

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
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class RoleList_RESTView(APIView, IoTConf):
    """
    Creates or returns a Role into a service

    """
    schema_name = "Role"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id):
        self.schema_name = "Role"
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
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
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


class AssignRoleUser_RESTView(APIView, IoTConf):
    """
    Assign or list assignments of a role to a user in a service or subservice

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
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result['error'],
                            status=self.getStatusFromCode(result['code']))

    def post(self, request, service_id):
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.DATA.get('INHERIT', False) is True)
        try:
            request.DATA  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)

            if not (request.DATA.get("SUBSERVICE_NAME", None) or
                    request.DATA.get("SUBSERVICE_ID", None)):
                if inherit:
                    result = flow.assignInheritRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME", None),
                        request.DATA.get("ROLE_ID", None),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", None))
                else:
                    result = flow.assignRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN",
                                         HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME", None),
                        request.DATA.get("ROLE_ID", None),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", None))
            else:
                result = flow.assignRoleSubServiceUser(
                    request.DATA.get("SERVICE_NAME", None),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SUBSERVICE_NAME", None),
                    request.DATA.get("SUBSERVICE_ID", None),
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("ROLE_NAME", None),
                    request.DATA.get("ROLE_ID", None),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_ID", None))
            if 'error' not in result:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, service_id):
        self.schema_name = "AssignRole"
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        inherit = (request.GET.get('inherit', False) is True or
                   request.DATA.get('INHERIT', False) is True)
        try:
            request.DATA  # json validation
            flow = Roles(self.KEYSTONE_PROTOCOL,
                         self.KEYSTONE_HOST,
                         self.KEYSTONE_PORT)

            if not (request.DATA.get("SUBSERVICE_NAME", None) or
                    request.DATA.get("SUBSERVICE_ID", None)):
                if inherit:
                    result = flow.revokeInheritRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME"),
                        request.DATA.get("ROLE_ID", None),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", None))
                else:
                    result = flow.revokeRoleServiceUser(
                        request.DATA.get("SERVICE_NAME", None),
                        request.DATA.get("SERVICE_ID", service_id),
                        request.DATA.get("SERVICE_ADMIN_USER", None),
                        request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                        request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                        request.DATA.get("ROLE_NAME"),
                        request.DATA.get("ROLE_ID", None),
                        request.DATA.get("SERVICE_USER_NAME", None),
                        request.DATA.get("SERVICE_USER_ID", None))
            else:
                result = flow.revokeRoleSubServiceUser(
                    request.DATA.get("SERVICE_NAME"),
                    request.DATA.get("SERVICE_ID", service_id),
                    request.DATA.get("SUBSERVICE_NAME"),
                    request.DATA.get("SUBSERVICE_ID", None),
                    request.DATA.get("SERVICE_ADMIN_USER", None),
                    request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                    request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                    request.DATA.get("ROLE_NAME", None),
                    request.DATA.get("ROLE_ID", None),
                    request.DATA.get("SERVICE_USER_NAME", None),
                    request.DATA.get("SERVICE_USER_ID", None))
            if 'error' not in result:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))
        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )


class Trust_RESTView(APIView, IoTConf):
    """
    Creates a Trust Token

    """
    schema_name = "Trust"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id):
        self.schema_name = "Trust"
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
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result['error'],
                                status=self.getStatusFromCode(result['code']))

        except ParseError as error:
            return Response(
                'Input validation error - {0} {1}'.format(error.message,
                                                          error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
