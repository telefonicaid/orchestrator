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
import json
import logging

from orchestrator.common.util import RestOperations

logger = logging.getLogger('orchestrator_core')


class SplunkOperations(object):
    '''
       IoT platform: Splunk
    '''

    def __init__(self,
                 SPLUNK_PROTOCOL=None,
                 SPLUNK_HOST=None,
                 SPLUNK_PORT=None,
                 SPLUNK_USER=None,
                 SPLUNK_PASSWORD=None,                 
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):

        self.SPLUNK_PROTOCOL = SPLUNK_PROTOCOL
        self.SPLUNK_HOST = SPLUNK_HOST
        self.SPLUNK_PORT = SPLUNK_PORT
        self.SPLUNK_USER = SPLUNK_USER
        self.SPLUNK_PASSWORD = SPLUNK_PASSWORD        

        self.SplunkRestOperations = RestOperations("SPLUNK",
                                                   SPLUNK_PROTOCOL,
                                                   SPLUNK_HOST,
                                                   SPLUNK_PORT,
                                                   CORRELATOR_ID,
                                                   TRANSACTION_ID)     

    def checkSplunk(self):
        res = self.SplunkRestOperations.rest_request(
            url='/services/search',
            method='GET',
            user=self.SPLUNK_USER,
            password=self.SPLUNK_PASSWORD,
            data=None)

        assert res.code == 200, (res.code, res.msg)
        pass

    def searchRelevant(self,
                       SERVICE_NAME,
                       SUBSERVICE_NAME,
                       COMPONENT,
                       LOGLEVEL,
                       CUSTOMTEXT):
        
        search_data = "search "

        if (SERVICE_NAME):
            search_data += " srv=%s" % SERVICE_NAME
        if (SUBSERVICE_NAME):
            search_data += " subsrv=%s" % SUBSERVICE_NAME                     
        if (LOGLEVEL):
            search_data += " lvl=%s" % LOGLEVEL
        if (COMPONENT):
            search_data += " comp=%s" % COMPONENT
        if (CUSTOMTEXT):
            search_data += " %s" % CUSTOMTEXT

        logger.debug("searchRelevant with: %s " % search_data)

        res = self.SplunkRestOperations.rest_request(
            url='/servicesNS/admin/search/search/jobs/export?output_mode=json',
            method='POST',
            user=self.SPLUNK_USER,
            password=self.SPLUNK_PASSWORD,
            json_data=False,
            data=search_data)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                          indent=3))
        return json_body_response
