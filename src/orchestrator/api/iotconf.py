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

from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.conf import settings
#from orchestrator.api.stats import Stats

logger = logging.getLogger('orchestrator_api')

class IoTConf():
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
            self.LDAP_HOST = settings.LDAP['host']
            self.LDAP_PORT = settings.LDAP['port']
            self.LDAP_BASEDN = settings.LDAP['basedn']
        except KeyError:
            logger.warn("LDAP endpoint configuration error. " +
                        "Forcing to use default conf values (localhost)")
            self.LDAP_HOST = "localhost"
            self.LDAP_PORT = "389"
            self.LDAP_BASEDN = "dc=openstack,dc=org"

        try:
            self.MAILER_HOST = settings.MAILER['host']
            self.MAILER_PORT = settings.MAILER['port']
            self.MAILER_TLS = settings.MAILER['tls']
            self.MAILER_USER = settings.MAILER['user']
            self.MAILER_PASSWORD = settings.MAILER['password']
            self.MAILER_FROM = settings.MAILER['from']
            self.MAILER_TO = settings.MAILER['to']
        except KeyError:
            logger.warn("MAILER endpoint configuration error. " +
                        "Forcing to use default conf values (localhost)")
            self.MAILER_HOST = "localhost"
            self.MAILER_PORT = "587"
            self.MAILER_TLS = "true"
            self.MAILER_USER = "smtpuser@yourdomain.com"
            self.MAILER_PASSWORD = "yourpassword"
            self.MAILER_FROM = "smtpuser"
            self.MAILER_TO = "smtpuser"

        try:
            self.MONGODB_URI = settings.MONGODB["URI"]
        except KeyError:
            logger.error("MONGODB URI configuration error. " +
                         "Forcing to use default conf values (127.0.0.1:27017)")
            self.MONGODB_URI = "mongnodb://127.0.0.1:27017"


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

    def getFromHeader(self, request):
        # x-forwarded-for/forwarded overwrites x-real-ip
        origin = request.META.get('HTTP_X_REAL_IP', None)
        origin = request.META.get('HTTP_X_FORWARDED_FOR', origin)
        origin = request.META.get('HTTP_FORWARDED', origin)
        return origin
