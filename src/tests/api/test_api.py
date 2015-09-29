import uuid
import json
from settings import custom_dev as settings

from orchestrator.common.util import RestOperations


# TODO: split TestRestOperations in another file
class TestRestOperations(RestOperations):

    def __init__(self, PROTOCOL, HOST, PORT):
        RestOperations.__init__(self,
                                PROTOCOL,
                                HOST,
                                PORT)
        self.keystone_endpoint_url = settings.KEYSTONE['protocol'] + '://' + \
            settings.KEYSTONE['host'] + ":" + settings.KEYSTONE['port']

    def getToken(self, data):
        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": data["SERVICE_ADMIN_USER"],
                            "password": data["SERVICE_ADMIN_PASSWORD"]
                        }
                    }
                }
            }
        }
        if "SERVICE_NAME" in data:
            auth_data['auth']['identity']['password']['user'].update(
                {"domain": {"name": data["SERVICE_NAME"]}})

            scope_domain = {
                "scope": {
                    "domain": {
                        "name": data["SERVICE_NAME"]
                    }
                }
            }
            auth_data['auth'].update(scope_domain)
        res = self.rest_request(
            url=self.keystone_endpoint_url + '/v3/auth/tokens',
            relative_url=False,
            method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res

    def getScopedToken(self, data):
        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": data["SERVICE_ADMIN_USER"],
                            "password": data["SERVICE_ADMIN_PASSWORD"]
                        }
                    }
                }
            }
        }
        if "SERVICE_NAME" in data and "SUBSERVICE_NAME" in data:
            auth_data['auth']['identity']['password']['user'].update(
                {"domain": {"name": data["SERVICE_NAME"]}})

            scope_domain = {
                "scope": {
                    "project": {
                        "domain": {
                            "name": data["SERVICE_NAME"]
                        },
                        "name": "/" + data["SUBSERVICE_NAME"]
                    }
                }
            }
            auth_data['auth'].update(scope_domain)
        res = self.rest_request(
            url=self.keystone_endpoint_url + '/v3/auth/tokens',
            relative_url=False,
            method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res

    def getUnScopedToken(self, data):
        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": data["SERVICE_ADMIN_USER"],
                            "password": data["SERVICE_ADMIN_PASSWORD"]
                        }
                    }
                }
            }
        }
        if "SERVICE_NAME" in data:
            auth_data['auth']['identity']['password']['user'].update(
                {"domain": {"name": data["SERVICE_NAME"]}})

        res = self.rest_request(
            url=self.keystone_endpoint_url + '/v3/auth/tokens',
            relative_url=False,
            method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res

    def getTrustScopedToken(self, data):
        auth_token=None
        auth_data = { }
        if "SERVICE_ADMIN_USER" in data:
            auth_data = {
                "auth": {
                    "identity": {
                        "methods": [
                            "password"
                            ],
                            "password": {
                                "user": {
                                    "name": data["SERVICE_ADMIN_USER"],
                                    "password": data["SERVICE_ADMIN_PASSWORD"]
                                    }
                                }
                        }
                    }
                }
        if "ID_TOKEN" in data:
            auth_data = {
                "auth": {
                    "identity": {
                        "methods": [
                            "token"
                            ],
                            "token": {
                                "id": data["ID_TOKEN"]
                                }
                        }
                        }
                        }
            auth_token=data["ID_TOKEN"]
        if "SERVICE_NAME" in data and not "SUBSERVICE_NAME" in data:
            auth_data['auth']['identity']['password']['user'].update(
                {"domain": {"name": data["SERVICE_NAME"]}})

        scope_domain = {
                "scope": {
                    "OS-TRUST:trust": {
                        "id": data["ID_TRUST"]
                    },
                }
        }
        auth_data['auth'].update(scope_domain)
        res = self.rest_request(
            url=self.keystone_endpoint_url + '/v3/auth/tokens',
            relative_url=False,
            auth_token=auth_token,
            method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res

    def getServiceId(self, data):
        token_res = self.getToken(data)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        return json_body_response['token']['user']['domain']['id']

    def getSubServiceId(self, data):
        token_res = self.getToken(data)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)

        DOMAIN_ID = json_body_response['token']['user']['domain']['id']

        ADMIN_TOKEN = token_res.headers.get('X-Subject-Token')
        res = self.rest_request(
            url=self.keystone_endpoint_url + '/v3/projects?domain_id=%s' % DOMAIN_ID,
            relative_url=False,
            method='GET', auth_token=ADMIN_TOKEN)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        for project in json_body_response['projects']:
            if project['name'] == '/' + data["SUBSERVICE_NAME"]:
                return project['id']


class Test_NewService_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "DOMAIN_NAME": "admin_domain",
            "DOMAIN_ADMIN_USER": "cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER": "adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD": "4pass1w0rd",
            "NEW_SERVICE_ADMIN_EMAIL": "pepe@tid.es"
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok2 = {
            "DOMAIN_NAME": "admin_domain",
            "DOMAIN_ADMIN_USER": "cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "SERVICE_NAME": "admin_domain",
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER": "adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD": "4pass1w0rd",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "DOMAIN_NAME": "admin_domain",
            "DOMAIN_ADMIN_USER": "cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "wrong_password",
            "NEW_SERVICE_NAME": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER": "adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD": "4pass1w0rd",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad2 = {
            "DOMAIN_NAME": "admin_domain",
            "DOMAIN_ADMIN_USER": "cloud_admin",
            "NEW_SERVICE_NAME": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER": "adm_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        # TOKEN="kk3"
        res = self.TestRestOps.rest_request(method="POST",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            # auth_token=TOKEN,
                                            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok2(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok2)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        TOKEN = json_body_response['token']
        res = self.TestRestOps.rest_request(method="POST",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            auth_token=TOKEN,
                                            data=self.payload_data_ok2)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 409, (res.code, res.msg)

    def test_post_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg)

    def test_post_bad2(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad2)
        assert res.code == 400, (res.code, res.msg)


class Test_DeleteService_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "DOMAIN_NAME": "admin_domain",
            "DOMAIN_ADMIN_USER": "cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER": "adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD": "4pass1w0rd",
            "NEW_SERVICE_ADMIN_EMAIL": "pepe@tid.es",
            "SERVICE_NAME": "smartcity_%s" % self.suffix,
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok2 = {
            "DOMAIN_NAME": "admin_domain",
            "DOMAIN_ADMIN_USER": "cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION": "smartcity_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER": "adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD": "4pass1w0rd",
            "NEW_SERVICE_ADMIN_EMAIL": "pepe@tid.es",
            "SERVICE_NAME": "smartcity_%s" % self.suffix,
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad = {
            "SERVICE_NAME": "smartcity_%s" % self.suffix,
            "SERVICE_ADMIN_USER": "adm_%s" % self.suffix,
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_delete_ok(self):

        res = self.TestRestOps.rest_request(method="POST",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        response = res.read()
        json_body_response = json.loads(response)
        service_id = json_body_response['id']
        res = self.TestRestOps.rest_request(method="DELETE",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

    def test_delete_wrong(self):

        res = self.TestRestOps.rest_request(method="POST",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        response = res.read()
        json_body_response = json.loads(response)
        service_id = json_body_response['id']
        res = self.TestRestOps.rest_request(method="DELETE",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg, res.raw_json)


class Test_NewSubService_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SUBSERVICE_NAME": "Electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "electricidad_%s" % self.suffix,
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SUBSERVICE_NAME": "electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "electricidad_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
            "NEW_SUBSERVICE_NAME": "electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "electricidad_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "NEW_SUBSERVICE_NAME": "electricidad_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        response = res.read()
        json_body_response = json.loads(response)
        subservice_id = json_body_response['id']
        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/subservice/%s" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):

        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        response = res.read()
        json_body_response = json.loads(response)
        subservice_id = json_body_response['id']

        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 409, (res.code, res.msg)

        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/subservice/%s" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

    def test_post_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg)

    def test_post_bad2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_bad2)
        assert res.code == 400, (res.code, res.msg)


class Test_SubServiceIoTADevice_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "SERVICE_USER_NAME": "admin_bb",
            "SERVICE_USER_PASSWORD": "4passw0rd",
            "SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
        }
        self.payload_data2_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "SERVICE_USER_NAME": "admin_bb",
            "SERVICE_USER_PASSWORD": "4passw0rd",
            "SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "DEVICE_ID": "button_dev_sync_%s" % self.suffix,
            "ENTITY_TYPE": "BlackButton",
            "PROTOCOL": "TT_BLACKBUTTON",
            "ATT_CCID": "AAA",
            "ATT_IMEI": "1234567890",
            "ATT_IMSI": "0987654321",
            "ATT_INTERACTION_TYPE": "synchronous",
            "ATT_SERVICE_ID": "blackbutton",
            "ATT_GEOLOCATION": "40.4188,-3.6919",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data3_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "SERVICE_USER_NAME": "admin_bb",
            "SERVICE_USER_PASSWORD": "4passw0rd",
            "DEVICE_ID": "button_dev_async_%s" % self.suffix,
            "ENTITY_TYPE": "BlackButton",
            "PROTOCOL": "TT_BLACKBUTTON",
            "ATT_CCID": "AAA",
            "ATT_IMEI": "1234567890",
            "ATT_IMSI": "0987654321",
            "ATT_INTERACTION_TYPE": "asynchronous",
            "ATT_SERVICE_ID": "blackbutton",
            "ATT_GEOLOCATION": "40.4188,-3.6919",
        }

        self.suffix = str(uuid.uuid4())[:8]
        csv = """DEVICE_ID,ENTITY_TYPE,PROTOCOL,ATT_CCID,ATT_IMEI,ATT_IMSI,ATT_INTERACTION_TYPE,ATT_SERVICE_ID,ATT_GEOLOCATION
                  button_dev_async_%s, BlackButton, TT_BLACKBUTTON, AAA, 1234567890, 0987654321, asynchronous, blackbutton, 0
                  button_dev_sync_%s, BlackButton, TT_BLACKBUTTON, BBB, 2345678902, 2987654322, synchronous, blackbutton, 0"""  % (self.suffix, self.suffix)

        self.payload_data4_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "SERVICE_USER_NAME": "admin_bb",
            "SERVICE_USER_PASSWORD": "4passw0rd",
            "SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "CSV_DEVICES": csv
        }

        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)

        # Create SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok)

        # Register Device in SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/%s/register_device" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data2_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)


    def test_post_ok2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data3_ok)

        # Create SubService and Register Device in SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data3_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok3(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data4_ok)

        # Create SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data4_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data4_ok)

        # Register Device in SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/%s/register_devices" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data4_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

