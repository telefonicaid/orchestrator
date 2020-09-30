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
import urllib2
import base64
import json
import csv
import StringIO
import requests
import logging
import time
from settings import dev as settings

class RestOperations(object):
    '''
       IoT IdM (keystone + keypass)
    '''

    def __init__(self,
                 ENDPOINT_NAME="",
                 PROTOCOL=None,
                 HOST=None,
                 PORT=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):

        self.ENDPOINT_NAME = ENDPOINT_NAME
        self.PROTOCOL = PROTOCOL
        self.HOST = HOST
        self.PORT = PORT
        if PROTOCOL and HOST and PORT:
            self.base_url = PROTOCOL+'://'+HOST+':'+PORT
        else:
            self.base_url = None

        if TRANSACTION_ID:
            self.TRANSACTION_ID = TRANSACTION_ID
        else:
            self.TRANSACTION_ID = None

        if CORRELATOR_ID:
            self.CORRELATOR_ID = CORRELATOR_ID
        else:
            self.CORRELATOR_ID = None

        self.logger = logging.getLogger('orchestrator_core')
        self.logger.addFilter(ContextFilterCorrelatorId(self.CORRELATOR_ID))
        self.logger.addFilter(ContextFilterTransactionId(self.TRANSACTION_ID))

        self.service = {}
        self.sum = {
            "serviceTime": 0,
            "serviceTimeTotal": 0,
            "outgoingTransactions": 0,
            "outgoingTransactionRequestSize": 0,
            "outgoingTransactionResponseSize": 0,
            "outgoingTransactionErrors": 0,
        }



    def rest_request(self, url, method, user=None, password=None,
                     data=None, json_data=True, relative_url=True,
                     auth_token=None, subject_token=None, fiware_service=None,
                     fiware_service_path=None):
        '''Does an (optionally) authorized REST request with optional JSON data.

        In case of HTTP error, the exception is returned normally instead of
        raised and, if JSON error data is present in the response, .msg will
        contain the error detail.'''
        service_start = time.time()
        user = user or None
        password = password or None

        if relative_url:
            # Create real url
            url = self.base_url + url

        if data:
            if json_data:
                request = urllib2.Request(
                    url, data=json.dumps(data))
            else:
                request = urllib2.Request(url, data=data)
        else:
            request = urllib2.Request(url)
        request.get_method = lambda: method

        if json_data:
            request.add_header('Accept', 'application/json')
            if data:
                request.add_header('Content-Type', 'application/json')
        else:
            request.add_header('Accept', 'application/xml')
            if data:
                request.add_header('Content-Type', 'application/xml')

        if user and password:
            base64string = base64.encodestring(
                '%s:%s' % (user, password))[:-1]
            authheader = "Basic %s" % base64string
            request.add_header("Authorization", authheader)

        if auth_token:
            request.add_header('X-Auth-Token', auth_token)

        if subject_token:
            request.add_header('X-Subject-Token', subject_token)

        if fiware_service:
            request.add_header('Fiware-Service', fiware_service)

        if fiware_service_path:
            request.add_header('Fiware-ServicePath', fiware_service_path)

        if self.TRANSACTION_ID:
            request.add_header('Fiware-Transaction', self.TRANSACTION_ID)

        if self.CORRELATOR_ID:
            request.add_header('Fiware-Correlator', self.CORRELATOR_ID)

        res = None

        try:
            res = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            res = e
            data = res.read()
            try:
                data_json = json.loads(data)
                res.raw_json = data_json
                if data_json and isinstance(data_json, dict) and \
                    'detail' in data_json:
                    res.msg = data_json['detail']
                if data_json and isinstance(data_json, dict) and \
                    'error' in data_json:
                    if data_json['error'] and \
                        isinstance(data_json['error'], dict) and \
                        'message' in data_json['error']:
                        res.msg = data_json['error']['message']
                if data_json and isinstance(data_json, dict) and \
                    'message' in data_json:
                    res.msg = data_json['message']

            except ValueError:
                res.msg = data
            except Exception, e:
                print e
        except urllib2.URLError, e:
            data = None
            res = e
            res.code = 500
            res.msg = self.ENDPOINT_NAME + " endpoint ERROR: " + res.args[0][1]

        if settings.ORC_EXTENDED_METRICS:
            self.collectOutgoingMetrics(service_start, request.data, request.headers, res)
        return res


    def rest_request2(self, url, method, user=None, password=None,
                     data=None, json_data=True, relative_url=True,
                     auth_token=None, subject_token=None, fiware_service=None,
                     fiware_service_path=None):
        '''Does an (optionally) authorized REST request with optional JSON data.

        In case of HTTP error, the exception is returned normally instead of
        raised and, if JSON error data is present in the response, .msg will
        contain the error detail.
        Without SSL security

        '''
        service_start = time.time()
        user = user or None
        password = password or None
        auth = None

        if relative_url:
            # Create real url
            url = self.base_url + url

        headers = {}
        rdata = None

        if json_data:
            headers.update({'Accept': 'application/json'})
            if data:
                headers.update({'Content-Type': 'application/json'})
                rdata = json.dumps(data)
        else:
            headers.update({'Accept': 'application/xml'})
            if data:
                headers.update({'Content-Type': 'application/xml'})
                rdata = data


        if user and password:
            # base64string = base64.encodestring(
            #     '%s:%s' % (user, password))[:-1]
            # authheader = "Basic %s" % base64string
            # headers.update({'Authorization': authheader})
            auth=(user, password)

        if auth_token:
            headers.update({'X-Auth-Token': auth_token })

        if subject_token:
            headers.update({'X-Subject-Token': subject_token })

        if fiware_service:
            headers.update({'Fiware-Service': fiware_service})

        if fiware_service_path:
            headers.update({'Fiware-ServicePath': fiware_service_path})

        if self.TRANSACTION_ID:
            headers.update({'Fiware-Transaction': self.TRANSACTION_ID})

        if self.CORRELATOR_ID:
            headers.update({'Fiware-Correlator': self.CORRELATOR_ID})

        res = None

        try:
            if not auth:
                res = requests.post(url,
                                    headers=headers,
                                    data=rdata,
                                    verify=False)
            else:
                res = requests.post(url,
                                    auth=auth,
                                    headers=headers,
                                    data=rdata,
                                    verify=False)

        except Exception, e:
            print e

        if settings.ORC_EXTENDED_METRICS:
            self.collectOutgoingMetrics(service_start, rdata, headers, res)
        return res


    def collectOutgoingMetrics(self, service_start, data_request, headers_request, response):
        try:
            service_stop = time.time()
            transactionError = False
            if response.code not in [200, 201, 204]:
                transactionError = True
            data_response = response.msg
            if transactionError:
                self.sum["outgoingTransactions"] += 1
            else:
                self.sum["outgoingTransactionErrors"] += 1
            self.sum["outgoingTransactionRequestSize"] += len(json.dumps(data_request)) + len(str(headers_request))
            # Check headers
            self.sum["outgoingTransactionResponseSize"] += len(json.dumps(data_response)) + len(str(response.headers.headers)) if 'headers' in response and 'headers' in response.headers else 0
            self.sum["serviceTimeTotal"] += (service_stop - service_start)
        except Exception, ex:
            self.logger.warn("ERROR collecting outgoing metrics %s", ex)

    def getOutgoingMetrics(self):
        return self.sum


