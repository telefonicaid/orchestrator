import json
import os

from orchestrator.common.util import RestOperations
from orchestrator.core import policies
from orchestrator.core.ac import AccCOperations



class AccCKeypassOperations(AccCOperations):
    '''
       IoT Access Control: Keypass
    '''

    def __init__(self,
                 KEYPASS_PROTOCOL=None,
                 KEYPASS_HOST=None,
                 KEYPASS_PORT=None
             ):

        self.KEYPASS_PROTOCOL=KEYPASS_PROTOCOL
        self.KEYPASS_HOST=KEYPASS_HOST
        self.KEYPASS_PORT=KEYPASS_PORT

        self.AccessControlRestOperations = RestOperations(KEYPASS_PROTOCOL,
                                                          KEYPASS_HOST,
                                                          KEYPASS_PORT)

        self.policy_dir = os.path.dirname(policies.__file__)

    def checkAccC(self):
        res = self.AccessControlRestOperations.rest_request(
            url='/pap/v1/subject/',
            method='GET',
            data=None)
        assert res.code == 404, (res.code, res.msg)


    def provisionPolicy(self,
                        SERVICE_NAME,
                        SERVICE_ADMIN_TOKEN,
                        SUB_SERVICE_ROLE_ID,
                        POLICY_FILE_NAME):

        xml_data = open(self.policy_dir + '/' + POLICY_FILE_NAME)
        body_data = xml_data.read()
        xml_data.close()
        self.provisionPolicyByContent(SERVICE_NAME,
                                      SERVICE_ADMIN_TOKEN,
                                      SUB_SERVICE_ROLE_ID,
                                      body_data)

    def provisionPolicyByContent(self,
                        SERVICE_NAME,
                        SERVICE_ADMIN_TOKEN,
                        SUB_SERVICE_ROLE_ID,
                        POLICY_CONTENT):

        res = self.AccessControlRestOperations.rest_request(
                                url='pap/v1/subject/'+SUB_SERVICE_ROLE_ID,
                                method='POST',
                                json_data=False,
                                data=POLICY_CONTENT,
                                auth_token=SERVICE_ADMIN_TOKEN,
                                fiware_service=SERVICE_NAME)

        assert res.code == 201, (res.code, res.msg)
        # TODO: return ?
