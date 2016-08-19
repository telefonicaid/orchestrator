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
import logging

from orchestrator.common.util import RestOperations

logger = logging.getLogger('orchestrator_core')

class PerseoOperations(object):
    '''
       IoT platform: Perseo rules
    '''

    def __init__(self,
                 PERSEO_PROTOCOL=None,
                 PERSEO_HOST=None,
                 PERSEO_PORT=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):

        self.PERSEO_PROTOCOL = PERSEO_PROTOCOL
        self.PERSEO_HOST = PERSEO_HOST
        self.PERSEO_PORT = PERSEO_PORT

        self.PerseoRestOperations = RestOperations("PERSEO",
                                                   PERSEO_PROTOCOL,
                                                   PERSEO_HOST,
                                                   PERSEO_PORT,
                                                   CORRELATOR_ID,
                                                   TRANSACTION_ID)


    def checkPERSEO(self):
        res = self.PerseoRestOperations.rest_request(
            url='/perseo-core/rules',
            method='GET',
            data=None)
        assert res.code == 404, (res.code, res.msg)
        pass


    def deleteAllRules(self,
                       SERVICE_USER_TOKEN,
                       SERVICE_NAME,
                       SUBSERVICE_NAME):

        # GET all rules: /perseo-core/rules
        body_data = {}
        logger.debug("GET %s/%s to /perseo-core/rules" % (
            SERVICE_NAME,
            SUBSERVICE_NAME))
        res = self.PerseoRestOperations.rest_request(
            url='/perseo-core/rules',
            method='GET',
            data=body_data,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        # TODO:
        # res['name']
        for rule in res:
            # DELETE /perseo-core/rules/{name}: remvoes a rule

            logger.debug("DELETE %s/%s to /perseo-core/rules/{name} with: %s" % (
                SERVICE_NAME,
                SUBSERVICE_NAME,
                rule['name'])
            )
            res = self.PerseoRestOperations.rest_request(
                url='/perseo-core/rules/'+ rule['name'],
                method='DELETE',
                data=body_data,
                auth_token=SERVICE_USER_TOKEN,
                fiware_service=SERVICE_NAME,
                fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response
