import uuid
import json

from orchestrator.common.util import RestOperations


# TODO: split TestRestOperations in another file
class TestRestOperations(RestOperations):

    def __init__(self, PROTOCOL, HOST, PORT):
        RestOperations.__init__(self,
                                PROTOCOL,
                                HOST,
                                PORT)

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
            auth_data['auth']['identity']['password']['user'].update({"domain": { "name": data["SERVICE_NAME"]}})

            scope_domain = {
                "scope": {
                    "domain": {
                        "name": data["SERVICE_NAME"]
                    }
                }
            }
            auth_data['auth'].update(scope_domain)
        res = self.rest_request(url='http://localhost:5000/v3/auth/tokens',
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
            auth_data['auth']['identity']['password']['user'].update({"domain": { "name": data["SERVICE_NAME"]}})

            scope_domain = {
                "scope": {
                    "project": {
                        "domain": {
                            "name": data["SERVICE_NAME"]
                        },
                        "name": "/"+ data["SUBSERVICE_NAME"]
                    }
                }
            }
            auth_data['auth'].update(scope_domain)
        res = self.rest_request(url='http://localhost:5000/v3/auth/tokens',
                                relative_url=False,
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
        res = self.rest_request(url='http://localhost:5000/v3/projects?domain_id=%s' % DOMAIN_ID,
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
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD":"password",
        }
        self.payload_data_ok2 = {
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD":"password",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "wrong_password",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD":"password",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad2 = {
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        #TOKEN="kk3"
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/",
                                            json_data=True,
         #                                   auth_token=TOKEN,
                                            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad2(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad2)
        assert res.code == 400, (res.code, res.msg)


class Test_NewSubService_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD":"password",
            "NEW_SUBSERVICE_NAME":"Electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION":"electricidad_%s" % self.suffix,            
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD":"password",
            "NEW_SUBSERVICE_NAME":"electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION":"electricidad_%s" % self.suffix,            
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD":"wrong_password",
            "NEW_SUBSERVICE_NAME":"electricidad_%s" % self.suffix,
            "NEW_SUBSERVICE_DESCRIPTION":"electricidad_%s" % self.suffix,                        
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad2 = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "NEW_SUBSERVICE_NAME":"electricidad_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/subservice/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/subservice/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/subservice/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_bad)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/subservice/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_bad2)
        assert res.code == 400, (res.code, res.msg)


class Test_NewServiceUser_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD":"password",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD":"password",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD":"password",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_bad2 = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/user/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/user/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/user/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_bad)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/user/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_bad2)
        assert res.code == 400, (res.code, res.msg)

class Test_ServiceLists_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "DOMAIN_NAME":"admin_domain",
            "SERVICE_ADMIN_USER":"cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad = {
            "SERVICE_ADMIN_USER":"cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad2 = {
            "DOMAIN_NAME":"admin_domain",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad3 = {
            "DOMAIN_NAME":"admin_domain",
            "SERVICE_ADMIN_USER":"cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
        }
        self.payload_data_bad4 = {
            "DOMAIN_NAME":"wrong_admin_domain",
            "SERVICE_ADMIN_USER":"cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_bad(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad)
        assert res.code == 400, (res.code, res.msg)

    def test_get_bad2(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad2)
        assert res.code == 400, (res.code, res.msg)

    def test_get_bad3(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad3)
        assert res.code == 400, (res.code, res.msg)

    def test_get_bad4(self):
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.payload_data_bad4)
        assert res.code == 400, (res.code, res.msg)

class Test_ServiceDetail_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME":"admin_domain",
            "SERVICE_ADMIN_USER":"cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_ProjectList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_bad = {
            "SERVICE_ADMIN_USER":"cloud_admin",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s/subservice" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_ProjectDetail_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SUBSERVICE_NAME":"Electricidad",
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s/subservice/%s" % (
                                                service_id,
                                                subservice_id),
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_NewServiceRole_RestView(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_ROLE_NAME":"role_%s" % self.suffix,
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_post_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="POST",
                                            url="v1.0/service/%s/role/" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

class Test_RoleList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.payload_data_ok2 = {
            "SERVICE_NAME":"SmartValencia",
            "SUBSERVICE_NAME":"Electricidad",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s/role" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

    def test_get_bad(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok2)
        auth_token_res = self.TestRestOps.getScopedToken(self.payload_data_ok2)
        auth_token = auth_token_res.headers.get('X-Subject-Token')
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s/role" % service_id,
                                            auth_token=auth_token,
                                            json_data=True,
                                            data=self.payload_data_ok2)
        assert res.code == 400, (res.code, res.msg, res.raw_json)

    def test_get_bad2(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="GET",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/service/%s/role" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


class Test_UserList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s/user" % service_id,
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

class Test_UserDetail_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
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
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s/user/%s" % (service_id,
                                                                             user_id),
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)



class Test_UserModify_RestView(object):
    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "USER_NAME":"adm1",
            "USER_DATA_VALUE": { "emails": [ {"value": "test@gmail.com"}] }
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
        res = self.TestRestOps.rest_request(method="PUT",
                                            url="v1.0/service/%s/user/%s" % (service_id,
                                                                             user_id),
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)



class Test_UserDelete_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "USER_NAME":"Alice"
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_delete_ok(self):
        token_res = self.TestRestOps.getToken(self.payload_data_ok)
        data_response = token_res.read()
        json_body_response = json.loads(data_response)
        service_id = json_body_response['token']['user']['domain']['id']
        user_id = json_body_response['token']['user']['id']
        res = self.TestRestOps.rest_request(method="DELETE",
                                            url="v1.0/service/%s/user/%s" % (service_id,
                                                                             user_id),
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)

class Test_AssignRoleUserList_RestView(object):

    def __init__(self):
        self.payload_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SUBSERVICE_NAME":"Electricidad",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
        }
        self.TestRestOps = TestRestOperations(PROTOCOL="http",
                                              HOST="localhost",
                                              PORT="8084")

    def test_get_ok(self):
        service_id = self.TestRestOps.getServiceId(self.payload_data_ok)
        subservice_id = self.TestRestOps.getSubServiceId(self.payload_data_ok)
        res = self.TestRestOps.rest_request(method="GET",
                                            url="v1.0/service/%s/role_assignments?project_id=%s" % (
                                                service_id, subservice_id),
                                            json_data=True,
                                            data=self.payload_data_ok)
        assert res.code == 200, (res.code, res.msg, res.raw_json)


if __name__ == '__main__':

    test_NewService = Test_NewService_RestView()
    test_NewService.test_post_ok()
    test_NewService.test_post_ok_bad()
    test_NewService.test_post_bad()
    test_NewService.test_post_bad2()

    test_NewSubService = Test_NewSubService_RestView()
    test_NewSubService.test_post_ok()
    test_NewSubService.test_post_ok_bad()
    test_NewSubService.test_post_bad()
    test_NewSubService.test_post_bad2()

    test_NewServiceUser = Test_NewServiceUser_RestView()
    test_NewServiceUser.test_post_ok()
    test_NewServiceUser.test_post_ok_bad()
    test_NewServiceUser.test_post_bad()
    test_NewServiceUser.test_post_bad2()

    test_NewServiceRole = Test_NewServiceRole_RestView()
    test_NewServiceRole.test_post_ok()

    test_ServiceDetail = Test_ServiceDetail_RestView()
    test_ServiceDetail.test_get_ok()

    test_ServiceLists = Test_ServiceLists_RestView()
    test_ServiceLists.test_get_ok()
    test_ServiceLists.test_get_bad()
    test_ServiceLists.test_get_bad2()
    test_ServiceLists.test_get_bad3()
    test_ServiceLists.test_get_bad4()

    test_ProjectList = Test_ProjectList_RestView()
    test_ProjectList.test_get_ok()

    test_UserList = Test_UserList_RestView()
    test_UserList.test_get_ok()

    test_UserDetail = Test_UserDetail_RestView()
    test_UserDetail.test_get_ok()

    test_UserModify = Test_UserModify_RestView()
    test_UserModify.test_put_ok()

    test_ProjectDetail = Test_ProjectDetail_RestView()
    test_ProjectDetail.test_get_ok()

    test_RoleList = Test_RoleList_RestView()
    test_RoleList.test_get_ok()
    test_RoleList.test_get_bad()
    # test_RoleList.test_get_bad2() # TODO: error 500

    test_AssignRoleUserList = Test_AssignRoleUserList_RestView()
    test_AssignRoleUserList.test_get_ok()
