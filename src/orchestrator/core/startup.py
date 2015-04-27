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

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from orchestrator.core.keystone import IdMKeystoneOperations as IdMOperations
from orchestrator.core.keypass import AccCKeypassOperations as AccCOperations

logger = logging.getLogger('orchestrator_api')


def read_banner():
    banner_dir = os.path.dirname(__file__)
    handle=open(banner_dir + '/'+ 'banner.txt','r+')
    var=handle.read()
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
        idm.checkIdM();
    except Exception, ex:
        logger.error("keystone endpoint not found")
        return "ERROR keystone endpoint not found"

    ac = AccCOperations(KEYPASS_PROTOCOL, KEYPASS_HOST, KEYPASS_PORT)        
    try:
        ac.checkAccC();
    except Exception, ex:
        logger.error("keyspass endpoint not found")        
        return "ERROR keypass endpoint not found"
        
    return "OK"
    
    
def run():
    logger.info("Starting Service %s " % read_banner())
    logger.info("Checking endpoints %s " % check_endpoints())    
