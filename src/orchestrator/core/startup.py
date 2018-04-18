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
import os
import json

from django.conf import settings

from orchestrator.core.keystone import IdMKeystoneOperations as IdMOperations
from orchestrator.core.keypass import AccCKeypassOperations as AccCOperations

from orchestrator.common.util import ContextFilterCorrelatorId
from orchestrator.common.util import ContextFilterTransactionId
from orchestrator.common.util import ContextFilterService
from orchestrator.common.util import ContextFilterSubService

logger = logging.getLogger('orchestrator_api')
logger.addFilter(ContextFilterCorrelatorId("n/a"))
logger.addFilter(ContextFilterTransactionId("n/a"))
logger.addFilter(ContextFilterService("None"))
logger.addFilter(ContextFilterSubService(""))

logger1 = logging.getLogger('orchestrator_core')
logger1.addFilter(ContextFilterCorrelatorId("n/a"))
logger1.addFilter(ContextFilterTransactionId("n/a"))
logger1.addFilter(ContextFilterService("None"))
logger1.addFilter(ContextFilterSubService(""))

logger2 = logging.getLogger('django')
logger2.addFilter(ContextFilterCorrelatorId("n/a"))
logger2.addFilter(ContextFilterTransactionId("n/a"))
logger2.addFilter(ContextFilterService("None"))
logger2.addFilter(ContextFilterSubService(""))

logger3 = logging.getLogger('django.request')
logger3.addFilter(ContextFilterCorrelatorId("n/a"))
logger3.addFilter(ContextFilterTransactionId("n/a"))
logger3.addFilter(ContextFilterService("None"))
logger3.addFilter(ContextFilterSubService(""))


def read_banner():
    banner_dir = os.path.dirname(__file__)
    handle = open(banner_dir + '/' + 'banner.txt', 'r+')
    var = handle.read()
    return var


def check_endpoints():

    KEYSTONE_PROTOCOL = settings.KEYSTONE['protocol']
    KEYSTONE_HOST = settings.KEYSTONE['host']
    KEYSTONE_PORT = settings.KEYSTONE['port']

    KEYPASS_PROTOCOL = settings.KEYPASS['protocol']
    KEYPASS_HOST = settings.KEYPASS['host']
    KEYPASS_PORT = settings.KEYPASS['port']

    idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)
    try:
        idm.checkIdM()
        logger.info("Keystone endpoint OK")
    except Exception, ex:
        logger.error("keystone endpoint not found: %s" % ex)
        return "ERROR keystone endpoint not found: %s" % ex

    ac = AccCOperations(KEYPASS_PROTOCOL, KEYPASS_HOST, KEYPASS_PORT)
    try:
        ac.checkAccC()
        logger.info("Keypass endpoint OK")
    except Exception, ex:
        logger.error("keypass endpoint not found: %s" % ex)
        return "ERROR keypass endpoint not found: %s" % ex

    return "OK"

def show_conf():
    conf = {}
    from django.conf import settings
    custom_settings_entries = ['KEYSTONE', 'KEYPASS',
                               'ORION',
                               'PEP', 'IOTAGENT', 'SCIM_API_VERSION',
                               'CYGNUS', 'STH', 'PERSEO',
                               'LDAP', 'MAILER', 'MONGODB'
                               ]
    for name in custom_settings_entries:
        conf[name] = getattr(settings, name)
    return conf


def run():
    logger.info("Starting Service %s " % read_banner())
    logger.info("Checking endpoints %s " % check_endpoints())
    logger.info("Using custom conf: %s " % json.dumps(show_conf(), indent=3))
