import uuid
from orchestrator.common.util import RestOperations

class Test_NewService_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.post_data_ok = {
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD":"password",
        }
        self.post_data_ok2 = {
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD":"password",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.post_data_bad = {
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "wrong_password",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_PASSWORD":"password",
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.post_data_bad2 = {
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "NEW_SERVICE_NAME":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_DESCRIPTION":"SmartValencia_%s" % self.suffix,
            "NEW_SERVICE_ADMIN_USER":"adm_%s" % self.suffix,
        }

        self.TestRestOps = RestOperations(PROTOCOL="http",
                                          HOST="localhost",
                                          PORT="8084")

    def test_post_ok(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.post_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.post_data_ok2)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.post_data_bad)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad2(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/service/",
                                            json_data=True,
                                            data=self.post_data_bad2)
        assert res.code == 400, (res.code, res.msg)



class Test_NewServiceUser_RestView(object):

    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]
        self.post_data_ok = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD":"password",
        }
        self.post_data_ok2 = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD":"password",            
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.post_data_bad = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "wrong_password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
            "NEW_SERVICE_USER_PASSWORD":"password",            
        }
        self.suffix = str(uuid.uuid4())[:8]
        self.post_data_bad2 = {
            "SERVICE_NAME":"SmartValencia",
            "SERVICE_ADMIN_USER":"adm1",
            "SERVICE_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_USER_NAME":"user_%s" % self.suffix,
        }

        self.TestRestOps = RestOperations(PROTOCOL="http",
                                          HOST="localhost",
                                          PORT="8084")

    def test_post_ok(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/user/",
                                            json_data=True,
                                            data=self.post_data_ok)
        assert res.code == 201, (res.code, res.msg, res.raw_json)

    def test_post_ok_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/user/",
                                            json_data=True,
                                            data=self.post_data_ok2)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/user/",
                                            json_data=True,
                                            data=self.post_data_bad)
        assert res.code == 400, (res.code, res.msg)

    def test_post_bad2(self):
        res = self.TestRestOps.rest_request(method="POST",
                                            user="admin",
                                            password="admin",
                                            url="v1.0/user/",
                                            json_data=True,
                                            data=self.post_data_bad2)
        assert res.code == 400, (res.code, res.msg)
        


if __name__ == '__main__':
    test_NewService = Test_NewService_RestView()
    test_NewService.test_post_ok()
    test_NewService.test_post_ok_bad()
    test_NewService.test_post_bad()
    test_NewService.test_post_bad2()

    test_NewServiceUser = Test_NewServiceUser_RestView()
    test_NewServiceUser.test_post_ok()
    test_NewServiceUser.test_post_ok_bad()
    test_NewServiceUser.test_post_bad()
    test_NewServiceUser.test_post_bad2()
