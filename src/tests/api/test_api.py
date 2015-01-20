from orchestrator.common.util import RestOperations

class Test_NewService_RestView(object):

    def __init__(self):
        self.post_data = {
            "KEYSTONE_PROTOCOL":"http",
            "KEYSTONE_HOST":"localhost",
            "KEYSTONE_PORT":"5000",
            "DOMAIN_NAME":"admin_domain",
            "DOMAIN_ADMIN_USER":"cloud_admin",
            "DOMAIN_ADMIN_PASSWORD": "password",
            "NEW_SERVICE_NAME":"SmartValencia20",
            "NEW_SERVICE_DESCRIPTION":"SmartValencia20",
            "NEW_SERVICE_ADMIN_USER":"adm20",
            "NEW_SERVICE_ADMIN_PASSWORD":"password",
            "KEYPASS_PROTOCOL":"http",
            "KEYPASS_HOST":"localhost",
            "KEYPASS_PORT":"8080"
        }
        self.rest_ops = RestOperations()
    
    def test_post(self):


        res = self.rest_ops.rest_request(method="POST",
                                   user="admin",
                                   password="admin",
                                   url="http://localhost:8084/v1.0/service/",
                                   relative_url=False,
                                   json_data=True,
                                   data=self.post_data)
        # TODO assert res.code
        # import pdb
        # pdb.set_trace()
        # None
        pass
        


if __name__ == '__main__':
   
    test_NewService = Test_NewService_RestView()
    test_NewService.test_post()
