#
# Copyright 2018 Telefonica Espana
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

from orchestrator.core.flow.LdapUserHelper import LdapUserHelper
from orchestrator.core.flow.LdapGroupHelper import LdapGroupHelper
from orchestrator.api import parsers
from orchestrator.api.iotconf import IoTConf
from orchestrator.api.stats import Stats

class LdapUser_RESTView(APIView, IoTConf):
    """
    { Create, Read, Update, Delete } LDAP Users

    """
    schema_name = "LdapUser"
    parser_classes = (parsers.JSONSchemaParser,)
    stats = None

    def __init__(self):
        IoTConf.__init__(self)
        stats = Stats()

    def post(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapUserHelper(
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           MAILER_HOST=self.MAILER_HOST,
                           MAILER_PORT=self.MAILER_PORT,
                           MAILER_TLS=self.MAILER_TLS,
                           MAILER_USER=self.MAILER_USER,
                           MAILER_PASSWORD=self.MAILER_PASSWORD,
                           MAILER_FROM=self.MAILER_FROM,
                           MAILER_TO=self.MAILER_TO,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            if (request.data.get("LDAP_ADMIN_USER", None) and
                    request.data.get("LDAP_ADMIN_PASSWORD", None)):
                result = flow.createNewUser(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("NEW_USER_NAME", None),
                               request.data.get("NEW_USER_PASSWORD", None),
                               request.data.get("NEW_USER_EMAIL", None),
                               request.data.get("NEW_USER_DESCRIPTION", None),
                               request.data.get("GROUP_NAMES", None))
            else:
                result = flow.askForCreateNewUser(
                               request.data.get("NEW_USER_NAME", None),
                               request.data.get("NEW_USER_PASSWORD", None),
                               request.data.get("NEW_USER_EMAIL", None),
                               request.data.get("NEW_USER_DESCRIPTION", None),
                               request.data.get("GROUP_NAMES", None))

            if 'error' not in result:
                self.stats.add_statistic("num_post_ldap", 1)
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response

    def get(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapUserHelper(
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            if ( request.data.get("LDAP_ADMIN_USER", None) and
                 request.data.get("LDAP_ADMIN_PASSWORD", None) and
                 request.data.get("FILTER", None)):
                result = flow.listUsers(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("FILTER", None))
            elif ( request.data.get("LDAP_ADMIN_USER", None) and
                   request.data.get("LDAP_ADMIN_PASSWORD", None) and
                   request.data.get("USER_NAME", None)):
                result = flow.getUserDetailByAdmin(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("USER_NAME", None))
            elif (request.data.get("USER_NAME", None) and
                  request.data.get("USER_PASSWORD", None)):
                result = flow.getUserDetail(
                               request.data.get("USER_NAME", None),
                               request.data.get("USER_PASSWORD", None))
            else:
                result = { "error": "not valid parameters", "code": 400 }
            if 'error' not in result:
                stats.add_statistic("num_get_ldap", 1)
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response

    def put(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapUserHelper(
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         LDAP_HOST=self.LDAP_HOST,
                         LDAP_PORT=self.LDAP_PORT,
                         LDAP_BASEDN=self.LDAP_BASEDN,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result = flow.updateUser(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("USER_NAME", None),
                               request.data.get("USER_PASSWORD", None),
                               request.data.get("USER_DATA", None))
            if 'error' not in result:
                self.stats.add_statistic("num_put_ldap", 1)
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response
    

    def delete(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapUserHelper(
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         LDAP_HOST=self.LDAP_HOST,
                         LDAP_PORT=self.LDAP_PORT,
                         LDAP_BASEDN=self.LDAP_BASEDN,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result = flow.deleteUser(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("USER_NAME", None),
                               request.data.get("USER_PASSWORD", None))
            if 'error' not in result:
                self.stats.add_statistic("num_delete_ldap", 1)
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response


class LdapAuth_RESTView(APIView, IoTConf):
    """
    { post } LDAP Auth

    """
    schema_name = "LdapUser"
    parser_classes = (parsers.JSONSchemaParser,)
    stats = None

    def __init__(self):
        IoTConf.__init__(self)
        stats = Stats()

    def post(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapUserHelper(
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result = flow.authUser(
                               request.data.get("USER_NAME", None),
                               request.data.get("USER_PASSWORD", None))

            if 'error' not in result:
                self.stats.add_statistic("num_post_ldap", 1)
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response


class LdapGroup_RESTView(APIView, IoTConf):
    """
    { Create, Read, Update, Delete } LDAP Groups

    """
    schema_name = "LdapGroup"
    parser_classes = (parsers.JSONSchemaParser,)
    stats = None

    def __init__(self):
        IoTConf.__init__(self)
        stats = Stats()

    def post(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapGroupHelper(
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           MAILER_HOST=self.MAILER_HOST,
                           MAILER_PORT=self.MAILER_PORT,
                           MAILER_TLS=self.MAILER_TLS,
                           MAILER_USER=self.MAILER_USER,
                           MAILER_PASSWORD=self.MAILER_PASSWORD,
                           MAILER_FROM=self.MAILER_FROM,
                           MAILER_TO=self.MAILER_TO,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            result = flow.createNewGroup(
                request.data.get("LDAP_ADMIN_USER", None),
                request.data.get("LDAP_ADMIN_PASSWORD", None),
                request.data.get("NEW_GROUP_NAME", None),
                request.data.get("NEW_GROUP_DESCRIPTION", None))

            if 'error' not in result:
                self.stats.add_statistic("num_post_ldap", 1)
                response = Response(result, status=status.HTTP_201_CREATED,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response

    def get(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapGroupHelper(
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            if ( request.data.get("LDAP_ADMIN_USER", None) and
                 request.data.get("LDAP_ADMIN_PASSWORD", None) and
                 request.data.get("FILTER", None)):
                result = flow.listGroups(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("FILTER", None))
            elif ( request.data.get("LDAP_ADMIN_USER", None) and
                   request.data.get("LDAP_ADMIN_PASSWORD", None) and
                   request.data.get("GROUP_NAME", None)):
                result = flow.getGroupDetailByAdmin(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("GROUP_NAME", None))
            else:
                result = { "error": "not valid parameters", "code": 400 }
            if 'error' not in result:
                self.stats.add_statistic("num_get_ldap", 1)
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response


    def put(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapGroupHelper(
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         LDAP_HOST=self.LDAP_HOST,
                         LDAP_PORT=self.LDAP_PORT,
                         LDAP_BASEDN=self.LDAP_BASEDN,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result = flow.updateGroup(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("GROUP_NAME", None),
                               request.data.get("GROUP_DESCRIPTION", None))
            if 'error' not in result:
                self.stats.add_statistic("num_put_ldap", 1)
                response = Response(result, status=status.HTTP_200_OK,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response


    def delete(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.data  # json validation
            flow = LdapGroupHelper(
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         None, None, None,
                         LDAP_HOST=self.LDAP_HOST,
                         LDAP_PORT=self.LDAP_PORT,
                         LDAP_BASEDN=self.LDAP_BASEDN,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result = flow.deleteGroup(
                               request.data.get("LDAP_ADMIN_USER", None),
                               request.data.get("LDAP_ADMIN_PASSWORD", None),
                               request.data.get("GROUP_NAME", None))
            if 'error' not in result:
                self.stats.add_statistic("num_delete_ldap", 1)
                response = Response(result, status=status.HTTP_204_NO_CONTENT,
                                headers={"Fiware-Correlator": CORRELATOR_ID})
            else:
                self.stats.add_statistic("num_flow_errors", 1)
                response = Response(result['error'],
                                status=self.getStatusFromCode(result['code']),
                                headers={"Fiware-Correlator": CORRELATOR_ID})
        except ParseError as error:
            self.stats.add_statistic("num_api_errors", 1)
            response = Response(
                'Input validation error - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Fiware-Correlator": CORRELATOR_ID}
            )
        return response