class CSVOperations(object):
    '''

    '''

    def __init__(self):
        None

    @staticmethod
    def read_devices(CSV):
        devices = {}
        csvreader = csv.reader(StringIO.StringIO(CSV),
                               delimiter=',',
                               #quotechar='"',
                               skipinitialspace=True)

        header =  csvreader.next()
        for name in header:
            devices[name] = []

        for row in csvreader:
            for i, value in enumerate(row):
                devices[header[i]].append(value)

        return i, header, devices


class ContextFilterTransactionId(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def __init__(self, TRANSACTION_ID):
        self.TRANSACTION_ID = TRANSACTION_ID

    def filter(self, record):
        record.transaction = self.TRANSACTION_ID
        return True


class ContextFilterService(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self, service):
        self.service = service

    def filter(self, record):
        record.service = self.service
        return True


class ContextFilterSubService(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self, subservice):
        self.subservice = subservice

    def filter(self, record):
        record.subservice = self.subservice
        return True


class ContextFilterCorrelatorId(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self, CORRELATOR_ID):
        self.CORRELATOR_ID = CORRELATOR_ID

    def filter(self, record):
        record.correlator = self.CORRELATOR_ID
        return True


class ContextFilterFrom(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self, FROM):
        self.FROM = FROM

    def filter(self, record):
        record.origin = self.FROM
        return True