class Test_SubServiceIoTAService_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "SERVICE_USER_NAME": "admin_bb",
            "SERVICE_USER_PASSWORD": "4passw0rd",
            "SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
        }
        self.payload_data2_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "SERVICE_USER_NAME": "admin_bb",
            "SERVICE_USER_PASSWORD": "4passw0rd",
            "SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "DEVICE_ID": "button_dev_%s" % self.suffix,
            "ENTITY_TYPE": "BlackButton",
            "ENTITY_ID": "button_dev_%s" % self.suffix,
            "PROTOCOL": "TT_BLACKBUTTON",
            "ATT_CCID": "AAA",
            "ATT_IMEI": "1234567890",
            "ATT_IMSI": "0987654321",
            "ATT_INTERACTION_TYPE": "asynchronous",
            "ATT_SERVICE_ID": "blackbutton",
            "ATT_GEOLOCATION": "40.4188,-3.6919",
        }
        self.payload_data2b_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "SERVICE_USER_NAME": "admin_bb",
            "SERVICE_USER_PASSWORD": "4passw0rd",
            "SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "ENTITY_TYPE": "service",
            "ENTITY_ID": "blackbutton-telepizza_%s" % self.suffix,
            "PROTOCOL": "TT_BLACKBUTTON",
            "ATT_NAME": "blackbutton_telepizza_%s" % self.suffix,
            "ATT_PROVIDER": "telepizza_%s" % self.suffix,
            "ATT_ENDPOINT": "http://localhost:6500/sync/request",
            "ATT_METHOD": "POST",
            "ATT_AUTHENTICATION": "context-adapter",
            "ATT_INTERACTION_TYPE": "asynchronous",
            "ATT_MAPPING": "xxx",
            "ATT_TIMEOUT": 120
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data3_ok = {
            "SERVICE_NAME": "blackbutton",
            "SERVICE_ADMIN_USER": "admin_bb",
            "SERVICE_ADMIN_PASSWORD": "4passw0rd",
            "NEW_SUBSERVICE_NAME": "telepizza_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "telepizza_%s" % self.suffix,
            "ENTITY_TYPE": "service",
            "ENTITY_ID": "blackbutton-telepizza_%s" % self.suffix,
            "PROTOCOL": "TT_BLACKBUTTON",
            "ATT_NAME": "blackbutton_telepizza_%s" % self.suffix,
            "ATT_PROVIDER": "telepizza_%s" % self.suffix,
            "ATT_ENDPOINT": "http://localhost:6500/sync/request",
            "ATT_METHOD": "POST",
            "ATT_AUTHENTICATION": "third-party",
            "ATT_INTERACTION_TYPE": "synchronous",
            "ATT_MAPPING": "xxx",
            "ATT_TIMEOUT": 120

        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)

        # Create SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok)


        # Register Device in SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/%s/register_device" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data2_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)


        # Register Service Device in SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/%s/register_service" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data2b_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)


    def test_post_ok2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data3_ok)

        # Create SubService and register Service in SubService
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data3_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)


