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

from orchestrator.api.stats import Stats


class IoTConf(Stats):
    throttle_classes = (AnonRateThrottle,)

    # Class to extract Keystone/Keypass conf from django settings
    def __init__(self):
        try:
            self.KEYSTONE_PROTOCOL = settings.KEYSTONE['protocol']
            self.KEYSTONE_HOST = settings.KEYSTONE['host']
            self.KEYSTONE_PORT = settings.KEYSTONE['port']
        except KeyError:
            logger.error("KEYSTONE endpoint configuration error. " +
                         "Forcing to use default conf values (localhost)")
            self.KEYSTONE_PROTOCOL = "http"
            self.KEYSTONE_HOST = "localhost"
            self.KEYSTONE_PORT = "5001"

        try:
            self.KEYPASS_PROTOCOL = settings.KEYPASS['protocol']
            self.KEYPASS_HOST = settings.KEYPASS['host']
            self.KEYPASS_PORT = settings.KEYPASS['port']
        except KeyError:
            logger.error("KEYPASS endpoint configuration error. " +
                         "Forcing to use default conf values (localhost)")
            self.KEYPASS_PROTOCOL = "http"
            self.KEYPASS_HOST = "localhost"
            self.KEYPASS_PORT = "17070"

        try:
            self.IOTA_PROTOCOL = settings.IOTA['protocol']
            self.IOTA_HOST = settings.IOTA['host']
            self.IOTA_PORT = settings.IOTA['port']
        except KeyError:
            logger.error("IOTA endpoint configuration error. " +
                         "Forcing to use default conf values (localhost)")
            self.IOTA_PROTOCOL = "http"
            self.IOTA_HOST = "localhost"
            self.IOTA_PORT = "4052"

        try:
            self.ORION_PROTOCOL = settings.ORION['protocol']
            self.ORION_HOST = settings.ORION['host']
            self.ORION_PORT = settings.ORION['port']
        except KeyError:
            logger.error("ORION endpoint configuration error. " +
                         "Forcing to use default conf values (localhost)")
            self.ORION_PROTOCOL = "http"
            self.ORION_HOST = "localhost"
            self.ORION_PORT = "1026"

        try:
            self.CA_PROTOCOL = settings.CA['protocol']
            self.CA_HOST = settings.CA['host']
            self.CA_PORT = settings.CA['port']
        except KeyError:
            logger.error("CA endpoint configuration error. " +
                         "Forcing to use default conf values (localhost)")
            self.CA_PROTOCOL = "http"
            self.CA_HOST = "localhost"
            self.CA_PORT = "9999"

        try:
            self.PERSEO_PROTOCOL = settings.PEP_PERSEO['protocol']
            self.PERSEO_HOST = settings.PEP_PERSEO['host']
            self.PERSEO_PORT = settings.PEP_PERSEO['port']
        except KeyError:
            logger.error("PEP_PERSEO endpoint configuration error. " +
                         "Forcing to use default conf values (localhost)")
            self.PERSEO_PROTOCOL = "http"
            self.PERSEO_HOST = "localhost"
            self.PERSEO_PORT = "9090"

        try:
            self.LDAP_PROTOCOL = settings.LDAP['protocol']
            self.LDAP_HOST = settings.LDAP['host']
            self.LDAP_PORT = settings.LDAP['port']
        except KeyError:
            logger.error("LDAP endpoint configuration error. " +
                         "Forcing to use default conf values (localhost)")
            self.LDAP_PROTOCOL = "http"
            self.LDAP_HOST = "localhost"
            self.LDAP_PORT = "389"            


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
        elif code == 500:
            rstatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            rstatus = status.HTTP_400_BAD_REQUEST
        return rstatus

    def getCorrelatorIdHeader(self, request):
        return request.META.get('FIWARE-CORRELATOR', None)

    def getXAuthToken(self, request):
        return request.META.get('HTTP_X_AUTH_TOKEN', None)

    def getCorrelatorId(self, flow, CORRELATOR_ID):
        return str(flow.CORRELATOR_ID) if not CORRELATOR_ID else CORRELATOR_ID
