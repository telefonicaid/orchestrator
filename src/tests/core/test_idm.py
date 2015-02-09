from orchestrator.core.idm import IdMOperations

class Test_createNewService(object):

    def __init__(self):
        self.KEYSTONE_PROTOCOL="http"
        self.KEYSTONE_HOST="localhost"
        self.KEYSTONE_PORT="5000"
        self.DOMAIN_NAME="admin_domain"
        self.DOMAIN_ADMIN_USER="cloud_admin"
        self.DOMAIN_ADMIN_PASSWORD="password"
        self.SERVICE_NAME="SmartValencia"
        self.SERVICE_ADMIN_USER="adm1"
        self.SERVICE_ADMIN_PASSWORD="password"
        self.KEYPASS_PROTOCOL="http"
        self.KEYPASS_HOST="localhost"
        self.KEYPASS_PORT="8080"
    
    def test_getToken(DOMAIN_NAME, DOMAIN_ADMIN_USER, DOMAIN_ADMIN_PASSWORD):
        pass
    def test_createDomain(CLOUD_ADMIN_TOKEN, NEW_SERVICE_NAME, NEW_SERVICE_DESCRIPTION):
        pass
    # def test_createUserAdminDomain(CLOUD_ADMIN_TOKEN, NEW_SERVICE_NAME, ID_DOM1,
    #                                NEW_SERVICE_ADMIN_USER, NEW_SERVICE_ADMIN_PASSWORD):
    #     pass

    def createUserDomain(
            SERVICE_ADMIN_TOKEN,
            ID_DOM1,
            SERVICE_NAME,
            NEW_USER_NAME,
            NEW_USER_PASSWORD):
        pass
        
    def test_getRoleId(CLOUD_ADMIN_TOKEN, ROLE_NAME):
        pass

    def test_grantDomainRole(CLOUD_ADMIN_TOKEN, ID_DOM1, ID_ADM1, ADMIN_ROLE_ID):
        pass

    def test_createDomainRole(SERVICE_ADMIN_TOKEN, SUB_SERVICE_ROLE_NAME, ID_DOM1):
        pass
    def test_provisionPolicy(SERVICE_NAME, SERVICE_ADMIN_TOKEN,
                             SUB_SERVICE_ROLE_ID, POLICY_FILE_NAME):
        pass

    def createProject(SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      NEW_SUBSERVICE_NAME,
                      NEW_SUBSERVICE_DESCRIPTION):
        pass
    

        
class Test_createNewSubService(object):

    def __init__(self):
        self.KEYSTONE_PROTOCOL="http"
        self.KEYSTONE_HOST="localhost"
        self.KEYSTONE_PORT="5000"
        self.SERVICE_NAME="SmartValencia"
        self.SERVICE_ADMIN_USER="adm1"
        self.SERVICE_ADMIN_PASSWORD="password"
        self.SUBSERVICE_NAME="Electricidad"
        self.SUBSERVICE_DESCRIPTION="electricidad"
    
    def test_createProject(self):
        pass

    def test_getDomainId(self):
        ko=IdMOperations(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)
        SERVICE_ADMIN_TOKEN = ko.getToken(self.SERVICE_NAME,
                                          self.SERVICE_ADMIN_USER,
                                          self.SERVICE_ADMIN_PASSWORD)
        SERVICE_ID = ko.getDomainId(SERVICE_ADMIN_TOKEN,
                                    self.SERVICE_NAME)
        print SERVICE_ID


if __name__ == '__main__':
   
    test_createNewService = Test_createNewSubService()
    test_createNewService.test_getDomainId()
