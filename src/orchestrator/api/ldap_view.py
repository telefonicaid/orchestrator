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
import logging
import json
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.throttling import AnonRateThrottle

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from datetime import datetime

from orchestrator.core.flow.LdapUserHelper import LdapUserHelper
from orchestrator.api import parsers
from orchestrator.api.iotconf import IoTConf
from orchestrator.api.stats import Stats

from orchestrator.common.util import ContextFilterCorrelatorId
from orchestrator.common.util import ContextFilterTransactionId


class LdapUser_RESTView(APIView, IoTConf):
    """
    { Create, Read, Update, Delete } LDAP Users

    """
    schema_name = "LdapUser"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)


    def post(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           MAILER_HOST=self.MAILER_HOST,
                           MAILER_PORT=self.MAILER_PORT,
                           MAILER_USER=self.MAILER_USER,
                           MAILER_PASSWORD=self.MAILER_PASSWORD,
                           MAILER_FROM=self.MAILER_FROM,
                           MAILER_TO=self.MAILER_TO,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            # if LDAP_ADMIN_USER and LDA_ADMIN_PASSWORD
            if (request.DATA.get("LDAP_ADMIN_USER", None) and
                    request.DATA.get("LDAP_ADMIN_PASSWORD", None)):
                result = flow.createNewUser(
                               request.DATA.get("LDAP_ADMIN_USER", None),
                               request.DATA.get("LDAP_ADMIN_PASSWORD", None),
                               request.DATA.get("NEW_USER_NAME", None),
                               request.DATA.get("NEW_USER_PASSWORD", None),
                               request.DATA.get("NEW_USER_EMAIL", None), 
                               request.DATA.get("NEW_USER_DESCRIPTION", None),
                               request.DATA.get("GROUP_NAMES", None))
            else:
                result = flow.askForCreateNewUser(
                               request.DATA.get("NEW_USER_NAME", None),
                               request.DATA.get("NEW_USER_PASSWORD", None),
                               request.DATA.get("NEW_USER_EMAIL", None),
                               request.DATA.get("NEW_USER_DESCRIPTION", None),
                               request.DATA.get("GROUP_NAMES", None))

            if 'error' not in result:
                #Stats.num_post_ldap += 1
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
        return response

    def get(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            # if FILTER, LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD
            if ( request.DATA.get("LDAP_ADMIN_USER", None) and
                 request.DATA.get("LDAP_ADMIN_PASSWORD", None) and
                 request.DATA.get("FILTER", None)):
                result = flow.listUsers(
                               request.DATA.get("LDAP_ADMIN_USER", None),
                               request.DATA.get("LDAP_ADMIN_PASSWORD", None),
                               request.DATA.get("FILTER", None))
            elif (request.DATA.get("USER_NAME", None) and
                  request.DATA.get("USER_PASSWORD", None)):
                result = flow.getUserDetail(
                               request.DATA.get("USER_NAME", None),
                               request.DATA.get("USER_PASSWORD", None))
            else:
                result = { "error": "not valid parameters", "code": 400 }
            if 'error' not in result:
                #Stats.num_get_ldap += 1
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
        return response        

    def put(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(
                         None, None, None,
                         LDAP_HOST=self.LDAP_HOST,
                         LDAP_PORT=self.LDAP_PORT,
                         LDAP_BASEDN=self.LDAP_BASEDN,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result = flow.updateUser(
                               request.DATA.get("LDAP_ADMIN_USER", None),
                               request.DATA.get("LDAP_ADMIN_PASSWORD", None),
                               request.DATA.get("USER_NAME", None),
                               request.DATA.get("USER_PASSWORD", None),
                               request.DATA.get("USER_DATA", None))
            if 'error' not in result:
                #Stats.num_put_ldap += 1
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
        return response
    

    def delete(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(
                         None, None, None,
                         LDAP_HOST=self.LDAP_HOST,
                         LDAP_PORT=self.LDAP_PORT,
                         LDAP_BASEDN=self.LDAP_BASEDN,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result = flow.deleteUser(
                               request.DATA.get("LDAP_ADMIN_USER", None),
                               request.DATA.get("LDAP_ADMIN_PASSWORD", None),
                               request.DATA.get("USER_NAME", None),
                               request.DATA.get("USER_PASSWORD", None))
            if 'error' not in result:
                #Stats.num_delete_ldap += 1
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
        return response


class LdapAuth_RESTView(APIView, IoTConf):
    """
    { post } LDAP Auth

    """
    schema_name = "LdapUser"
    parser_classes = (parsers.JSONSchemaParser,)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request):
        response = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(
                           None, None, None,
                           LDAP_HOST=self.LDAP_HOST,
                           LDAP_PORT=self.LDAP_PORT,
                           LDAP_BASEDN=self.LDAP_BASEDN,
                           CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            # if LDAP_ADMIN_USER and LDA_ADMIN_PASSWORD
            result = flow.authUser(
                               request.DATA.get("USER_NAME", None),
                               request.DATA.get("USER_PASSWORD", None))

            if 'error' not in result:
                #Stats.num_post_ldap += 1
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
        return response
