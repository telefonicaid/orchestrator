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
            url='/m2m/vrules',
            method='GET',
            data=None)
        assert res.code == 404, (res.code, res.msg)
        pass


    def deleteAllRules(self,
                       SERVICE_USER_TOKEN,
                       SERVICE_NAME,
                       SUBSERVICE_NAME):

        rules_deleted = []
        logger.debug("Getting rules for %s %s" % (SERVICE_NAME,
                                                  SUBSERVICE_NAME))

        try:

            # GET all rules: /perseo-core/rules
            body_data = {}
            logger.debug("GET %s/%s to /m2m/vrules" % (
                SERVICE_NAME,
                SUBSERVICE_NAME))
            res = self.PerseoRestOperations.rest_request(
                url='/m2m/vrules',
                method='GET',
                data=body_data,
                auth_token=SERVICE_USER_TOKEN,
                fiware_service=SERVICE_NAME,
                fiware_service_path='/'+SUBSERVICE_NAME)

            assert res.code == 200, (res.code, res.msg)
            data = res.read()
            rules = json.loads(data)
            logger.debug("rules: %s" % json.dumps(rules, indent=3))

        except Exception, ex:
            logger.warn("%s trying getRules from PERSEO: %s/%s" % (ex,
                                                                    SERVICE_NAME,
                                                                    SUBSERVICE_NAME))
            return rules_deleted

        for rule in rules['data']:
            # DELETE /perseo-core/rules/{name}: removes a rule
            try:
                logger.debug("DELETE %s/%s to /m2m/vrules/{name} with: %s" % (
                    SERVICE_NAME,
                    SUBSERVICE_NAME,
                    rule['name'])
                )
                res = self.PerseoRestOperations.rest_request(
                    url='/m2m/vrules/'+ rule['name'],
                    method='DELETE',
                    data=body_data,
                    auth_token=SERVICE_USER_TOKEN,
                    fiware_service=SERVICE_NAME,
                    fiware_service_path='/'+SUBSERVICE_NAME)
                assert res.code == 204, (res.code, res.msg)
                rules_deleted.append(rule['name'])
            except Exception, ex:
                logger.warn("%s trying to remove rule: %s" % (ex,
                                                               rule['name']))

        return rules_deleted
