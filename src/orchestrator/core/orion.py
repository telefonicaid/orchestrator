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
import logging

from orchestrator.common.util import RestOperations
from orchestrator.core.cb import CBOperations

logger = logging.getLogger('orchestrator_core')

class CBOrionOperations(object):
    '''
       IoT platform: Orion Context Broker
    '''

    def __init__(self,
                 CB_PROTOCOL=None,
                 CB_HOST=None,
                 CB_PORT=None):

        self.CB_PROTOCOL = CB_PROTOCOL
        self.CB_HOST = CB_HOST
        self.CB_PORT = CB_PORT

        self.CBRestOperations = RestOperations(CB_PROTOCOL,
                                               CB_HOST,
                                               CB_PORT)


    def checkCB(self):
        res = self.CBRestOperations.rest_request(
            url='/v1/contextEntities',
            method='GET',
            data=None)
        assert res.code == 404, (res.code, res.msg)
        pass


    def registerContext(self,
                        SERVICE_USER_TOKEN,
                        SERVICE_NAME,
                        SUBSERVICE_NAME,
                        ENTITIES=[],
                        ATTRIBUTES=[],
                        APP="",
                        DURATION="P1M"):
        body_data = {
            "contextRegistrations": [
                {
                    "entities": ENTITIES,
                    "attributes": ATTRIBUTES,
                    "providingApplication": APP
                }
            ],
            "duration": DURATION
        }

        logger.debug("POST to /v1/registry/registerContext with: %s" % json.dumps(body_data,
                                                                                  indent=3))
        res = self.CBRestOperations.rest_request(
            url='/v1/registry/registerContext',
            method='POST',
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


    def updateContext(self,
                      SERVICE_USER_TOKEN,
                      SERVICE_NAME,
                      SUBSERVICE_NAME,
                      ENTITY_TYPE,
                      ENTITY_ID,
                      ACTION="APPEND",
                      IS_PATTERN="false",
                      ATTRIBUTES=[]):

        body_data = {
            "contextElements": [
                {
                    "type": ENTITY_TYPE,
                    "id": ENTITY_ID,
                    "isPattern": IS_PATTERN,
                    "attributes": ATTRIBUTES
                }
            ],
            "updateAction": ACTION
        }

        logger.debug("POST to /v1/updateContext with: %s" % json.dumps(body_data,
                                                                       indent=3))
        res = self.CBRestOperations.rest_request(
            url='/v1/updateContext',
            method='POST',
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


    def getContextTypes(self,
                        SERVICE_USER_TOKEN,
                        SERVICE_NAME,
                        SUBSERVICE_NAME,
                        ENTITY_TYPE=None):

        res = self.CBRestOperations.rest_request(
            url='/v1/contextTypes/%s?offset=0&limit=1000' % (
                ENTITY_TYPE if ENTITY_TYPE else ""),            
            method='GET',
            data=None,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        if 'statusCode' in json_body_response:
            return []
        else:
            return json_body_response


    def subscribeContext(self,
                         SERVICE_USER_TOKEN,
                         SERVICE_NAME,
                         SUBSERVICE_NAME,
                         REFERENCE_URL,
                         DURATION="P50Y",
                         ENTITIES=[],
                         ATTRIBUTES=[],
                         NOTIFY_CONDITIONS=[]):
        body_data = {
            "entities": ENTITIES,
            "attributes": ATTRIBUTES,
            "reference": REFERENCE_URL, # like http://<sth.host>:<sth.port>/notify
            "duration": DURATION,
            "notifyConditions": NOTIFY_CONDITIONS
        }
        logger.debug("POST to /v1/subscribeContext with: %s" % json.dumps(body_data,
                                                                          indent=3))

        #TODO: v1/registry/subscribeContextAvailability ?
        res = self.CBRestOperations.rest_request(
            url='/v1/subscribeContext',
            method='POST',
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


    def unsubscribeContext(self,
                           SERVICE_USER_TOKEN,
                           SERVICE_NAME,
                           SUBSERVICE_NAME,
                           SUBSCRIPTION_ID):
        body_data = {
            "subscriptionId": SUBSCRIPTION_ID
        }

        logger.debug("POST to /v1/unsubscribeContext with : %s" % json.dumps(body_data,
                                                                             indent=3))

        res = self.CBRestOperations.rest_request(
            url='/v1/unsubscribeContext',
            method='POST',
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

    def getContextEntity(self,
                         SERVICE_USER_TOKEN,
                         SERVICE_NAME,
                         SUBSERVICE_NAME,
                         ENTITY_ID):

        res = self.CBRestOperations.rest_request(
            url='/v1/contextEntities/%s' % ENTITY_ID ,
            method='GET',
            data=None,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response

    def getListSubscriptions(self,
                             SERVICE_USER_TOKEN,
                             SERVICE_NAME,
                             SUBSERVICE_NAME,
                             ENTITY_ID=None):

        res = self.CBRestOperations.rest_request(
            url='/v2/subscriptions?offset=0&limit=1000',
            method='GET',
            data=None,
            auth_token=SERVICE_USER_TOKEN,
            fiware_service=SERVICE_NAME,
            fiware_service_path='/'+SUBSERVICE_NAME)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        subscriptions_related = []
        # Filter over list of subscriptions returned
        for subscription in json_body_response:
            for entity in subscription['subject']['entities']:
                if not entity['idPattern'] and entity['id'] == ENTITY_ID:
                    subscriptions_related.append(subscription)
                if entity['idPattern'] and entity['idPattern'] in [".*", "*"]:
                    subscriptions_related.append(subscription)

        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return subscriptions_related


    def deleteAllSubscriptions(self,
                               SERVICE_USER_TOKEN,
                               SERVICE_NAME,
                               SUBSERVICE_NAME):

        subscriptions_deleted = []
        logger.debug("Getting subscriptions for %s  %s" % (SERVICE_NAME,
                                                           SUBSERVICE_NAME))
        try:
            subscriptions = self.getListSubscriptions(SERVICE_USER_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)
        except Exception, ex:
            logger.error("%s trying getListSubscriptions from CB: %s/%s" % (ex,
                                SERVICE_NAME,
                                SUBSERVICE_NAME))
            return subscriptions_deleted

        for subscription in subscriptions:
            try:
                self.unsubscribeContext(SERVICE_USER_TOKEN,
                                        SERVICE_NAME,
                                        SUBSERVICE_NAME,
                                        subscription['id'])
                subscriptions_deleted.append(subscription['id'])
            except Exception, ex:
                logger.error("%s trying to unsubscribe context: %s" % (ex,
                                                        subscription['id']))
        return subscriptions_deleted