class Test_DeleteSubService_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SUBSERVICE_NAME": "Electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "electricidad_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SUBSERVICE_NAME": "electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "electricidad_%s" % self.suffix,
        }
        self.payload_data_bad = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
            "NEW_SUBSERVICE_NAME": "electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION": "electricidad_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_delete_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        subservice_id = json_body_response['id']
        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/subservice/%s" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

    def test_delete_wrong(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/subservice/" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        subservice_id = json_body_response['id']
        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/subservice/%s" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg, res.raw_json)


class Test_NewServiceUser_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "4pass1w0rd",
            "NEW_SERVICE_USER_EMAIL": "pepe@gmail.com",
            "NEW_SERVICE_USER_DESCRIPTION": "Pepito",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "4pass1w0rd",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok3 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "4pass1w0rd",
            "NEW_SERVICE_USER_EMAIL": "email@email.com",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "4pass1w0rd",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 409, (res.code, res.msg)

    def test_post_ok3(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok3)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok3)
        assert res.code == 201, (res.code, res.msg)

    def test_post_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg)

    def test_post_bad2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_bad2)
        assert res.code == 400, (res.code, res.msg)


class Test_NewServiceTrust_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Basuras",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "ROLE_NAME": "SubServiceAdmin",
            "TRUSTEE_USER_NAME": "pep",
            "TRUSTOR_USER_NAME": "adm1",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME": "admin_domain",
            "SERVICE_ADMIN_USER": "pep",
            "SERVICE_ADMIN_PASSWORD": "pep",
        }
        self.payload_data_ok3 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "TRUSTEE_USER_NAME": "bob",
            "TRUSTOR_USER_NAME": "adm1",
        }
        self.payload_data_ok4 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "bob",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok5 = {
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Basuras",
            "ROLE_NAME": "SubServiceAdmin",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "TRUSTEE_USER_NAME":"iotagent",
            "TRUSTOR_USER_NAME":"adm1"
        }
        self.payload_data_ok5b = {
            "SERVICE_ADMIN_USER":"iotagent",
            "SERVICE_ADMIN_PASSWORD": "iotagent",
            "SERVICE_NAME": "default"
        }
        self.payload_data_ok6 = {
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Basuras",
            "ROLE_NAME": "SubServiceAdmin",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "TRUSTEE_USER_NAME":"Alice",
            "TRUSTOR_USER_NAME":"adm1"
        }
        self.payload_data_ok7 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER":"Alice",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        trustor_user_id = json_body_response['token']['user']['id']

        token_res = self.TestRestOps.getToken(self.payload_data_ok2)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        trustee_user_id = json_body_response['token']['user']['id']
        self.payload_data_ok["TRUSTEE_USER_ID"] = trustee_user_id

        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/trust/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        trust_id = json_body_response['id']
        self.payload_data_ok2["ID_TRUST"] = trust_id
        token_res = self.TestRestOps.getTrustScopedToken(self.payload_data_ok2)

    def test_post_ok2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok3)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/trust/" % service_id,
            json_data=True,
            data=self.payload_data_ok3)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        trust_id = json_body_response['id']
        self.payload_data_ok4["ID_TRUST"] = trust_id
        token_res = self.TestRestOps.getTrustScopedToken(self.payload_data_ok4)

    def test_post_ok3(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok5)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok5)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/trust/" % service_id,
            json_data=True,
            data=self.payload_data_ok5)

        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        trust_id = json_body_response['id']
        token_res = self.TestRestOps.getUnScopedToken(self.payload_data_ok5b)
        auth_token = token_res.headers.get('X-Subject-Token')
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % (service_id),
                                            json_data=True,
                                            auth_token=auth_token,
                                            data=None)
        assert res.code == 200, (res.code, res.msg, res.raw_json)
        #print "IOTAGENT token: " + auth_token

        self.payload_data_ok5b["ID_TRUST"] = trust_id
        token_res = self.TestRestOps.getTrustScopedToken(self.payload_data_ok5b)
        auth_token = token_res.headers.get('X-Subject-Token')
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % (service_id),
                                            json_data=True,
                                            auth_token=auth_token,
                                            data=None)
        assert res.code == 200, (res.code, res.msg, res.raw_json)
        #print "TRUST ID:" + trust_id,
        #print "IOTAGENT trust token: " + auth_token
        # curl -X GET  "http://127.0.0.1:1026/v1/contextEntities?details=on&limit=15&offset=0" -i -H "Accept: application/json"   -H "Fiware-Service: smartcity"   -H "Fiware-ServicePath: /Basuras" -H "X-Auth-Token: "
        # curl -X GET 'http://127.0.0.1:8088/iot/d?i=dev_01&d=t|18&k=apikey2' -i
        # curl -X GET  http://10.95.83.100:8081/iot/services   -i   -H "Content-Type: application/json"   -H "Fiware-Service: smartalcorcon"   -H "Fiware-ServicePath: /norte"

    def test_post_ok4(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok6)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/trust/" % service_id,
            json_data=True,
            data=self.payload_data_ok6)

        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        trust_id = json_body_response['id']

        # Another TrustID for the same data user
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/trust/" % service_id,
            json_data=True,
            data=self.payload_data_ok6)

        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        trust_id2 = json_body_response['id']
        assert trust_id != trust_id2

        # # Check token of iotagent does not allow a simple operation
        # token_res = self.TestRestOps.getUnScopedToken(self.payload_data_ok7)
        # auth_token = token_res.headers.get('X-Subject-Token')
        # res = self.TestRestOps.rest_request(method="GET",
        #                                     url="/v1.0/service/%s" % service_id,
        #                                     json_data=True,
        #                                     auth_token=auth_token,
        #                                     data=self.payload_data_ok7)
        # #assert res.code == 401, (res.code, res.msg, res.raw_json)

        # Use first trust to get a token
        self.payload_data_ok7["ID_TRUST"] = trust_id
        token_res = self.TestRestOps.getTrustScopedToken(self.payload_data_ok7)
        auth_token = token_res.headers.get('X-Subject-Token')
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            auth_token=auth_token,
                                            data=self.payload_data_ok7)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

        # Use second trust to get a token
        self.payload_data_ok7["ID_TRUST"] = trust_id2
        token_res2 = self.TestRestOps.getTrustScopedToken(self.payload_data_ok7)
        auth_token2 = token_res2.headers.get('X-Subject-Token')
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            auth_token=auth_token2,
                                            data=self.payload_data_ok7)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_ServiceLists_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "DOMAIN_NAME": "admin_domain",
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
            "SERVICE_NAME": "smartcity",
            "NEW_SERVICE_DESCRIPTION": "smartcity village",
        }
        self.payload_data_ok3 = {
            "DOMAIN_NAME": "smartcity",
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad = {
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad2 = {
            "DOMAIN_NAME": "admin_domain",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad3 = {
            "DOMAIN_NAME": "admin_domain",
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
        }
        self.payload_data_bad4 = {
            "DOMAIN_NAME": "wrong_admin_domain",
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
        }
        self.payload_data_bad5 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_bad(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad)
        assert res.code == 400, (res.code, res.msg)

    def test_get_bad2(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad2)
        assert res.code == 401, (res.code, res.msg)

    def test_get_bad3(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad3)
        assert res.code == 401, (res.code, res.msg)

    def test_get_bad4(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad4)
        assert res.code == 401, (res.code, res.msg)

    def test_get_bad5(self):
        auth_token_res = self.TestRestOps.getToken(self.payload_data_bad5)
        auth_token = auth_token_res.headers.get('X-Subject-Token')
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service",
                                            auth_token=auth_token,
                                            json_data=True,
                                            data=None)
        assert res.code == 403, (res.code, res.msg)

    def test_put_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok3)
        res = self.TestRestOps.rest_request(method="PUT",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

        # Get domain and check domain description
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok3)
        assert res.code == 200, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        assert json_body_response['domain']['description'] == self.payload_data_ok2["NEW_SERVICE_DESCRIPTION"]

    def test_put_nok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_bad5)
        res = self.TestRestOps.rest_request(method="PUT",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_bad5)
        assert res.code == 401, (res.code, res.msg, res.raw_json)


