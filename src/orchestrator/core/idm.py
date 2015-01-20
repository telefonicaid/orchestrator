import json

from orchestrator.common.util import RestOperations

class IdMOperations(object):
    '''
       IoT IdM (keystone + keypass)
    '''

    def __init__(self,
                 KEYSTONE_PROTOCOL=None,
                 KEYSTONE_HOST=None,
                 KEYSTONE_PORT=None,
                 KEYPASS_PROTOCOL=None,
                 KEYPASS_HOST=None,
                 KEYPASS_PORT=None
             ):

        self.KEYSTONE_PROTOCOL=KEYSTONE_PROTOCOL
        self.KEYSTONE_HOST=KEYSTONE_HOST
        self.KEYSTONE_PORT=KEYSTONE_PORT
        self.KEYPASS_PROTOCOL=KEYPASS_PROTOCOL
        self.KEYPASS_HOST=KEYPASS_HOST
        self.KEYPASS_PORT=KEYPASS_PORT
        self.base_url = KEYSTONE_PROTOCOL+'://'+KEYSTONE_HOST+':'+KEYSTONE_PORT+'/'

        self.RestOperations = RestOperations(KEYSTONE_PROTOCOL,
                                             KEYSTONE_HOST,
                                             KEYSTONE_PORT,
                                             KEYPASS_PROTOCOL,
                                             KEYPASS_HOST,
                                             KEYPASS_PORT)
        
    # def rest_request(self, url, method, user=None, password=None,
    #                  data=None, json_data=True, relative_url=True,
    #                  auth_token=None, fiware_service=None):
    #     '''Does an (optionally) authorized REST request with optional JSON data.

    #     In case of HTTP error, the exception is returned normally instead of
    #     raised and, if JSON error data is present in the response, .msg will
    #     contain the error detail.'''
    #     user = user or None
    #     password = password or None

    #     if relative_url:
    #         # Create real url
    #         url = self.base_url + url

    #     if data:
    #         if json_data:
    #             request = urllib2.Request(
    #                 url, data=json.dumps(data))
    #         else:
    #             request = urllib2.Request(url, data=data)
    #     else:
    #         request = urllib2.Request(url)
    #     request.get_method = lambda: method

    #     if json_data:
    #         request.add_header('Accept', 'application/json')
    #         request.add_header('Content-Type', 'application/json')
    #     else:
    #         request.add_header('Accept', 'application/xml')
    #         request.add_header('Content-Type', 'application/xml')

    #     if user and password:
    #         base64string = base64.encodestring(
    #         '%s:%s' % (user, password))[:-1]
    #         authheader = "Basic %s" % base64string
    #         request.add_header("Authorization", authheader)

    #     if auth_token:
    #         request.add_header('X-Auth-Token', auth_token)

    #     if fiware_service:
    #         request.add_header('Fiware-Service', fiware_service)

    #     res = None

    #     try:
    #         res = urllib2.urlopen(request)
    #     except urllib2.HTTPError, e:
    #         res = e
    #         data = res.read()
    #         try:
    #             data_json = json.loads(data)
    #             res.raw_json = data_json
    #             if data_json and 'detail' in data_json:
    #                 res.msg = data_json['detail']
    #         except ValueError:
    #             res.msg = data
    #         except Exception, e:
    #             print e

    #     return res


    def getToken(self,
                 DOMAIN_NAME,
                 DOMAIN_ADMIN_USER,
                 DOMAIN_ADMIN_PASSWORD):

        auth_data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": DOMAIN_NAME,
                        },
                        "name": DOMAIN_ADMIN_USER,
                        "password": DOMAIN_ADMIN_PASSWORD
                    }
                }
            },
            "scope": {
                "domain": {
                    "name": DOMAIN_NAME
                }
            }
        }
        }
        res = self.RestOperations.rest_request(url='/v3/auth/tokens',
                                method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')


    def createDomain(self,
                     CLOUD_ADMIN_TOKEN,
                     NEW_SERVICE_NAME,
                     NEW_SERVICE_DESCRIPTION):

        body_data = {
            "domain": {
                "enabled": True,
                "name": "%s" % NEW_SERVICE_NAME,
                "description": "%s" % NEW_SERVICE_DESCRIPTION
            }
        }
        res = self.RestOperations.rest_request(url='/v3/domains',
                                method='POST', data=body_data,
                                auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['domain']['id']


    def createUserAdminDomain(self,
                              CLOUD_ADMIN_TOKEN,
                              NEW_SERVICE_NAME,
                              ID_DOM1,
                              NEW_SERVICE_ADMIN_USER,
                              NEW_SERVICE_ADMIN_PASSWORD):
        body_data = {
            "user": {
                "description": "Administrator of domain %s" % NEW_SERVICE_NAME,
                "domain_id": "%s" % ID_DOM1,
                "enabled": True,
                "name": "%s" % NEW_SERVICE_ADMIN_USER,
                "password": "%s" % NEW_SERVICE_ADMIN_PASSWORD
            }
        }
        res = self.RestOperations.rest_request(url='/v3/users',
                                method='POST', data=body_data,
                                auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['user']['id']


    def getRoleId(self,
                 CLOUD_ADMIN_TOKEN,
                 ROLE_NAME):
        res = self.RestOperations.rest_request(url='/v3/roles?name=%s' % ROLE_NAME,
                                method='GET',
                                auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        # TODO ensure ADMIN_ROLE_ID?
        return json_body_response['roles'][0]['id']


    def grantDomainRole(self,
                      CLOUD_ADMIN_TOKEN,
                      ID_DOM1,
                      ID_ADM1,
                      ADMIN_ROLE_ID):
        res = self.RestOperations.rest_request(url='/v3/domains/%s/users/%s/roles/%s' % (
                                ID_DOM1, ID_ADM1, ADMIN_ROLE_ID),
                                method='PUT',
                                auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)


    def createDomainRole(self,
                        SERVICE_ADMIN_TOKEN,
                        SUB_SERVICE_ROLE_NAME,
                        ID_DOM1):
        body_data = {
            "schemas": ["urn:scim:schemas:extension:keystone:1.0"],
            "name": "%s" % SUB_SERVICE_ROLE_NAME,
            "domain_id": "%s" % ID_DOM1
        }
        res = self.RestOperations.rest_request(url='/v3/OS-SCIM/Roles',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['id']


    def provisionPolicy(self,
                        SERVICE_NAME,
                        SERVICE_ADMIN_TOKEN,
                        SUB_SERVICE_ROLE_ID,
                        POLICY_FILE_NAME):
        xml_data = open(POLICY_FILE_NAME)
        body_data = xml_data.read()
        xml_data.close()
        keypassurl = "%s://%s:%s" % (self.KEYPASS_PROTOCOL, self.KEYPASS_HOST,
                               self.KEYPASS_PORT)
        res = self.RestOperations.rest_request(url=keypassurl+'/pap/v1/subject/'+SUB_SERVICE_ROLE_ID,
                                relative_url=False,
                                method='POST',
                                json_data=False,
                                data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN,
                                fiware_service=SERVICE_NAME)

        assert res.code == 201, (res.code, res.msg)


    def createProject(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      NEW_SUBSERVICE_NAME,
                      NEW_SUBSERVICE_DESCRIPTION):

        body_data = {
            "project": {
                "enabled": True,
                "domain_id": "%s" % ID_DOM1,
                "name": "/%s" % NEW_SUBSERVICE_NAME,
                "description": "%s" % NEW_SUBSERVICE_DESCRIPTION
            }
        }
        res = self.RestOperations.rest_request(url='/v3/projects',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['domain']['id']


    def getDomainId(self, SERVICE_ADMIN_TOKEN, DOMAIN_NAME):

        auth_data = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": SERVICE_ADMIN_TOKEN
                }
            },
            "scope": {
                "domain": {
                    "name": DOMAIN_NAME
                }
            }
        }
        }
        res = self.RestOperations.rest_request(url='/v3/auth/tokens',
                                method='POST', data=auth_data)
        

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['token']['user']['domain']['id']

    def createUserDomain(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      SERVICE_NAME,
                      NEW_USER_NAME,
                      NEW_USER_PASSWORD):

        body_data = {
            "user": {
                "description": "user of domain" % SERVICE_NAME,
                "enabled": True,
                "domain_id": "%s" % ID_DOM1,
                "name": "/%s" % NEW_USER_NAME,
                "password": "/%s" % NEW_USER_PASSWORD,
            }
        }
        res = self.RestOperations.rest_request(url='/v3/users',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['user']['id']


    def createRoleDomain(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      NEW_ROLE_NAME):

        body_data = {
                "enabled": "\[\"urn:scim:schemas:extension:keystone:1.0\"\]",  # TODO: check this string!
                "domain_id": "%s" % ID_DOM1,
                "name": "/%s" % NEW_ROLE_NAME,
        }
        res = self.RestOperations.rest_request(url='/v3/OS-SCIM/Roles',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['id']
