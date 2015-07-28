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


class RestOperations(object):
    '''
       IoT IdM (keystone + keypass)
    '''

    def __init__(self,
                 PROTOCOL=None,
                 HOST=None,
                 PORT=None):

        self.PROTOCOL = PROTOCOL
        self.HOST = HOST
        self.PORT = PORT
        if PROTOCOL and HOST and PORT:
            self.base_url = PROTOCOL+'://'+HOST+':'+PORT
        else:
            self.base_url = None

    def rest_request(self, url, method, user=None, password=None,
                     data=None, json_data=True, relative_url=True,
                     auth_token=None, fiware_service=None, fiware_service_path=None):
        '''Does an (optionally) authorized REST request with optional JSON data.

        In case of HTTP error, the exception is returned normally instead of
        raised and, if JSON error data is present in the response, .msg will
        contain the error detail.'''
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
            request.add_header('Content-Type', 'application/json')
        else:
            request.add_header('Accept', 'application/xml')
            request.add_header('Content-Type', 'application/xml')

        if user and password:
            base64string = base64.encodestring(
                '%s:%s' % (user, password))[:-1]
            authheader = "Basic %s" % base64string
            request.add_header("Authorization", authheader)

        if auth_token:
            request.add_header('X-Auth-Token', auth_token)

        if fiware_service:
            request.add_header('Fiware-Service', fiware_service)

        if fiware_service_path:
            request.add_header('Fiware-ServicePath', fiware_service_path)

        res = None

        try:
            res = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            res = e
            data = res.read()
            try:
                data_json = json.loads(data)
                res.raw_json = data_json
                if data_json and 'detail' in data_json:
                    res.msg = data_json['detail']
                if data_json and 'error' in data_json:
                    if 'message' in data_json['error']:
                        res.msg = data_json['error']['message']
            except ValueError:
                res.msg = data
            except Exception, e:
                print e

        return res