class Test_ServiceDetail_RestView(object):

    def __init__(self):
        self.payload_data_nok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME": "admin_domain",
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok3 = {
            "SERVICE_NAME": "Default",
            "SERVICE_ID": "default",
            "SERVICE_ADMIN_USER": "iotagent",
            "SERVICE_ADMIN_PASSWORD": "iotagent",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_nok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_nok)
        assert res.code == 401, (res.code, res.msg, res.raw_json)

    def test_get_ok3(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="/v1.0/service/%s" % self.payload_data_ok3['SERVICE_ID'],
                                            json_data=True,
                                            data=self.payload_data_ok3)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

class Test_ProjectList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "SUBSERVICE_NAME": "Electricidad",
            "NEW_SUBSERVICE_DESCRIPTION": "Elektricidad",
        }
        self.payload_data_bad = {
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
            "SUBSERVICE_NAME": "Electricidad",
            "NEW_SUBSERVICE_DESCRIPTION": "Elektricidad",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/subservice" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_nok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/subservice" % service_id,
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg, res.raw_json)

    def test_put_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(
            method="PUT",
            url="/v1.0/service/%s/subservice/%s" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_put_nok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(
            method="PUT",
            url="/v1.0/service/%s/subservice/%s" % (service_id, subservice_id),
            json_data=True,
            data=self.payload_data_bad2)
        assert res.code == 401, (res.code, res.msg, res.raw_json)


class Test_ProjectDetail_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SUBSERVICE_NAME": "Electricidad",
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/subservice/%s" % (
                service_id,
                subservice_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_NewServiceRole_RestView(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_ROLE_NAME": "role_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_nok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_ROLE_NAME": "role_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_nok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_nok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role/" % service_id,
            json_data=True,
            data=self.payload_data_nok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role/" % service_id,
            json_data=True,
            data=self.payload_data_nok)
        assert res.code == 409, (res.code, res.msg, res.raw_json)


class Test_DeleteServiceRole_RestView(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "Adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_ROLE_NAME": "role_%s" % self.suffix,
            "ROLE_NAME": "role_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_ROLE_NAME": "role_tmp_%s" % self.suffix,
            "ROLE_NAME": "role_tmp_%s" % self.suffix,
            "SERVICE_USER_NAME": "user_for_role_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "user_for_role_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "user_for_role_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok3 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "Adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_ROLE_NAME": "role_%s" % self.suffix,
            "ROLE_NAME": "role_%s" % self.suffix,
        }
        self.payload_data_bad = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "Adm1",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
            "NEW_ROLE_NAME": "role_%s" % self.suffix,
            "ROLE_NAME": "role_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_delete_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        role_id = json_body_response['id']
        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/role/%s" % (service_id, role_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

    def test_delete_ok2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role/" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        role_id = json_body_response['id']

        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        user_id = json_body_response['id']

        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role_assignments" % (
                service_id),
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/role/%s" % (service_id, role_id),
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

        # Check user exists with no role
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role_assignments?user_id=%s" % (
                service_id, user_id),
            json_data=True,
            data=self.payload_data_ok2)
        response = res.read()
        assert res.code == 400, (res.code, res.msg, res.raw_json)
        # json_body_response = json.loads(response)
        # assert len(json_body_response['role_assignments']) == 0

    def test_delete_nok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok3)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role/" % service_id,
            json_data=True,
            data=self.payload_data_ok3)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        role_id = json_body_response['id']
        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/role/%s" % (service_id, role_id),
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg, res.raw_json)


