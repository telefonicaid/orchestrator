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

class CBOrionOperations(object):
    '''
       IoT platform: Orion Context Broker
    '''

    def __init__(self,
                 CB_PROTOCOL=None,
                 CB_HOST=None,
                 CB_PORT=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):

        self.CB_PROTOCOL = CB_PROTOCOL
        self.CB_HOST = CB_HOST
        self.CB_PORT = CB_PORT

        self.CBRestOperations = RestOperations("ORION",
                                               CB_PROTOCOL,
                                               CB_HOST,
                                               CB_PORT,
                                               CORRELATOR_ID,
                                               TRANSACTION_ID)


    def checkCB(self):
        res = self.CBRestOperations.rest_request(
            url='/version',
            method='GET',
            data=None)
        # Expecting also headers about
        #  fiware-service, fiware-servicepath and x-auth-token
        assert res.code == 400, (res.code, res.msg)
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

        logger.debug("POST %s/%s to /v1/registry/registerContext with: %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME,
            json.dumps(body_data, indent=3))
        )
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

        logger.debug("POST %s/%s to /v1/updateContext with: %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME,
            json.dumps(body_data, indent=3))
        )
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

        logger.debug("Getting ContextTyesy for %s %s %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME,
            ENTITY_TYPE)
        )
        res = self.CBRestOperations.rest_request(
            url='/v1/contextTypes%s?details=on&offset=0&limit=1000' % (
                '/' + ENTITY_TYPE if ENTITY_TYPE else ""),
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
            if (int(json_body_response['statusCode']['code']) != 200):
                return []

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
        logger.debug("POST %s/%s to /v1/subscribeContext with: %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME,
            json.dumps(body_data, indent=3))
        )

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

        logger.debug("POST %s/%s to /v1/unsubscribeContext with: %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME,
            json.dumps(body_data, indent=3))
        )

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
        logger.debug("Getting ContextEntity for %s %s %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME,
            ENTITY_ID)
        )
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

        logger.debug("Getting subscriptions for %s %s %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME,
            ENTITY_ID)
        )
        offset = 0
        page = 40
        fiware_total_count = page
        subscriptions_related = []

        while (offset + page <= fiware_total_count):
            url='/v2/subscriptions?offset=%s&limit=%s&options=count' % (offset, page)
            res = self.CBRestOperations.rest_request(
                url=url,
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

            # ensure subcrtiptions is an array
            if isinstance(json_body_response, list):
                for subscription in json_body_response:
                    for entity in subscription['subject']['entities']:
                        if ( ((not 'idPattern' in entity) or
                              ('idPattern' in entity and not entity['idPattern'])) and
                             entity['id'] == ENTITY_ID):
                            subscriptions_related.append(subscription)
                        if ('idPattern' in entity and entity['idPattern'] and
                            entity['idPattern'] in [".*", "*"]):
                            subscriptions_related.append(subscription)

            fiware_total_count = int(res.headers.get('Fiware-Total-Count', 0))
            offset += page

        return subscriptions_related


    def deleteAllSubscriptions(self,
                               SERVICE_USER_TOKEN,
                               SERVICE_NAME,
                               SUBSERVICE_NAME=""):

        subscriptions_deleted = []
        logger.debug("Removing all subscriptions for %s %s" % (
            SERVICE_NAME,
            SUBSERVICE_NAME)
        )
        try:
            subscriptions = self.getListSubscriptions(SERVICE_USER_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)
            logger.debug("subscriptions: %s" % json.dumps(subscriptions,
                                                          indent=3))
        except Exception, ex:
            logger.warn("%s trying getListSubscriptions from CB: %s/%s" % (ex,
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
                logger.warn("%s trying to unsubscribe context: %s" % (ex,
                                                        subscription['id']))
        return subscriptions_deleted

    def extractModulesFromSubscriptions(self,
                                           flow,
                                           iot_modules,
                                           subscriptions):
        modules = []
        for sub in subscriptions:
            if "notification" in sub:
                sub_callback = self.getSubscriptionCallbackEndpoint(sub)
                for iotmodule in iot_modules:
                    if sub_callback.startswith(
                        flow.getEndpointIotModule(iotmodule)):
                        if ((len(sub['subject']['entities']) == 1) and
                            ('idPattern' in sub['subject']['entities'][0] and
                             sub['subject']['entities'][0]['idPattern'] == '.*') and
                            ( ('type' in sub['subject']['entities'][0] and
                               sub['subject']['entities'][0]['type'] == '') or
                              'type' not in sub['subject']['entities'][0])):
                            modules.append(
                                { "name": iotmodule,
                                  "subscriptionid": sub['id'],
                                  "alias": flow.getAliasIotModule(iotmodule)
                              })
                            break

        return modules

    def getSubscriptionCallbackEndpoint(self, sub):
        sub_callback = ""
        if "notification" in sub:
            if "callback" in sub["notification"]:
                sub_callback = sub["notification"]["callback"]
            else:  # From Orion 1.1.0
                if "http" in sub["notification"]:
                    sub_callback = sub["notification"]["http"]["url"]

        return sub_callback
