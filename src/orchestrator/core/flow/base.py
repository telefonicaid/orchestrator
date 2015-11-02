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

from orchestrator.core.keystone import IdMKeystoneOperations as IdMOperations
from orchestrator.core.keypass import AccCKeypassOperations as AccCOperations
from orchestrator.core.iota_cpp import IoTACppOperations as IoTAOperations
from orchestrator.core.orion import CBOrionOperations as CBOperations

logger = logging.getLogger('orchestrator_core')


class FlowBase(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT,
                 KEYPASS_PROTOCOL=None,
                 KEYPASS_HOST=None,
                 KEYPASS_PORT=None,
                 IOTA_PROTOCOL="http",
                 IOTA_HOST="localhost",
                 IOTA_PORT="4041",
                 ORION_PROTOCOL="http",
                 ORION_HOST="localhost",
                 ORION_PORT="1026",
                 CA_PROTOCOL="http",
                 CA_HOST="localhost",
                 CA_PORT="9999",
                 CYGNUS_PROTOCOL="http",
                 CYGNUS_HOST="localhost",
                 CYGNUS_PORT="5050",
                 STH_PROTOCOL="http",
                 STH_HOST="localhost",
                 STH_PORT="8666",
                 PERSEO_PROTOCOL="http",
                 PERSEO_HOST="localhost",
                 PERSEO_PORT="9090"):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL,
                                 KEYSTONE_HOST,
                                 KEYSTONE_PORT)

        self.ac = AccCOperations(KEYPASS_PROTOCOL,
                                 KEYPASS_HOST,
                                 KEYPASS_PORT)

        self.iota = IoTAOperations(IOTA_PROTOCOL,
                                   IOTA_HOST,
                                   IOTA_PORT)

        self.cb = CBOperations(ORION_PROTOCOL,
                               ORION_HOST,
                               ORION_PORT)
        if CA_PROTOCOL:
            self.ca_endpoint = CA_PROTOCOL + "://"+CA_HOST+":"+CA_PORT+"/v1"
        if CYGNUS_PROTOCOL:
            self.cygnus_endpoint = CYGNUS_PROTOCOL + "://"+CYGNUS_HOST+":"+CYGNUS_PORT+""
        if STH_PROTOCOL:
            self.sth_endpoint = STH_PROTOCOL + "://"+STH_HOST+":"+STH_PORT+""
        if PERSEO_PROTOCOL:
            self.perseo_endpoint = PERSEO_PROTOCOL + "://"+PERSEO_HOST+":"+PERSEO_PORT+""


    def composeErrorCode(self, ex):
        '''
        Compose error detail and code from AssertionError exception ex
        '''
        # Get line where exception was produced
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        res = {"error": str(ex), "code": 400}
        if isinstance(ex.args, tuple) and (
            not isinstance(ex.args[0], tuple)):  # Python 2.6
            res['code'] = ex.args[0]
            if res['code'] == 400 and len(ex.args) > 1 and \
               ex.args[1].startswith('SPASSWORD'):
                res['error'] = ex.args[1]
        elif isinstance(ex.message, tuple):  # Python 2.7
            res['code'] = ex.message[0]
            if res['code'] == 400 and len(ex.message) > 1 and \
               ex.message[1].startswith('SPASSWORD'):
                res['error'] = ex.message[1]
        return res