class Test_RoleList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Electricidad",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        auth_token_res = self.TestRestOps.getScopedToken(self.payload_data_ok2)
        auth_token = auth_token_res.headers.get('X-Subject-Token')
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role" % service_id,
            auth_token=auth_token,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 403, (res.code, res.msg, res.raw_json)

    def test_get_bad2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            user="admin",
            password="admin",
            url="/v1.0/service/%s/role" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_UserList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "START_INDEX": "10",
            "COUNT": "10"
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/user" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_ok2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/user" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 200, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        assert len(json_body_response['users']) <= 10

    def test_get_ok3(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/user?count=2&index=0" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        assert len(json_body_response['users']) <= 2


class Test_UserDetail_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        user_id = json_body_response['token']['user']['id']
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_UserModify_RestView(object):
    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "USER_NAME": "adm1",
            "USER_DATA_VALUE": {"emails": [{"value": "test@gmail.com"}]}
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "USER_NAME": "alf_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "alf_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "alf_%s" % self.suffix,
            "USER_DATA_VALUE": {"name": "bet_%s" % self.suffix}
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok3 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "USER_NAME": "alf_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "alf_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "alf_%s" % self.suffix,
            "USER_DATA_VALUE": {"name": "bet_%s" % self.suffix,
                                "password": "bet_%s" % self.suffix,
                                "description": "Bet bet_%s" % self.suffix}
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "USER_NAME": "alf_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "alf_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "alf_%s" % self.suffix,
            "USER_DATA_VALUE": {"nameKK3": "bet_%s" % self.suffix}
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_put_ok(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        user_id = json_body_response['token']['user']['id']
        res = self.TestRestOps.rest_request(
            method="PUT",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_put_ok2(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok2)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        # Create user
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        user_id = json_body_response['id']
        # Modify user name
        res = self.TestRestOps.rest_request(
            method="PUT",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_put_ok3(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok3)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        # Create user
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok3)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        user_id = json_body_response['id']

        # Login -> OK
        self.payload_data_tmp = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": self.payload_data_ok3["NEW_SERVICE_USER_NAME"],
            "SERVICE_ADMIN_PASSWORD": self.payload_data_ok3["NEW_SERVICE_USER_PASSWORD"]
        }
        token_res = self.TestRestOps.getUnScopedToken(self.payload_data_tmp)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)

        # Modify user password
        res = self.TestRestOps.rest_request(
            method="PUT",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_ok3)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

        # Login -> OK
        self.payload_data_tmp = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": self.payload_data_ok3["USER_DATA_VALUE"]["name"],
            "SERVICE_ADMIN_PASSWORD": self.payload_data_ok3["USER_DATA_VALUE"]["password"]
        }

        token_res = self.TestRestOps.getUnScopedToken(self.payload_data_tmp)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)

    def test_put_bad(self):
        token_res = self.TestRestOps.getToken(self.payload_data_bad)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        # Create user
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        response = res.read()
        json_body_response = json.loads(response)
        user_id = json_body_response['id']
        # Modify user name
        res = self.TestRestOps.rest_request(
            method="PUT",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 400, (res.code, res.msg, res.raw_json)


class Test_UserDelete_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "USER_NAME": "Alice_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "4pass1w0rd",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_delete_ok(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        user_id = json_body_response['id']
        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg)


