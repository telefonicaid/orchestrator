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
import json
import os

from orchestrator.common.util import RestOperations
from orchestrator.core import policies
from orchestrator.core.ac import AccCOperations


class AccCKeypassOperations(AccCOperations):
    '''
       IoT Access Control: Keypass
    '''
    def __init__(self,
                 KEYPASS_PROTOCOL=None,
                 KEYPASS_HOST=None,
                 KEYPASS_PORT=None):

        self.KEYPASS_PROTOCOL = KEYPASS_PROTOCOL
        self.KEYPASS_HOST = KEYPASS_HOST
        self.KEYPASS_PORT = KEYPASS_PORT

        self.AccessControlRestOperations = RestOperations(KEYPASS_PROTOCOL,
                                                          KEYPASS_HOST,
                                                          KEYPASS_PORT)

        self.policy_dir = os.path.dirname(policies.__file__)

    def checkAccC(self):
        res = self.AccessControlRestOperations.rest_request(
            url='/pap/v1/subject/',
            method='GET',
            data=None)
        assert res.code == 404, (res.code, res.msg)

    def provisionPolicy(self,
                        SERVICE_NAME,
                        SERVICE_ADMIN_TOKEN,
                        SUB_SERVICE_ROLE_ID,
                        POLICY_FILE_NAME):

        xml_data = open(self.policy_dir + '/' + POLICY_FILE_NAME)
        body_data = xml_data.read()
        xml_data.close()
        self.provisionPolicyByContent(SERVICE_NAME,
                                      SERVICE_ADMIN_TOKEN,
                                      SUB_SERVICE_ROLE_ID,
                                      body_data)

    def provisionPolicyByContent(self,
                                 SERVICE_NAME,
                                 SERVICE_ADMIN_TOKEN,
                                 SUB_SERVICE_ROLE_ID,
                                 POLICY_CONTENT):

        res = self.AccessControlRestOperations.rest_request(
            url='pap/v1/subject/'+SUB_SERVICE_ROLE_ID,
            method='POST',
            json_data=False,
            data=POLICY_CONTENT,
            auth_token=SERVICE_ADMIN_TOKEN,
            fiware_service=SERVICE_NAME)

        assert res.code == 201, (res.code, res.msg)
        # TODO: return ?

    def deleteTenantPolicies(self,
                             SERVICE_NAME,
                             SERVICE_ADMIN_TOKEN):

        res = self.AccessControlRestOperations.rest_request(
            url='pap/v1',
            method='DELETE',
            json_data=False,
            auth_token=SERVICE_ADMIN_TOKEN,
            fiware_service=SERVICE_NAME)

        assert res.code == 204, (res.code, res.msg)


