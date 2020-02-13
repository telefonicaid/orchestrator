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
import json
import logging

from orchestrator.common.util import RestOperations
from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class IdMKeystoneOperations(IdMOperations):
    '''
       IoT IdM: Keystone
    '''

    def __init__(self,
                 KEYSTONE_PROTOCOL=None,
                 KEYSTONE_HOST=None,
                 KEYSTONE_PORT=None,
                 TRANSACTION_ID=None):

        self.KEYSTONE_PROTOCOL = KEYSTONE_PROTOCOL
        self.KEYSTONE_HOST = KEYSTONE_HOST
        self.KEYSTONE_PORT = KEYSTONE_PORT

        self.IdMRestOperations = RestOperations("KEYSTONE",
                                                KEYSTONE_PROTOCOL,
                                                KEYSTONE_HOST,
                                                KEYSTONE_PORT,
                                                TRANSACTION_ID)

        try:
            from settings.common import SCIM_API_VERSION
        except AttributeError:
            SCIM_API_VERSION="1.1"

        self.SCIM_URI="/v3/OS-SCIM/v1" if  SCIM_API_VERSION=="2.0" else "/v3/OS-SCIM"


    def checkIdM(self):
        res = self.IdMRestOperations.rest_request(
            url='/v3/',
            method='GET',
            data=None)
        assert res.code == 200, (res.code, res.msg)

    def getToken(self,
                 DOMAIN_NAME,
                 DOMAIN_ADMIN_USER,
                 DOMAIN_ADMIN_PASSWORD,
                 SCOPED=True):

        assert DOMAIN_ADMIN_USER != None, (
                401, "auth wrong: user name not provided")
        assert DOMAIN_ADMIN_PASSWORD != None, (
                401, "auth wrong: user password not provided")

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": DOMAIN_ADMIN_USER,
                            "password": DOMAIN_ADMIN_PASSWORD
                        }
                    }
                }
            }
        }

        if DOMAIN_NAME:
            auth_data['auth']['identity']['password']['user'].update(
                {
                    "domain": {
                        "name": DOMAIN_NAME
                    }
                })
            if SCOPED:
                scope_domain = {
                    "scope": {
                        "domain": {
                            "name": DOMAIN_NAME
                        }
                    }
                }
                auth_data['auth'].update(scope_domain)

        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST',
            data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')

    def getToken2(self,
                  DOMAIN_ID,
                  DOMAIN_ADMIN_USER,
                  DOMAIN_ADMIN_PASSWORD,
                  SCOPED=True):

        assert DOMAIN_ADMIN_USER != None, (
                401, "auth wrong: user name not provided")
        assert DOMAIN_ADMIN_PASSWORD != None, (
                401, "auth wrong: user password not provided")

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": DOMAIN_ADMIN_USER,
                            "password": DOMAIN_ADMIN_PASSWORD
                        }
                    }
                }
            }
        }

        if DOMAIN_ID:
            auth_data['auth']['identity']['password']['user'].update(
                {
                    "domain": {
                        "id": DOMAIN_ID
                    }
                })
            if SCOPED:
                scope_domain = {
                    "scope": {
                        "domain": {
                            "id": DOMAIN_ID
                        }
                    }
                }
                auth_data['auth'].update(scope_domain)

        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')


    def getTokenFromToken(self,
                 DOMAIN_ADMIN_TOKEN,
                 DOMAIN_ID,
                 PROJECT_ID,
                 SCOPED=True):

        assert DOMAIN_ADMIN_TOKEN != None, (
                401, "auth wrong: user token not provided")

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "token"
                    ],
                    "token": {
                        "id": DOMAIN_ADMIN_TOKEN
                    }
                }
            }
        }

        if DOMAIN_ID:
            if SCOPED:
                if PROJECT_ID:
                    scope_domain = {
                        "scope": {
                            "project": {
                                "domain": {
                                    "id": DOMAIN_ID
                                    },
                                    "id": PROJECT_ID
                                }
                            }
                        }
                else:
                    scope_domain = {
                        "scope": {
                            "domain": {
                                "id": DOMAIN_ID
                            }
                        }
                    }
                auth_data['auth'].update(scope_domain)

        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST',
            data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        #return res.headers.get('X-Subject-Token')

        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response, res.headers.get('X-Subject-Token')


    def getScopedProjectToken(self,
                              DOMAIN_NAME,
                              PROJECT_NAME,
                              SERVICE_ADMIN_USER,
                              SERVICE_ADMIN_PASSWORD):

        assert SERVICE_ADMIN_USER != None, (
                401, "auth wrong: user name not provided")
        assert SERVICE_ADMIN_PASSWORD != None, (
                401, "auth wrong: user password not provided")

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": SERVICE_ADMIN_USER,
                            "password": SERVICE_ADMIN_PASSWORD
                        }
                    }
                }
            }
        }
        if DOMAIN_NAME and PROJECT_NAME:
            auth_data['auth']['identity']['password']['user'].update(
                {"domain": {"name": DOMAIN_NAME}})

            scope_domain = {
                "scope": {
                    "project": {
                        "domain": {
                            "name": DOMAIN_NAME
                        },
                        "name": "/" + PROJECT_NAME
                    }
                }
            }
            auth_data['auth'].update(scope_domain)
        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')

    def getScopedProjectToken2(self,
                              DOMAIN_ID,
                              PROJECT_ID,
                              SERVICE_ADMIN_USER,
                              SERVICE_ADMIN_PASSWORD):

        assert SERVICE_ADMIN_USER != None, (
                401, "auth wrong: user name not provided")
        assert SERVICE_ADMIN_PASSWORD != None, (
                401, "auth wrong: user password not provided")

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": SERVICE_ADMIN_USER,
                            "password": SERVICE_ADMIN_PASSWORD
                        }
                    }
                }
            }
        }
        if DOMAIN_ID and PROJECT_ID:
            auth_data['auth']['identity']['password']['user'].update(
                {"domain": {"id": DOMAIN_ID}})

            scope_domain = {
                "scope": {
                    "project": {
                        "domain": {
                            "id": DOMAIN_ID
                        },
                        "id": PROJECT_ID
                    }
                }
            }
            auth_data['auth'].update(scope_domain)
        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')


    # aka createService
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
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains',
            method='POST', data=body_data,
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        assert 'domain' in json_body_response, "domain %s not found" % NEW_SERVICE_NAME
        assert 'id' in json_body_response['domain'], "domain id not found"
        return json_body_response['domain']['id']

    def updateDomain(self,
                     CLOUD_ADMIN_TOKEN,
                     SERVICE_ID,
                     NEW_SERVICE_DESCRIPTION):

        body_data = {
            "domain": {
                "description": "%s" % NEW_SERVICE_DESCRIPTION
            }
        }
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s' % SERVICE_ID,
            method='PATCH', data=body_data,
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        assert 'domain' in json_body_response, "domain not found"
        assert 'id' in json_body_response['domain'], "domain id not found"
        return json_body_response['domain']['id']

    def getRoleId(self,
                  CLOUD_ADMIN_TOKEN,
                  ROLE_NAME):
        res = self.IdMRestOperations.rest_request(
            url='/v3/roles?name=%s' % ROLE_NAME,
            method='GET',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        # TODO ensure ADMIN_ROLE_ID?
        if len(json_body_response['roles']) > 0:
            return json_body_response['roles'][0]['id']
        else:
            assert False, "role id not found"

    def grantDomainRole(self,
                        CLOUD_ADMIN_TOKEN,
                        ID_DOM1,
                        ID_ADM1,
                        ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s/users/%s/roles/%s' % (
                ID_DOM1, ID_ADM1, ADMIN_ROLE_ID),
            method='PUT',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)
        # TODO: return?

    def grantDomainRoleToGroup(self,
                        CLOUD_ADMIN_TOKEN,
                        ID_DOM1,
                        ID_GROUP,
                        ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s/groups/%s/roles/%s' % (
                ID_DOM1, ID_GROUP, ADMIN_ROLE_ID),
            method='PUT',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)
        # TODO: return?

    def createDomainRole(self,
                         SERVICE_ADMIN_TOKEN,
                         ROLE_NAME,
                         ID_DOM1):
        body_data = {
            "schemas": ["urn:scim:schemas:extension:keystone:1.0"],
            "name": "%s" % ROLE_NAME,
            "domain_id": "%s" % ID_DOM1
        }
        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Roles',
            method='POST', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['id']

    def createDomainRoles(self,
                         SERVICE_ADMIN_TOKEN,
                         ROLES,
                         ID_DOM1):
        body_data = []
        for ROLE_NAME in ROLES:
            role = {
                "schemas": ["urn:scim:schemas:extension:keystone:1.0"],
                "name": "%s" % ROLE_NAME,
                "domain_id": "%s" % ID_DOM1
            }
            body_data.append(role)

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/RolesAll',
            method='POST', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        res = []
        for role in json_body_response:
            res.append(role['id'])
        return res

    # aka createSubService
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
        if NEW_SUBSERVICE_NAME.startswith('#'):
            body_data['project']['name']=NEW_SUBSERVICE_NAME
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects',
            method='POST', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['project']['id']

    def updateProject(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      SUBSERVICE_ID,
                      NEW_SUBSERVICE_DESCRIPTION):

        body_data = {
            "project": {
                "description": "%s" % NEW_SUBSERVICE_DESCRIPTION
            }
        }
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s' % SUBSERVICE_ID,
            method='PATCH', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['project']['id']

    def getDomainId(self, SERVICE_ADMIN_TOKEN, DOMAIN_NAME, SCOPED=True):

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
            }
        }
        if SCOPED:
            scope = {
                "scope": {
                    "domain": {
                        "name": DOMAIN_NAME
                    }
                }
            }
            auth_data['auth'].update(scope)

        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST',
            data=auth_data)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['token']['user']['domain']['id']

    def createUserDomain(self,
                         SERVICE_ADMIN_TOKEN,
                         ID_DOM1,
                         SERVICE_NAME,
                         NEW_USER_NAME,
                         NEW_USER_PASSWORD,
                         NEW_USER_EMAIL,
                         NEW_USER_DESCRIPTION):

        body_data = {
            "user": {
                "description": NEW_USER_DESCRIPTION if NEW_USER_DESCRIPTION else "user of domain %s" % SERVICE_NAME,
                "enabled": True,
                "domain_id": "%s" % ID_DOM1,
                "name": "%s" % NEW_USER_NAME,
                "password": "%s" % NEW_USER_PASSWORD
            }
        }
        if NEW_USER_EMAIL:
            body_data['user'].update({'email': NEW_USER_EMAIL})
        res = self.IdMRestOperations.rest_request(
            url='/v3/users',
            method='POST',
            data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['user']['id']

    def createGroupDomain(self,
                         SERVICE_ADMIN_TOKEN,
                         ID_DOM1,
                         SERVICE_NAME,
                         NEW_GROUP_NAME,
                         NEW_GROUP_DESCRIPTION):

        body_data = {
            "group": {
                "description": NEW_GROUP_DESCRIPTION if NEW_GROUP_DESCRIPTION else "group of domain %s" % SERVICE_NAME,
                "domain_id": "%s" % ID_DOM1,
                "name": "%s" % NEW_GROUP_NAME,
            }
        }
        res = self.IdMRestOperations.rest_request(
            url='/v3/groups',
            method='POST',
            data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['group']['id']

    def createRoleDomain(self,
                         SERVICE_ADMIN_TOKEN,
                         ID_DOM1,
                         NEW_ROLE_NAME):

        body_data = {
            # TODO: check this string!
            "enabled": "\[\"urn:scim:schemas:extension:keystone:1.0\"\]",
            "domain_id": "%s" % ID_DOM1,
            "name": "%s" % NEW_ROLE_NAME,
        }
        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Roles',
            method='POST', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['id']

    def getProjectId(self, SERVICE_ADMIN_TOKEN, DOMAIN_NAME, PROJECT_NAME):

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
        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST',
            data=auth_data)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        if 'projects' in json_body_response:
            for project in json_body_response['projects']:
                if project['name'] == PROJECT_NAME:
                    return project['id']
        else:
            projects = self.getUserProjects(
                SERVICE_ADMIN_TOKEN,
                json_body_response['token']['user']['id'])
            for project in projects['projects']:
                if ((project['name'] == '/' + PROJECT_NAME) or
                    (PROJECT_NAME.startswith('#') and project['name'] == PROJECT_NAME)):
                    return project['id']
            assert False, "Project %s not found" % PROJECT_NAME

    def getDomainRoleId(self,
                        SERVICE_ADMIN_TOKEN,
                        DOMAIN_ID,
                        ROLE_NAME):
        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Roles?domain_id=%s' % DOMAIN_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        for role in json_body_response['Resources']:
            if role['name'] == ROLE_NAME:
                return role['id']
        assert False, "Role %s name not found" % ROLE_NAME

    def getUserRoleId(self, SERVICE_ADMIN_TOKEN, DOMAIN_ID, PROJECT_ID, ROLE_NAME):

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
                    "project": {
                        "domain": {
                            "id": DOMAIN_ID
                        },
                        "id": PROJECT_ID
                    }
                }
            }
        }
        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST',
            data=auth_data)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        if 'roles' in json_body_response['token']:
            for role in json_body_response['token']['roles']:
                if DOMAIN_ID + '#' + ROLE_NAME == role['name']:
                    return role['id']
        assert False, "Role %s not found" % ROLE_NAME

    def getUserId(self,
                  SERVICE_USER_TOKEN,
                  USER_NAME):

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "token"
                        ],
                    "token": {
                        "id": SERVICE_USER_TOKEN
                    }
                }
            }
        }

        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST',
            data=auth_data)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        if json_body_response['token']['user']['name'] == USER_NAME:
            return json_body_response['token']['user']['id']
        else:
            assert False, "user %s not Found" % USER_NAME


    def getDomainUserId(self,
                        SERVICE_ADMIN_TOKEN,
                        DOMAIN_ID,
                        USER_NAME):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Users?domain_id=%s' % DOMAIN_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        for user in json_body_response['Resources']:
            if user['userName'] == USER_NAME:
                return user['id']
        assert False, "user name %s not Found" % USER_NAME


    def getDomainGroupId(self,
                        SERVICE_ADMIN_TOKEN,
                        DOMAIN_ID,
                        GROUP_NAME):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Groups?domain_id=%s' % DOMAIN_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        for group in json_body_response['Resources']:
            if group['displayName'] == GROUP_NAME:
                return group['id']
        assert False, "group name %s not Found" % GROUP_NAME


    def grantProjectRole(self,
                         SERVICE_ADMIN_TOKEN,
                         ID_PRO1,
                         ID_USER,
                         ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s/users/%s/roles/%s' % (
                ID_PRO1, ID_USER, ROLE_ID),
            method='PUT',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)
        # TODO: return?


    def grantProjectRoleToGroup(self,
                         SERVICE_ADMIN_TOKEN,
                         ID_PRO1,
                         ID_GROUP,
                         ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s/groups/%s/roles/%s' % (
                ID_PRO1, ID_GROUP, ROLE_ID),
            method='PUT',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)


    def detailUser(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_USER):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Users/%s' % ID_USER,
            method='GET', data=None,
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def detailGroup(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_GROUP):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Groups/%s' % ID_GROUP,
            method='GET', data=None,
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def removeUser(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_USER):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Users/%s' % ID_USER,
            method='DELETE', data=None,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)
        # return ?


    def removeGroup(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_GROUP):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Groups/%s' % ID_GROUP,
            method='DELETE', data=None,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)


    def updateUser(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_USER,
                   USER_DATA):
        body_data = {

            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
        }
        # Replace 'name' by 'userName' since we are using SCIM API
        if 'name' in USER_DATA:
            USER_DATA['userName'] = USER_DATA['name']
        if 'description' in USER_DATA:
            USER_DATA['displayName'] = USER_DATA['description']
        body_data.update(USER_DATA)
        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Users/%s' % ID_USER,
            method='PATCH', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def updateGroup(self,
                    SERVICE_ADMIN_TOKEN,
                    ID_GROUP,
                    GROUP_DATA):
        body_data = {
            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
        }
        # Replace 'name' by 'displayName' since we are using SCIM API
        if 'groupName' in GROUP_DATA:
            GROUP_DATA['displayName'] = GROUP_DATA['groupName']
        if 'description' in GROUP_DATA:
            GROUP_DATA['displayName'] = GROUP_DATA['description']
        body_data.update(GROUP_DATA)
        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Groups/%s' % ID_GROUP,
            method='PATCH', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def getDomains(self,
                   SERVICE_ADMIN_TOKEN):

        res = self.IdMRestOperations.rest_request(
            url='/v3/domains',
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        domains = []
        for domain in json_body_response['domains']:
            domain_data = {
                "id": domain['id'],
                "name": domain['name'],
                "enabled": domain['enabled']
            }
            if 'description' in domain:
                domain_data.update({"description": domain['description']})
            domains.append(domain_data)

        return {"domains": domains}

    def getDomain(self,
                  SERVICE_ADMIN_TOKEN,
                  DOMAIN_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s' % DOMAIN_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def getDomainRoles(self,
                       SERVICE_ADMIN_TOKEN,
                       DOMAIN_ID,
                       START_INDEX=None,
                       COUNT=None):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Roles?domain_id=%s%s' % (
                DOMAIN_ID,
                "&startIndex=%s&count=%s" % (START_INDEX, COUNT) if START_INDEX and COUNT else ""),
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        # Group each role by name and id
        roles = []
        for role in json_body_response['Resources']:
            role_data = {
                "name": role['name'],
                "id": role['id'],
                "domain_id": DOMAIN_ID
            }
            roles.append(role_data)

        res = {"roles": roles}
        if "totalResults" in json_body_response:
            res["totalResults"] = json_body_response["totalResults"]
        if "itemsPerPage" in json_body_response:
            res["itemsPerPage"] = json_body_response["itemsPerPage"]
        if "startIndex" in json_body_response:
            res["startIndex"] = json_body_response["startIndex"]
        return res

    def getDomainUsers(self,
                       SERVICE_ADMIN_TOKEN,
                       DOMAIN_ID,
                       START_INDEX=None,
                       COUNT=None):
        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Users?domain_id=%s%s' % (
                DOMAIN_ID,
                "&startIndex=%s&count=%s" % (START_INDEX, COUNT) if START_INDEX and COUNT else ""),
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        # Group each user by name and id
        users = []
        for user in json_body_response['Resources']:
            users.append(
                {
                    "name": user['userName'],
                    "userName": user['userName'],
                    "id": user['id'],
                    "description": user["displayName"] if "displayName" in user else "",
                    "domain_id":
                       user['urn:scim:schemas:extension:keystone:1.0']['domain_id'],
                    "enabled": user['active'] if "active" in user else ""
                }
            )
        res = {"users": users}
        if "totalResults" in json_body_response:
            res["totalResults"] = json_body_response["totalResults"]
        if "itemsPerPage" in json_body_response:
            res["itemsPerPage"] = json_body_response["itemsPerPage"]
        if "startIndex" in json_body_response:
            res["startIndex"] = json_body_response["startIndex"]
        return res


    def getDomainGroups(self,
                       SERVICE_ADMIN_TOKEN,
                       DOMAIN_ID,
                       START_INDEX=None,
                       COUNT=None):
        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Groups?domain_id=%s%s' % (
                DOMAIN_ID,
                "&startIndex=%s&count=%s" % (START_INDEX, COUNT) if START_INDEX and COUNT else ""),
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        # Group each group by name and id
        groups = []
        for group in json_body_response['Resources']:
            groups.append(
                {
                    "name": group['displayName'],
                    "groupName": group['displayName'],
                    "id": group['id'],
                    "description": group["displayName"],
                    "domain_id":
                       group['urn:scim:schemas:extension:keystone:1.0']['domain_id']
                }
            )
        res = {"groups": groups}
        if "totalResults" in json_body_response:
            res["totalResults"] = json_body_response["totalResults"]
        if "itemsPerPage" in json_body_response:
            res["itemsPerPage"] = json_body_response["itemsPerPage"]
        if "startIndex" in json_body_response:
            res["startIndex"] = json_body_response["startIndex"]
        return res


    def getDomainProjects(self,
                          SERVICE_ADMIN_TOKEN,
                          DOMAIN_ID):

        res = self.IdMRestOperations.rest_request(
            url='/v3/projects?domain_id=%s' % DOMAIN_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        # Group each role by name and id
        projects = []
        for project in json_body_response['projects']:
            project_data = {
                "name": project['name'],
                "id": project['id'],
                "domain_id": project['domain_id']
            }
            # TODO: include domain_name into each project ?
            if 'description' in project:
                project_data.update({"description": project['description']})

            projects.append(project_data)
        return {"projects": projects}

    def getUserProjects(self,
                        SERVICE_ADMIN_TOKEN,
                        USER_ID):

        res = self.IdMRestOperations.rest_request(
            url='/v3/users/%s/projects' % USER_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return {"projects": json_body_response['projects']}

    def getGroupProjects(self,
                        SERVICE_ADMIN_TOKEN,
                        GROUP_ID):

        res = self.IdMRestOperations.rest_request(
            url='/v3/groups/%s/projects' % GROUP_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return {"projects": json_body_response['projects']}

    def changeUserPassword(self,
                           SERVICE_USER_TOKEN,
                           USER_ID,
                           USER_PASSWORD,
                           NEW_USER_PASSWORD):

        body_data = {
            'user': {
                'original_password': USER_PASSWORD,
                'password': NEW_USER_PASSWORD
            }
        }
        res = self.IdMRestOperations.rest_request(
            url='/v3/users/%s/password' % USER_ID,
            method='POST', data=body_data,
            auth_token=SERVICE_USER_TOKEN)
        assert res.code == 204, (res.code, res.msg)

    def getProject(self,
                   SERVICE_ADMIN_TOKEN,
                   PROJECT_ID):

        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s' % PROJECT_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response


    def getDomainNameFromToken(self,
                               SERVICE_ADMIN_TOKEN,
                               DOMAIN_ID):

        token_data, token_value = self.getTokenFromToken(
                                            SERVICE_ADMIN_TOKEN,
                                            DOMAIN_ID,
                                            None,
                                            True)
        logger.debug("json response: %s" % json.dumps(token_data,
                                                      indent=3))
        return token_data['token']['domain']['name']


    def getProjectNameFromToken(self,
                            SERVICE_ADMIN_TOKEN,
                            DOMAIN_ID,
                            PROJECT_ID):

        token_data, token_value = self.getTokenFromToken(
                                            SERVICE_ADMIN_TOKEN,
                                            DOMAIN_ID,
                                            PROJECT_ID,
                                            True)
        logger.debug("json response: %s" % json.dumps(token_data,
                                                      indent=3))

        return token_data['token']['project']['name'][1:]

    def getProjectRoleAssignments(self,
                                  SERVICE_ADMIN_TOKEN,
                                  PROJECT_ID,
                                  EFFECTIVE):

        res = self.IdMRestOperations.rest_request(
            url='/v3/role_assignments?scope.project.id=%s%s' % (
                PROJECT_ID, "&effective" if EFFECTIVE else ""),
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response

    def getDomainRoleAssignments(self,
                                 SERVICE_ADMIN_TOKEN,
                                 DOMAIN_ID,
                                 EFFECTIVE):

        res = self.IdMRestOperations.rest_request(
            url='/v3/role_assignments?scope.domain.id=%s%s' % (
                DOMAIN_ID, "&effective" if EFFECTIVE else ""),
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response

    def grantInheritRole(self,
                         CLOUD_ADMIN_TOKEN,
                         ID_DOM1,
                         ID_ADM1,
                         ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-INHERIT/domains/%s/users/%s/roles/%s/inherited_to_projects' % (
                ID_DOM1, ID_ADM1, ADMIN_ROLE_ID),
            method='PUT',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def grantInheritRoleToGroup(self,
                         CLOUD_ADMIN_TOKEN,
                         ID_DOM1,
                         ID_GROUP,
                         ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-INHERIT/domains/%s/groups/%s/roles/%s/inherited_to_projects' % (
                ID_DOM1, ID_GROUP, ADMIN_ROLE_ID),
            method='PUT',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def deleteDomain(self,
                     SERVICE_ADMIN_TOKEN,
                     DOMAIN_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s' % DOMAIN_ID,
            method='DELETE',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def deleteProject(self,
                      SERVICE_ADMIN_TOKEN,
                      PROJECT_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s' % PROJECT_ID,
            method='DELETE',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def disableDomain(self,
                      CLOUD_ADMIN_TOKEN,
                      SERVICE_ID):

        body_data = {
            "domain": {
                "enabled": False
            }
        }
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s' % SERVICE_ID,
            method='PATCH', data=body_data,
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        assert 'domain' in json_body_response, "domain not found"
        assert 'id' in json_body_response['domain'], "domain id not found"
        return json_body_response['domain']['id']

    def disableProject(self,
                       SERVICE_ADMIN_TOKEN,
                       ID_DOM1,
                       SUBSERVICE_ID):

        body_data = {
            "project": {
                "enabled": False
            }
        }
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s' % SUBSERVICE_ID,
            method='PATCH', data=body_data,
            auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        assert 'project' in json_body_response, "project not found"
        assert 'id' in json_body_response['project'], "project id not found"
        return json_body_response['project']['id']

    def revokeDomainRole(self,
                         CLOUD_ADMIN_TOKEN,
                         ID_DOM1,
                         ID_ADM1,
                         ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s/users/%s/roles/%s' % (
                ID_DOM1, ID_ADM1, ADMIN_ROLE_ID),
            method='DELETE',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def revokeDomainRoleToGroup(self,
                         CLOUD_ADMIN_TOKEN,
                         ID_DOM1,
                         ID_GROUP,
                         ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/domains/%s/groups/%s/roles/%s' % (
                ID_DOM1, ID_GROUP, ADMIN_ROLE_ID),
            method='DELETE',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def revokeProjectRole(self,
                          SERVICE_ADMIN_TOKEN,
                          ID_PRO1,
                          ID_USER,
                          ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s/users/%s/roles/%s' % (
                ID_PRO1, ID_USER, ROLE_ID),
            method='DELETE',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def revokeProjectRoleToGroup(self,
                          SERVICE_ADMIN_TOKEN,
                          ID_PRO1,
                          ID_GROUP,
                          ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/projects/%s/groups/%s/roles/%s' % (
                ID_PRO1, ID_GROUP, ROLE_ID),
            method='DELETE',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def revokeInheritRole(self,
                          CLOUD_ADMIN_TOKEN,
                          ID_DOM1,
                          ID_ADM1,
                          ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-INHERIT/domains/%s/users/%s/roles/%s/inherited_to_projects' % (
                ID_DOM1, ID_ADM1, ADMIN_ROLE_ID),
            method='DELETE',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def revokeInheritRoleToGroup(self,
                          CLOUD_ADMIN_TOKEN,
                          ID_DOM1,
                          ID_GROUP,
                          ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-INHERIT/domains/%s/groups/%s/roles/%s/inherited_to_projects' % (
                ID_DOM1, ID_GROUP, ADMIN_ROLE_ID),
            method='DELETE',
            auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def getUserDomainInheritRoleAssignments(self,
                                            SERVICE_ADMIN_TOKEN,
                                            DOMAIN_ID,
                                            USER_ID):

        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-INHERIT/domains/%s/users/%s/roles/inherited_to_projects' % (
                DOMAIN_ID,
                USER_ID,
                ),
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response

    def getGroupDomainInheritRoleAssignments(self,
                                            SERVICE_ADMIN_TOKEN,
                                            DOMAIN_ID,
                                            GROUP_ID):

        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-INHERIT/domains/%s/groups/%s/roles/inherited_to_projects' % (
                DOMAIN_ID,
                GROUP_ID,
                ),
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response

    def removeRole(self,
                   SERVICE_ADMIN_TOKEN,
                   DOMAIN_ID,
                   ID_ROLE):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/Roles/%s?domain_id=%s' % (ID_ROLE, DOMAIN_ID),
            method='DELETE', data=None,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def removeRoles(self,
                    SERVICE_ADMIN_TOKEN,
                    DOMAIN_ID):

        res = self.IdMRestOperations.rest_request(
            url=self.SCIM_URI+'/RolesAll?domain_id=%s' % DOMAIN_ID,
            method='DELETE', data=None,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)

    def createTrustToken(self,
                         SERVICE_ADMIN_TOKEN,
                         SUBSERVICE_ID,
                         ROLE_ID,
                         TRUSTEE_USER_ID,
                         TRUSTOR_USER_ID):

        trust_data = {
            "trust": {
                "impersonation": False,
                "trustee_user_id": TRUSTEE_USER_ID,
                "trustor_user_id": TRUSTOR_USER_ID
                }
            }


        # According with:
        # https://github.com/openstack-attic/identity-api/blob/master/v3/src/markdown/identity-api-v3-os-trust-ext.md
        # A project_id may not be specified without at least one role, and vice versa. In other words, there is no way of implicitly delegating all roles to a trustee, in order to prevent users accidentally creating trust that are much more broad in scope than intended. A trust without a project_id or any delegated roles is unscoped, and therefore does not represent authorization on a specific resource
        if SUBSERVICE_ID and ROLE_ID:
            trust_data['trust'].update({"project_id": SUBSERVICE_ID})
            trust_data['trust'].update({"roles": [{"id": ROLE_ID}]})

        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-TRUST/trusts',
            method='POST',
            data=trust_data,
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response['trust']['id']


    def getTrustsTrustee(self,
                         SERVICE_ADMIN_TOKEN,
                         USER_ID):

        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-TRUST/trusts?trustee_user_id=%s' % USER_ID,
            method='GET',
            auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return { "trusts": json_body_response['trusts'] }


    def getAuthorizeOauth2(self,
                           SERVICE_USER_TOKEN,
                           URL_PARAMS):

        res = self.IdMRestOperations.rest_request(
            url='/v3/OS-OAUTH2/authorize?%s' % URL_PARAMS,
            method='GET',
            auth_token=SERVICE_USER_TOKEN)

        assert res.code == 200, (res.code, res.msg)

    def getAuthorizeCodeOauth2(self,
                               SERVICE_USER_TOKEN,
                               CLIENT_ID,
                               SCOPES):

        user_auth_data = {
            "user_auth": {
                "client_id": CLIENT_ID,
                "scopes": SCOPES
            }
        }

        res = self.IdMRestOperations.rest_request2(
            url='/v3/OS-OAUTH2/authorize',
            method='POST',
            data=user_auth_data,
            auth_token=SERVICE_USER_TOKEN)

        #assert res.code == 201, (res.code, res.msg)
        return res.history[0].headers.get('location').split('code=')[1]


    def requestAccessToken(self,
                           USER,
                           PASSWORD,
                           GRANT_TYPE,
                           CODE,
                           REDIRECT_URL):

        data = {
            "token_request": {
                "grant_type": GRANT_TYPE,
                "code": CODE,
                "redirect_uri": REDIRECT_URL
            }
        }

        res = self.IdMRestOperations.rest_request2(
            user=USER,
            password=PASSWORD,
            url='/v3/OS-OAUTH2/access_token',
            method='POST',
            data=data)

        assert res.status_code == 200, (res.code, res.reason)

        json_body_response = json.loads(res.content)
        return json_body_response['access_token'], json_body_response['refresh_token']

    def requestRefreshAccessToken(self,
                           USER,
                           PASSWORD,
                           GRANT_TYPE,
                           REFRESH_TOKEN):

        data = {
            "token_request": {
                "grant_type": GRANT_TYPE,
                "refresh_token": REFRESH_TOKEN
            }
        }

        res = self.IdMRestOperations.rest_request2(
            user=USER,
            password=PASSWORD,
            url='/v3/OS-OAUTH2/access_token',
            method='POST',
            data=data)

        assert res.status_code == 200, (res.code, res.reason)

        json_body_response = json.loads(res.content)
        return json_body_response['access_token']


    def getTokenFromAccessToken(self,
                                ACCESS_TOKEN_ID,
                                DOMAIN_NAME,
                                PROJECT_NAME=None,
                                SCOPED=True):

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "oauth2"
                    ],
                    "oauth2": {
                        "access_token_id": ACCESS_TOKEN_ID
                    }
                }
            }
        }

        if DOMAIN_NAME:
            if SCOPED:
                if PROJECT_NAME:
                    scope_domain = {
                        "scope": {
                            "project": {
                                "domain": {
                                    "name": DOMAIN_NAME
                                },
                                "name": "/" + PROJECT_NAME
                            }
                        }
                    }
                else:
                    scope_domain = {
                        "scope": {
                            "domain": {
                                "name": DOMAIN_NAME
                            }
                        }
                    }
                auth_data['auth'].update(scope_domain)

        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='POST',
            data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')

    def getTokenDetail(self,
                       TOKEN):

        res = self.IdMRestOperations.rest_request(
            url='/v3/auth/tokens',
            method='GET',
            data=None,
            auth_token=TOKEN,
            subject_token=TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        logger.debug("json response: %s" % json.dumps(json_body_response,
                                                      indent=3))
        return json_body_response

    def isTokenAdmin(self, TOKEN, DOMAIN_ID):
        # Check Role admin asigned in DOMAIN
        token_res = self.getTokenDetail(TOKEN)
        for role in token_res['token']['roles']:
            if role['name'] == 'admin':
                return True
        return False