class Test_UserChangePasswordByHimself_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "4pass1w0rd",
            "SERVICE_NAME": "smartcity",
            "SERVICE_USER_NAME": "user_%s" % self.suffix,
            "SERVICE_USER_PASSWORD": "4pass1w0rd",
            "NEW_USER_PASSWORD": "paswod234",
        }

        self.payload_data_ok2 = {
            "SERVICE_ADMIN_USER": "user_%s" % self.suffix,
            "SERVICE_ADMIN_PASSWORD": "4pass1w0rd",
            "SERVICE_NAME": "smartcity",
        }

        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "4pass1w0rd",
            "SERVICE_NAME": "smartcity",
            "SERVICE_USER_NAME": "user_%s" % self.suffix,
            "SERVICE_USER_PASSWORD": "bad_password",
            "NEW_USER_PASSWORD": "new_paswod234",
        }
        self.payload_data_bad2 = {
            "SERVICE_ADMIN_USER": "user_%s" % self.suffix,
            "SERVICE_ADMIN_PASSWORD": "4pass1w0rd",
            "SERVICE_NAME": "smartcity"
        }

        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']

        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        user_id = json_body_response['id']

        token_res = self.TestRestOps.getUnScopedToken(self.payload_data_ok2)
        data_response = token_res.read()
        token = token_res.headers.get('X-Subject-Token')

        res = self.TestRestOps.rest_request(
            url=self.TestRestOps.keystone_endpoint_url + '/v3/projects?domain_id=%s' % service_id,
            relative_url=False,
            method='GET',
            auth_token=token)
        assert res.code == 403, (res.code, res.msg)  # 403 just authorization not authentication
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg)

        # Use original token
        res = self.TestRestOps.rest_request(
            url=self.TestRestOps.keystone_endpoint_url + '/v3/projects?domain_id=%s' % service_id,
            relative_url=False,
            method='GET',
            auth_token=token)
        assert res.code == 401, (res.code, res.msg)


    def test_post_bad(self):
        token_res = self.TestRestOps.getToken(self.payload_data_bad)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        data_response = res.read()
        json_body_response = json.loads(data_response)
        user_id = json_body_response['id']

        # Get user token
        token_res = self.TestRestOps.getUnScopedToken(self.payload_data_bad2)
        data_response = token_res.read()
        USER_TOKEN = token_res.headers.get('X-Subject-Token')
        self.payload_data_bad["SERVICE_USER_TOKEN"] = USER_TOKEN

        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/%s" % (service_id,
                                             user_id),
            json_data=True,
            data=self.payload_data_bad)
        assert res.code == 401, (res.code, res.msg)



