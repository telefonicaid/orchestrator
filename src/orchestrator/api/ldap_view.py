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
        response = service_name = subservice_name = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(self.LDAP_PROTOCOL,
                         self.LDAP_HOST,
                         self.LDAP_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            # if LDAP_ADMIN_USER and LDA_ADMIN_PASSWORD
            result, service_name, subservice_name = flow.createNewUser(
                               request.DATA.get("LDAP_ADMIN_USER", None),
                               request.DATA.get("LDAP_ADMIN_PASSWORD", None),
                               request.DATA.get("NEW_USER_NAME", None),
                               request.DATA.get("NEW_USER_PASSWORD", None),
                               request.DATA.get("NEW_USER_EMAIL", None), 
                               request.DATA.get("NEW_USER_DESCRIPTION", None),
                               request.DATA.get("GROUP_NAMES", None))
            # else -> flow.askforCreateNewUser()
            
            if 'error' not in result:
                #Stats.num_post_ldap += 1
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

    def get(self, request):
        response = service_name = subservice_name = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(self.LDAP_PROTOCOL,
                         self.LDAP_HOST,
                         self.LDAP_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)

            # if FILTER, LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD
            if request.DATA.get("FILTER", None):
                result, service_name, subservice_name = flow.listUsers(
                               request.DATA.get("LDAP_ADMIN_USER", None),
                               request.DATA.get("LDAP_ADMIN_PASSWORD", None),
                               request.DATA.get("FILTER", None))
            else: 
                result, service_name, subservice_name = flow.getUserDetail(
                               request.DATA.get("USER_NAME", None),
                               request.DATA.get("USER_PASSWORD", None))
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
        response = service_name = subservice_name = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(self.LDAP_PROTOCOL,
                         self.LDAP_HOST,
                         self.LDAP_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.updateUser(
                               request.DATA.get("LDAP_ADMIN_USER", None),
                               request.DATA.get("LDAP_ADMIN_PASSWORD", None),
                               request.DATA.get("USER_NAME", None),
                               request.DATA.get("USER_PASSWORD", None),
                               request.DATA.get("DATA_USER", None))
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
        response = service_name = subservice_name = flow = None
        CORRELATOR_ID = self.getCorrelatorIdHeader(request)
        try:
            request.DATA  # json validation
            flow = LdapUserHelper(self.LDAP_PROTOCOL,
                         self.LDAP_HOST,
                         self.LDAP_PORT,
                         CORRELATOR_ID=CORRELATOR_ID)
            CORRELATOR_ID = self.getCorrelatorId(flow, CORRELATOR_ID)
            result, service_name, subservice_name = flow.deleteUser(
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