class Test_AssignRoleUserList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Electricidad",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_USER_NAME": "Alice",
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Electricidad",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role_assignments?subservice_id=%s" % (
                service_id, subservice_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_ok2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        # token_res = self.TestRestOps.getScopedToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        role_id = json_body_response['token']['roles'][0]['id']  # admin role
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role_assignments?role_id=%s" % (
                service_id, role_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_ok3(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        user_id = json_body_response['token']['user']['id']
        role_id = json_body_response['token']['roles'][0]['id']  # admin role
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role_assignments?role_id=%s&user_id=%s" % (
                service_id, role_id, user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_ok4(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok)
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        user_id = json_body_response['token']['user']['id']
        role_id = json_body_response['token']['roles'][0]['id']  # admin role
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role_assignments?subservice_id=%s&role_id=%s&user_id=%s" % (
                service_id, subservice_id, role_id, user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_ok5(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        user_id = json_body_response['token']['user']['id']
        role_id = json_body_response['token']['roles'][0]['id']  # admin role
        res = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role_assignments?role_id=%s&user_id=%s&effective=true" % (
                service_id, role_id, user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

        res2 = self.TestRestOps.rest_request(
            method="GET",
            url="/v1.0/service/%s/role_assignments?role_id=%s&user_id=%s&effective=false" % (
                service_id, role_id, user_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res2.code == 200, (res2.code, res2.msg, res2.raw_json)


class Test_AssignRoleUser_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "ROLE_NAME": "ServiceCustomer",
            "SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "user_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok2 = {
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Electricidad",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "ROLE_NAME": "SubServiceCustomer",
            "SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "user_%s" % self.suffix,
        }
        self.payload_data_ok2b = {
            "SERVICE_NAME": "smartcity",
            "SUBSERVICE_NAME": "Electricidad",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            #"SERVICE_ADMIN_USER": "user_%s" % self.suffix,
            #"SERVICE_ADMIN_PASSWORD": "user_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok3 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "ROLE_NAME": "SubServiceCustomer",
            "SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "user_%s" % self.suffix,
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok4 = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "ROLE_NAME": "SubServiceCustomer",
            "SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "user_%s" % self.suffix,
            "INHERIT": True
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role_assignments" % (
                service_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

    def test_post_ok2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role_assignments" % (
                service_id),
            json_data=True,
            data=self.payload_data_ok2)
        assert res.code == 204, (res.code, res.msg, res.raw_json)
        # Get Scoped Token in their project
        auth_token_res = self.TestRestOps.getScopedToken(self.payload_data_ok2b)
        auth_token = auth_token_res.headers.get('X-Subject-Token')
        # Try to get scoped token in forener project
        self.payload_data_ok2b["SUBSERVICE_NAME"] = "Basuras"
        auth_token_res = self.TestRestOps.getScopedToken(self.payload_data_ok2b)
        auth_token = auth_token_res.headers.get('X-Subject-Token')


    def test_post_ok3(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok3)
        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok3)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role_assignments?inherit=true" % (
                service_id),
            json_data=True,
            data=self.payload_data_ok3)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

    def test_post_ok4(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok4)
        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok4)
        assert res.code == 201, (res.code, res.msg, res.raw_json)
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role_assignments" % (
                service_id),
            json_data=True,
            data=self.payload_data_ok4)
        assert res.code == 204, (res.code, res.msg, res.raw_json)


class Test_UnassignRoleUser_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME": "smartcity",
            "SERVICE_ADMIN_USER": "adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "ROLE_NAME": "SubServiceCustomer",
            "SERVICE_USER_NAME": "user_%s" % self.suffix,
            "SERVICE_USER_PASSWORD": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_NAME": "user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD": "user_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_delete_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        # Create a user to test it
        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/user/" % service_id,
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

        res = self.TestRestOps.rest_request(
            method="POST",
            url="/v1.0/service/%s/role_assignments" % (
                service_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)

        res = self.TestRestOps.rest_request(
            method="DELETE",
            url="/v1.0/service/%s/role_assignments" % (
                service_id),
            json_data=True,
            data=self.payload_data_ok)
        assert res.code == 204, (res.code, res.msg, res.raw_json)


if __name__ == '__main__':

    test_NewService = Test_NewService_RestView()
    test_NewService.test_post_ok()
    test_NewService.test_post_ok_bad()
    test_NewService.test_post_bad()
    test_NewService.test_post_bad2()

    test_DeleteService = Test_DeleteService_RestView()
    test_DeleteService.test_delete_ok()
    test_DeleteService.test_delete_wrong()

    test_NewSubService = Test_NewSubService_RestView()
    test_NewSubService.test_post_ok()
    test_NewSubService.test_post_ok_bad()
    test_NewSubService.test_post_bad()
    test_NewSubService.test_post_bad2()

    test_SubServiceIoTADevice = Test_SubServiceIoTADevice_RestView()
    test_SubServiceIoTADevice.test_post_ok()
    test_SubServiceIoTADevice.test_post_ok2()
    test_SubServiceIoTADevice.test_post_ok3()

    test_SubServiceIoTAService = Test_SubServiceIoTAService_RestView()
    test_SubServiceIoTAService.test_post_ok()
    test_SubServiceIoTAService.test_post_ok2()

    test_DeleteSubService = Test_DeleteSubService_RestView()
    test_DeleteSubService.test_delete_ok()
    test_DeleteSubService.test_delete_wrong()

    test_NewServiceUser = Test_NewServiceUser_RestView()
    test_NewServiceUser.test_post_ok()
    test_NewServiceUser.test_post_ok_bad()
    test_NewServiceUser.test_post_ok3()
    test_NewServiceUser.test_post_bad()
    test_NewServiceUser.test_post_bad2()

    test_NewServiceRole = Test_NewServiceRole_RestView()
    test_NewServiceRole.test_post_ok()
    test_NewServiceRole.test_post_nok()

    test_DeleteServiceRole = Test_DeleteServiceRole_RestView()
    test_DeleteServiceRole.test_delete_ok()
    test_DeleteServiceRole.test_delete_ok2()
    test_DeleteServiceRole.test_delete_nok()

    test_ServiceDetail = Test_ServiceDetail_RestView()
    test_ServiceDetail.test_get_ok()
    test_ServiceDetail.test_get_nok()
    test_ServiceDetail.test_get_ok3()

    test_ServiceLists = Test_ServiceLists_RestView()
    test_ServiceLists.test_get_ok()
    test_ServiceLists.test_get_bad()
    test_ServiceLists.test_get_bad2()
    test_ServiceLists.test_get_bad3()
    test_ServiceLists.test_get_bad4()
    test_ServiceLists.test_get_bad5()
    test_ServiceLists.test_put_ok()
    test_ServiceLists.test_put_nok()

    test_ProjectList = Test_ProjectList_RestView()
    test_ProjectList.test_get_ok()
    test_ProjectList.test_get_nok()
    test_ProjectList.test_put_ok()
    test_ProjectList.test_put_nok()

    test_UserList = Test_UserList_RestView()
    test_UserList.test_get_ok()
    test_UserList.test_get_ok2()
    test_UserList.test_get_ok3()

    test_UserDetail = Test_UserDetail_RestView()
    test_UserDetail.test_get_ok()

    test_UserModify = Test_UserModify_RestView()
    test_UserModify.test_put_ok()
    test_UserModify.test_put_ok2()
    test_UserModify.test_put_ok3()
    test_UserModify.test_put_bad()

    test_UserModify = Test_UserDelete_RestView()
    test_UserModify.test_delete_ok()

    test_UserChangePasswordByHimself = Test_UserChangePasswordByHimself_RestView()
    test_UserChangePasswordByHimself.test_post_ok()
    test_UserChangePasswordByHimself.test_post_bad()

    test_ProjectDetail = Test_ProjectDetail_RestView()
    test_ProjectDetail.test_get_ok()

    test_RoleList = Test_RoleList_RestView()
    test_RoleList.test_get_ok()
    test_RoleList.test_get_bad()
    # test_RoleList.test_get_bad2()  # TODO: error 500 due to basic auth

    test_AssignRoleUserList = Test_AssignRoleUserList_RestView()
    test_AssignRoleUserList.test_get_ok()
    test_AssignRoleUserList.test_get_ok2()
    test_AssignRoleUserList.test_get_ok3()
    test_AssignRoleUserList.test_get_ok4()
    test_AssignRoleUserList.test_get_ok5()

    test_AssignRoleUser = Test_AssignRoleUser_RestView()
    test_AssignRoleUser.test_post_ok()
    test_AssignRoleUser.test_post_ok2()
    test_AssignRoleUser.test_post_ok3()

    test_UnassignRoleUser = Test_UnassignRoleUser_RestView()
    test_UnassignRoleUser.test_delete_ok()

    test_NewServiceTrust = Test_NewServiceTrust_RestView()
    test_NewServiceTrust.test_post_ok()
    test_NewServiceTrust.test_post_ok3()
    test_NewServiceTrust.test_post_ok4()
    # It will work just for keystone juno or upper
    #test_NewServiceTrust.test_post_ok2()
