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

from orchestrator.core.flow.base import FlowBase
from orchestrator.common.util import ContextFilterService
from orchestrator.common.util import ContextFilterSubService


class Roles(FlowBase):

    def roles(self,
              DOMAIN_NAME,
              DOMAIN_ID,
              ADMIN_USER,
              ADMIN_PASSWORD,
              ADMIN_TOKEN,
              START_INDEX=None,
              COUNT=None):

        '''Get Roles of a domain

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_NAME: name of domain
        - DOMAIN_ID: id of domain
        - ADMIN_USER: Service admin username
        - ADMIN_PASSWORD: Service admin password
        - ADMIN_TOKEN: Service admin token
        - START_INDEX: Start index
        - COUNT: Count
        Return:
        - array list of roles
        '''
        data_log = {
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % "***", #ADMIN_PASSWORD,
            "ADMIN_TOKEN": self.get_extended_token(ADMIN_TOKEN),
            "START_INDEX": "%s" % START_INDEX,
            "COUNT": "%s" % COUNT,
        }
        self.logger.debug("FLOW roles invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                if not DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)
                else:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                 ADMIN_USER,
                                                 ADMIN_PASSWORD)
            self.logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            # Ensure DOMAIN_NAME
            DOMAIN_NAME = self.ensure_service_name(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))
            self.logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)

            DOMAIN_ROLES = self.idm.getDomainRoles(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   START_INDEX,
                                                   COUNT)
            self.logger.debug("DOMAIN_ROLES=%s" % json.dumps(DOMAIN_ROLES, indent=3))

            ROLES = DOMAIN_ROLES

            self.logger.debug("ROLES=%s" % json.dumps(ROLES, indent=3))

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "ROLES": ROLES
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return ROLES, DOMAIN_NAME, None

    def roles_assignments(self,
                          DOMAIN_ID,
                          DOMAIN_NAME,
                          PROJECT_ID,
                          PROJECT_NAME,
                          ROLE_ID,
                          ROLE_NAME,
                          USER_ID,
                          USER_NAME,
                          ADMIN_USER,
                          ADMIN_PASSWORD,
                          ADMIN_TOKEN,
                          EFFECTIVE):

        '''Get roles assignments of a domain (and project).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: Name of domain
        - PROJECT_ID: id of project (optional)
        - PROJECT_NAME: name of project (optional)
        - ROLE_ID: id of role (optional)
        - ROLE_NAME: name of role (optional)
        - USER_ID: id of user (optional)
        - USER_NAME: name of user (optional)
        - ADMIN_USER: Service admin username
        - ADMIN_PASSWORD: Service admin password
        - ADMIN_TOKEN: Service admin token
        - EFFECTIVE: effective roles
        Return:
        - roles_assginments: array of role assignments
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "ROLE_NAME": "%s" % ROLE_NAME,
            "USER_ID": "%s" % USER_ID,
            "USER_NAME": "%s" % USER_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % "***", #ADMIN_PASSWORD,
            "ADMIN_TOKEN": self.get_extended_token(ADMIN_TOKEN),
            "EFFECTIVE:": "%s" % EFFECTIVE
        }
        self.logger.debug("FLOW roles_assignments invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                if not DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)
                else:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
            self.logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            # Ensure DOMAIN_NAME
            DOMAIN_NAME = self.ensure_service_name(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))
            self.logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)

            # Extract PROJECT, USER, ROLE IDs from NAME
            if not PROJECT_ID and PROJECT_NAME:
                PROJECT_ID = self.idm.getProjectId(ADMIN_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)
                self.logger.debug("PROJECT_ID=%s" % PROJECT_ID)

            if not USER_ID and USER_NAME:
                USER_ID = self.idm.getDomainUserId(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   USER_NAME)
                self.logger.debug("USER_ID=%s" % USER_ID)

            if not ROLE_ID and ROLE_NAME:
                ROLE_ID = self.idm.getDomainRoleId(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   ROLE_NAME)
                self.logger.debug("ROLE_ID=%s" % ROLE_ID)


            # if USER_ID:
            #     USER_ROLES = self.idm.getUserRoleAssignments(ADMIN_TOKEN,
            #                                                  USER_ID,
            #                                                  EFFECTIVE)
            #     self.logger.debug("USER_ROLES=%s" % json.dumps(USER_ROLES, indent=3))

            if PROJECT_ID:
                PROJECT_ROLES = self.idm.getProjectRoleAssignments(ADMIN_TOKEN,
                                                                   PROJECT_ID,
                                                                   EFFECTIVE)
                self.logger.debug("PROJECT_ROLES=%s" % json.dumps(PROJECT_ROLES,
                                                             indent=3))
                ROLE_ASSIGNMENTS = PROJECT_ROLES

            else:
                DOMAIN_ROLES = self.idm.getDomainRoleAssignments(ADMIN_TOKEN,
                                                                 DOMAIN_ID,
                                                                 EFFECTIVE)
                self.logger.debug("DOMAIN_ROLES=%s" % json.dumps(DOMAIN_ROLES,
                                                            indent=3))
                ROLE_ASSIGNMENTS = DOMAIN_ROLES

            role_assignments_expanded = []
            for role_assignment in ROLE_ASSIGNMENTS['role_assignments']:
                if 'group' in role_assignment:
                    continue
                if ROLE_ID:
                    if not (role_assignment['role']['id'] == ROLE_ID):
                        continue
                if PROJECT_ID:
                    if not (role_assignment['scope']['project']['id'] == PROJECT_ID):
                        continue
                if USER_ID:
                    if ('user' in role_assignment) and not (role_assignment['user']['id'] == USER_ID):
                        continue
                role_assignments_expanded.append(role_assignment)

            # Cache these data? -> memcached/redis
            domain_roles = self.idm.getDomainRoles(ADMIN_TOKEN, DOMAIN_ID)
            domain_roles['roles'].append(
                {
                    "name": "admin",
                    "id": self.idm.getRoleId(ADMIN_TOKEN, "admin")
                })
            domain_roles['roles'].append(
                {
                    "name": "service",
                    "id": self.idm.getRoleId(ADMIN_TOKEN, "service")
                })
            domain_users = self.idm.getDomainUsers(ADMIN_TOKEN, DOMAIN_ID)
            domain_projects = self.idm.getDomainProjects(ADMIN_TOKEN, DOMAIN_ID)

            inherit_roles = []
            if USER_ID:
                inherit_roles = self.idm.getUserDomainInheritRoleAssignments(
                    ADMIN_TOKEN,
                    DOMAIN_ID,
                    USER_ID)
            for assign in role_assignments_expanded:
                # Expand user detail
                if 'user' in assign:
                    match_list = [x for x in domain_users['users'] if x['id'] == str(assign['user']['id'])]
                    if len(match_list) > 0:
                        assign['user'].update(match_list[0])
                # Expand role detail
                match_list = [x for x in domain_roles['roles'] if str(x['id']) == str(assign['role']['id'])]
                if len(match_list) > 0:
                    assign['role'].update(match_list[0])

                # Expand if role is inherited
                if len(inherit_roles) > 0:
                    match_list = [x for x in inherit_roles['roles'] if str(x['id']) == str(assign['role']['id'])]
                    assign['role']['inherited'] = len(match_list) > 0

                # Expand project detail
                if 'project' in assign['scope']:
                    match_list = [x for x in domain_projects['projects'] if x['id'] == str(assign['scope']['project']['id'])]
                    if len(match_list) > 0:
                        assign['scope']['project'].update(match_list[0])

            self.logger.debug("ROLES=%s" % json.dumps(role_assignments_expanded,
                                                 indent=3))
        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "role_assignments": role_assignments_expanded,
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {"role_assignments": role_assignments_expanded}, DOMAIN_NAME, PROJECT_NAME

    def assignRoleServiceUser(self,
                              SERVICE_NAME,
                              SERVICE_ID,
                              SERVICE_ADMIN_USER,
                              SERVICE_ADMIN_PASSWORD,
                              SERVICE_ADMIN_TOKEN,
                              ROLE_NAME,
                              ROLE_ID,
                              SERVICE_USER_NAME,
                              SERVICE_USER_ID):

        '''Assigns a service role to an user in IoT keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_USER_NAME: User service name
        - SERVICE_USER_ID: User service Id
        Return:
        - ?
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID
        }
        self.logger.debug("assignRoleServiceUser invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                       SERVICE_ID))

            #
            # 2.  Get role
            #
            if not ROLE_ID and ROLE_NAME:
                if ROLE_NAME == "Admin":
                    SERVICE_ADMIN_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                          SERVICE_ADMIN_USER)
                    # Get KEYSTONE CONF from base idm class
                    roles = self.roles_assignments(SERVICE_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_TOKEN,
                                                   True)
                    for role in roles['role_assignments']:
                        if role['role']['name'] == 'admin':
                            ROLE_ID=role['role']['id']
                            break
                else:
                    ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                       SERVICE_ID,
                                                       ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3.  Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           SERVICE_USER_NAME)
            self.logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME,
                                                SERVICE_USER_ID))

            #
            # 4.  Grant role to user in service
            #
            self.idm.grantDomainRole(SERVICE_ADMIN_TOKEN,
                                     SERVICE_ID,
                                     SERVICE_USER_ID,
                                     ROLE_ID)
        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None

    def assignRoleSubServiceUser(self,
                                 SERVICE_NAME,
                                 SERVICE_ID,
                                 SUBSERVICE_NAME,
                                 SUBSERVICE_ID,
                                 SERVICE_ADMIN_USER,
                                 SERVICE_ADMIN_PASSWORD,
                                 SERVICE_ADMIN_TOKEN,
                                 ROLE_NAME,
                                 ROLE_ID,
                                 SERVICE_USER_NAME,
                                 SERVICE_USER_ID):

        '''Assigns a subservice role to an user in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_USER_NAME: User service name
        - SERVICE_USER_ID: User service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_NAME": "%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID
        }
        self.logger.debug("assignRoleSubServiceUser invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            # Ensure SERVICE_NAME
            if not SERVICE_NAME:
                SERVICE_NAME = self.idm.getDomainNameFromToken(SERVICE_ADMIN_TOKEN,
                                                               SERVICE_ID)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            #
            # 1. Get service (aka domain)
            #
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2. Get SubService (aka project)
            #
            if not SUBSERVICE_ID:
                SUBSERVICE_ID = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)
            # Ensure SUBSERVICE_NAME
            if not SUBSERVICE_NAME:
                SUBSERVICE_NAME = self.idm.getProjectNameFromToken(SERVICE_ADMIN_TOKEN,
                                                                   SERVICE_ID,
                                                                   SUBSERVICE_ID)
            self.logger.addFilter(ContextFilterSubService(SUBSERVICE_NAME))

            self.logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME,
                                                          SUBSERVICE_ID))

            #
            # 3. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 4. Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           SERVICE_USER_NAME)
            self.logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME,
                                                SERVICE_USER_ID))

            #
            # 5. Grant role to user in service
            #
            self.idm.grantProjectRole(SERVICE_ADMIN_TOKEN,
                                      SUBSERVICE_ID,
                                      SERVICE_USER_ID,
                                      ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, SUBSERVICE_NAME

    def assignInheritRoleServiceUser(self,
                                     SERVICE_NAME,
                                     SERVICE_ID,
                                     SERVICE_ADMIN_USER,
                                     SERVICE_ADMIN_PASSWORD,
                                     SERVICE_ADMIN_TOKEN,
                                     INHERIT_ROLE_NAME,
                                     INHERIT_ROLE_ID,
                                     SERVICE_USER_NAME,
                                     SERVICE_USER_ID):

        '''Assigns a subservice role to an user in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - INEHRIT_ROLE_NAME: Role name
        - INHERIT_ROLE_ID: Role Id
        - SERVICE_USER_NAME: User service name
        - SERVICE_USER_ID: User service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "INHERIT_ROLE_NAME": "%s" % INHERIT_ROLE_NAME,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID
        }
        self.logger.debug("assignRoleSubServiceUser invoked with: %s" % json.dumps(
            data_log, indent=3)
            )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                       SERVICE_ID))

            #
            # 2. Get role
            #
            if not INHERIT_ROLE_ID:
                INHERIT_ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           INHERIT_ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (INHERIT_ROLE_NAME,
                                                INHERIT_ROLE_ID))

            #
            # 3. Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           SERVICE_USER_NAME)
            self.logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME,
                                                SERVICE_USER_ID))

            #
            # 4. Grant inherit role to user in all subservices
            #
            self.idm.grantInheritRole(SERVICE_ADMIN_TOKEN,
                                      SERVICE_ID,
                                      SERVICE_USER_ID,
                                      INHERIT_ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "ID_USER": "%s" % SERVICE_USER_ID,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None

    def revokeRoleServiceUser(self,
                              SERVICE_NAME,
                              SERVICE_ID,
                              SERVICE_ADMIN_USER,
                              SERVICE_ADMIN_PASSWORD,
                              SERVICE_ADMIN_TOKEN,
                              ROLE_NAME,
                              ROLE_ID,
                              SERVICE_USER_NAME,
                              SERVICE_USER_ID):

        '''Revoke a service role to an user in IoT keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_USER_NAME: User service name
        - SERVICE_USER_ID: User service Id
        Return:
        - ?
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID
        }
        self.logger.debug("revokeRoleServiceUser invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                       SERVICE_ID))

            #
            # 2. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3. Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           SERVICE_USER_NAME)
            self.logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME,
                                                SERVICE_USER_ID))

            #
            # 4. Revoke role to user in service
            #
            self.idm.revokeDomainRole(SERVICE_ADMIN_TOKEN,
                                      SERVICE_ID,
                                      SERVICE_USER_ID,
                                      ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None

    def revokeRoleSubServiceUser(self,
                                 SERVICE_NAME,
                                 SERVICE_ID,
                                 SUBSERVICE_NAME,
                                 SUBSERVICE_ID,
                                 SERVICE_ADMIN_USER,
                                 SERVICE_ADMIN_PASSWORD,
                                 SERVICE_ADMIN_TOKEN,
                                 ROLE_NAME,
                                 ROLE_ID,
                                 SERVICE_USER_NAME,
                                 SERVICE_USER_ID):

        '''Revoke a subservice role to an user in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_USER_NAME: User service name
        - SERVICE_USER_ID: User service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_NAME": "%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID
        }
        self.logger.debug("revokeRoleSubServiceUser invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                       SERVICE_ID))

            #
            # 2. Get SubService (aka project)
            #
            if not SUBSERVICE_ID:
                SUBSERVICE_ID = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)

            self.logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME,
                                                          SUBSERVICE_ID))

            #
            # 3. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 4. Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           SERVICE_USER_NAME)
            self.logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME,
                                                SERVICE_USER_ID))

            #
            # 5. Revoke role to user in service
            #
            self.idm.revokeProjectRole(SERVICE_ADMIN_TOKEN,
                                       SUBSERVICE_ID,
                                       SERVICE_USER_ID,
                                       ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, SUBSERVICE_NAME

    def revokeInheritRoleServiceUser(self,
                                     SERVICE_NAME,
                                     SERVICE_ID,
                                     SERVICE_ADMIN_USER,
                                     SERVICE_ADMIN_PASSWORD,
                                     SERVICE_ADMIN_TOKEN,
                                     INHERIT_ROLE_NAME,
                                     INHERIT_ROLE_ID,
                                     SERVICE_USER_NAME,
                                     SERVICE_USER_ID):

        '''Revoke a subservice role to an user in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - INEHRIT_ROLE_NAME: Role name
        - INHERIT_ROLE_ID: Role Id
        - SERVICE_USER_NAME: User service name
        - SERVICE_USER_ID: User service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "INHERIT_ROLE_NAME": "%s" % INHERIT_ROLE_NAME,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID,
            "SERVICE_USER_NAME": "%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID": "%s" % SERVICE_USER_ID
        }
        self.logger.debug("revokeRoleSubServiceUser invoked with: %s" % json.dumps(
            data_log, indent=3)
            )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2. Get role
            #
            if not INHERIT_ROLE_ID:
                INHERIT_ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           INHERIT_ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (INHERIT_ROLE_NAME,
                                                INHERIT_ROLE_ID))

            #
            # 3. Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           SERVICE_USER_NAME)
            self.logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME,
                                                SERVICE_USER_ID))

            #
            # 4. Revoke inherit role to user in all subservices
            #
            self.idm.revokeInheritRole(SERVICE_ADMIN_TOKEN,
                                       SERVICE_ID,
                                       SERVICE_USER_ID,
                                       INHERIT_ROLE_ID)
        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "ID_USER": "%s" % SERVICE_USER_ID,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None


    def roles_assignments_groups(self,
                          DOMAIN_ID,
                          DOMAIN_NAME,
                          PROJECT_ID,
                          PROJECT_NAME,
                          ROLE_ID,
                          ROLE_NAME,
                          GROUP_ID,
                          GROUP_NAME,
                          ADMIN_USER,
                          ADMIN_PASSWORD,
                          ADMIN_TOKEN,
                          EFFECTIVE):

        '''Get roles assignments of a domain (and project).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: Name of domain
        - PROJECT_ID: id of project (optional)
        - PROJECT_NAME: name of project (optional)
        - ROLE_ID: id of role (optional)
        - ROLE_NAME: name of role (optional)
        - GROUP_ID: id of group (optional)
        - GROUP_NAME: name of group (optional)
        - ADMIN_USER: Service admin username
        - ADMIN_PASSWORD: Service admin password
        - ADMIN_TOKEN: Service admin token
        - EFFECTIVE: effective roles
        Return:
        - roles_assginments: array of role assignments
        '''
        data_log = {
            "DOMAIN_ID": "%s" % DOMAIN_ID,
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "PROJECT_ID": "%s" % PROJECT_ID,
            "PROJECT_NAME": "%s" % PROJECT_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "ROLE_NAME": "%s" % ROLE_NAME,
            "GROUP_ID": "%s" % GROUP_ID,
            "GROUP_NAME": "%s" % GROUP_NAME,
            "ADMIN_USER": "%s" % ADMIN_USER,
            "ADMIN_PASSWORD": "%s" % "***", #ADMIN_PASSWORD,
            "ADMIN_TOKEN": self.get_extended_token(ADMIN_TOKEN),
            "EFFECTIVE:": "%s" % EFFECTIVE
        }
        self.logger.debug("FLOW roles_assignments invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not ADMIN_TOKEN:
                if not DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)
                else:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
            self.logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            # Ensure DOMAIN_NAME
            DOMAIN_NAME = self.ensure_service_name(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   DOMAIN_NAME)
            self.logger.addFilter(ContextFilterService(DOMAIN_NAME))
            self.logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)

            # Extract PROJECT, USER, ROLE IDs from NAME
            if not PROJECT_ID and PROJECT_NAME:
                PROJECT_ID = self.idm.getProjectId(ADMIN_TOKEN,
                                                   DOMAIN_NAME,
                                                   PROJECT_NAME)
                self.logger.debug("PROJECT_ID=%s" % PROJECT_ID)

            if not GROUP_ID and GROUP_NAME:
                GROUP_ID = self.idm.getDomainGroupId(ADMIN_TOKEN,
                                                    DOMAIN_ID,
                                                    GROUP_NAME)
                self.logger.debug("GROUP_ID=%s" % GROUP_ID)

            if not ROLE_ID and ROLE_NAME:
                ROLE_ID = self.idm.getDomainRoleId(ADMIN_TOKEN,
                                                   DOMAIN_ID,
                                                   ROLE_NAME)
                self.logger.debug("ROLE_ID=%s" % ROLE_ID)


            # if USER_ID:
            #     USER_ROLES = self.idm.getUserRoleAssignments(ADMIN_TOKEN,
            #                                                  USER_ID,
            #                                                  EFFECTIVE)
            #     self.logger.debug("USER_ROLES=%s" % json.dumps(USER_ROLES, indent=3))

            if PROJECT_ID:
                PROJECT_ROLES = self.idm.getProjectRoleAssignments(ADMIN_TOKEN,
                                                                   PROJECT_ID,
                                                                   EFFECTIVE)
                self.logger.debug("PROJECT_ROLES=%s" % json.dumps(PROJECT_ROLES,
                                                             indent=3))
                ROLE_ASSIGNMENTS = PROJECT_ROLES

            else:
                DOMAIN_ROLES = self.idm.getDomainRoleAssignments(ADMIN_TOKEN,
                                                                 DOMAIN_ID,
                                                                 EFFECTIVE)
                self.logger.debug("DOMAIN_ROLES=%s" % json.dumps(DOMAIN_ROLES,
                                                            indent=3))
                ROLE_ASSIGNMENTS = DOMAIN_ROLES

            role_assignments_expanded = []
            for role_assignment in ROLE_ASSIGNMENTS['role_assignments']:
                if 'user' in role_assignment:
                    continue
                if ROLE_ID:
                    if not (role_assignment['role']['id'] == ROLE_ID):
                        continue
                if PROJECT_ID:
                    if not (role_assignment['scope']['project']['id'] == PROJECT_ID):
                        continue
                if GROUP_ID:
                    if  ('group' in role_assignment) and not (role_assignment['group']['id'] == GROUP_ID):
                        continue
                role_assignments_expanded.append(role_assignment)

            # Cache these data? -> memcached/redis
            domain_roles = self.idm.getDomainRoles(ADMIN_TOKEN, DOMAIN_ID)
            domain_roles['roles'].append(
                {
                    "name": "admin",
                    "id": self.idm.getRoleId(ADMIN_TOKEN, "admin")
                })
            domain_roles['roles'].append(
                {
                    "name": "service",
                    "id": self.idm.getRoleId(ADMIN_TOKEN, "service")
                })
            domain_groups = self.idm.getDomainGroups(ADMIN_TOKEN, DOMAIN_ID)
            domain_projects = self.idm.getDomainProjects(ADMIN_TOKEN, DOMAIN_ID)

            inherit_roles = []
            if GROUP_ID:
                inherit_roles = self.idm.getGroupDomainInheritRoleAssignments(
                    ADMIN_TOKEN,
                    DOMAIN_ID,
                    GROUP_ID)

            for assign in role_assignments_expanded:
                # Expand user detail
                match_list = [x for x in domain_groups['groups'] if x['id'] == str(assign['group']['id'])]
                if len(match_list) > 0:
                    assign['group'].update(match_list[0])

                # Expand role detail
                match_list = [x for x in domain_roles['roles'] if str(x['id']) == str(assign['role']['id'])]
                if len(match_list) > 0:
                    assign['role'].update(match_list[0])

                # Expand if role is inherited
                if len(inherit_roles) > 0:
                    match_list = [x for x in inherit_roles['roles'] if str(x['id']) == str(assign['role']['id'])]
                    assign['role']['inherited'] = len(match_list) > 0

                # Expand project detail
                if 'project' in assign['scope']:
                    match_list = [x for x in domain_projects['projects'] if x['id'] == str(assign['scope']['project']['id'])]
                    if len(match_list) > 0:
                        assign['scope']['project'].update(match_list[0])

            self.logger.debug("ROLES=%s" % json.dumps(role_assignments_expanded,
                                                 indent=3))
        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "role_assignments": role_assignments_expanded,
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {"role_assignments": role_assignments_expanded}, DOMAIN_NAME, PROJECT_NAME


    def assignRoleServiceGroup(self,
                              SERVICE_NAME,
                              SERVICE_ID,
                              SERVICE_ADMIN_USER,
                              SERVICE_ADMIN_PASSWORD,
                              SERVICE_ADMIN_TOKEN,
                              ROLE_NAME,
                              ROLE_ID,
                              SERVICE_GROUP_NAME,
                              SERVICE_GROUP_ID):

        '''Assigns a service role to a group in IoT keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_GROUP_NAME: Group service name
        - SERVICE_GROUP_ID: Group service Id
        Return:
        - ?
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_GROUP_NAME": "%s" % SERVICE_GROUP_NAME,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID
        }
        self.logger.debug("assignRoleServiceGroup invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2.  Get role
            #
            if not ROLE_ID and ROLE_NAME:
                if ROLE_NAME == "Admin":
                    SERVICE_ADMIN_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                          SERVICE_ADMIN_USER)
                    # Get KEYSTONE CONF from base idm class
                    roles = self.roles_assignments(SERVICE_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_TOKEN,
                                                   True)
                    for role in roles['role_assignments']:
                        if role['role']['name'] == 'admin':
                            ROLE_ID=role['role']['id']
                            break
                else:
                    ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                       SERVICE_ID,
                                                       ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3.  Get Group
            #
            if not SERVICE_GROUP_ID:
                SERVICE_GROUP_ID = self.idm.getDomainGroupId(SERVICE_ADMIN_TOKEN,
                                                             SERVICE_ID,
                                                             SERVICE_GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (SERVICE_GROUP_NAME,
                                                      SERVICE_GROUP_ID))

            #
            # 4.  Grant role to group in service
            #
            self.idm.grantDomainRoleToGroup(SERVICE_ADMIN_TOKEN,
                                            SERVICE_ID,
                                            SERVICE_GROUP_ID,
                                            ROLE_ID)
        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None


    def assignRoleSubServiceGroup(self,
                                  SERVICE_NAME,
                                  SERVICE_ID,
                                  SUBSERVICE_NAME,
                                  SUBSERVICE_ID,
                                  SERVICE_ADMIN_USER,
                                  SERVICE_ADMIN_PASSWORD,
                                  SERVICE_ADMIN_TOKEN,
                                  ROLE_NAME,
                                  ROLE_ID,
                                  SERVICE_GROUP_NAME,
                                  SERVICE_GROUP_ID):

        '''Assigns a subservice role to a group in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_GROUP_NAME: Group service name
        - SERVICE_GROUP_ID: Group service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_NAME": "%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_GROUP_NAME": "%s" % SERVICE_GROUP_NAME,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID
        }
        self.logger.debug("assignRoleSubServiceUser invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            # Ensure SERVICE_NAME
            if not SERVICE_NAME:
                SERVICE_NAME = self.idm.getDomainNameFromToken(SERVICE_ADMIN_TOKEN,
                                                               SERVICE_ID)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            #
            # 1. Get service (aka domain)
            #
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2. Get SubService (aka project)
            #
            if not SUBSERVICE_ID:
                SUBSERVICE_ID = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)
            # Ensure SUBSERVICE_NAME
            if not SUBSERVICE_NAME:
                SUBSERVICE_NAME = self.idm.getProjectNameFromToken(SERVICE_ADMIN_TOKEN,
                                                                   SERVICE_ID,
                                                                   SUBSERVICE_ID)
            self.logger.addFilter(ContextFilterSubService(SUBSERVICE_NAME))

            self.logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME,
                                                          SUBSERVICE_ID))

            #
            # 3. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 4. Get group
            #
            if not SERVICE_GROUP_ID:
                SERVICE_GROUP_ID = self.idm.getDomainGroupId(SERVICE_ADMIN_TOKEN,
                                                             SERVICE_ID,
                                                             SERVICE_GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (SERVICE_GROUP_NAME,
                                                      SERVICE_GROUP_ID))

            #
            # 5. Grant role to group in service
            #
            self.idm.grantProjectRoleToGroup(SERVICE_ADMIN_TOKEN,
                                             SUBSERVICE_ID,
                                             SERVICE_GROUP_ID,
                                             ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, SUBSERVICE_NAME


    def assignInheritRoleServiceGroup(self,
                                      SERVICE_NAME,
                                      SERVICE_ID,
                                      SERVICE_ADMIN_USER,
                                      SERVICE_ADMIN_PASSWORD,
                                      SERVICE_ADMIN_TOKEN,
                                      INHERIT_ROLE_NAME,
                                      INHERIT_ROLE_ID,
                                      SERVICE_GROUP_NAME,
                                      SERVICE_GROUP_ID):

        '''Assigns a subservice role to a group in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - INEHRIT_ROLE_NAME: Role name
        - INHERIT_ROLE_ID: Role Id
        - SERVICE_GROUP_NAME: Group service name
        - SERVICE_GROUP_ID: Group service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "INHERIT_ROLE_NAME": "%s" % INHERIT_ROLE_NAME,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID,
            "SERVICE_GROUP_NAME": "%s" % SERVICE_GROUP_NAME,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID
        }
        self.logger.debug("assignRoleSubServiceGroup invoked with: %s" % json.dumps(
            data_log, indent=3)
            )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2. Get role
            #
            if not INHERIT_ROLE_ID:
                INHERIT_ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           INHERIT_ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (INHERIT_ROLE_NAME,
                                                     INHERIT_ROLE_ID))

            #
            # 3. Get Group
            #
            if not SERVICE_GROUP_ID:
                SERVICE_GROUP_ID = self.idm.getDomainGroupId(SERVICE_ADMIN_TOKEN,
                                                             SERVICE_ID,
                                                             SERVICE_GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (SERVICE_GROUP_NAME,
                                                      SERVICE_GROUP_ID))

            #
            # 4. Grant inherit role to group in all subservices
            #
            self.idm.grantInheritRoleToGroup(SERVICE_ADMIN_TOKEN,
                                             SERVICE_ID,
                                             SERVICE_GROUP_ID,
                                             INHERIT_ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "ID_GROUP": "%s" % SERVICE_GROUP_ID,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None


    def revokeRoleServiceGroup(self,
                               SERVICE_NAME,
                               SERVICE_ID,
                               SERVICE_ADMIN_USER,
                               SERVICE_ADMIN_PASSWORD,
                               SERVICE_ADMIN_TOKEN,
                               ROLE_NAME,
                               ROLE_ID,
                               SERVICE_GROUP_NAME,
                               SERVICE_GROUP_ID):

        '''Revoke a service role to a group in IoT keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_GROUP_NAME: Group service name
        - SERVICE_GROUP_ID: Group service Id
        Return:
        - ?
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_GROUP_NAME": "%s" % SERVICE_GROUP_NAME,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID
        }
        self.logger.debug("revokeRoleServiceGroup invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3. Get Group
            #
            if not SERVICE_GROUP_ID:
                SERVICE_GROUP_ID = self.idm.getDomainGroupId(SERVICE_ADMIN_TOKEN,
                                                            SERVICE_ID,
                                                            SERVICE_GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (SERVICE_GROUP_NAME,
                                                      SERVICE_GROUP_ID))

            #
            # 4. Revoke role to group in service
            #
            self.idm.revokeDomainRoleToGroup(SERVICE_ADMIN_TOKEN,
                                             SERVICE_ID,
                                             SERVICE_GROUP_ID,
                                             ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None


    def revokeRoleSubServiceGroup(self,
                                 SERVICE_NAME,
                                 SERVICE_ID,
                                 SUBSERVICE_NAME,
                                 SUBSERVICE_ID,
                                 SERVICE_ADMIN_USER,
                                 SERVICE_ADMIN_PASSWORD,
                                 SERVICE_ADMIN_TOKEN,
                                 ROLE_NAME,
                                 ROLE_ID,
                                 SERVICE_GROUP_NAME,
                                 SERVICE_GROUP_ID):

        '''Revoke a subservice role to a group in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role Id
        - SERVICE_GROUP_NAME: Group service name
        - SERVICE_GROUP_ID: Group service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SUBSERVICE_NAME": "%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "SERVICE_GROUP_NAME": "%s" % SERVICE_GROUP_NAME,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID
        }
        self.logger.debug("revokeRoleSubServiceGroup invoked with: %s" % json.dumps(
            data_log, indent=3)
            )

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2. Get SubService (aka project)
            #
            if not SUBSERVICE_ID:
                SUBSERVICE_ID = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)

            self.logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME,
                                                               SUBSERVICE_ID))

            #
            # 3. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 4. Get Group
            #
            if not SERVICE_GROUP_ID:
                SERVICE_GROUP_ID = self.idm.getDomainGroupId(SERVICE_ADMIN_TOKEN,
                                                             SERVICE_ID,
                                                             SERVICE_GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (SERVICE_GROUP_NAME,
                                                      SERVICE_GROUP_ID))

            #
            # 5. Revoke role to user in service
            #
            self.idm.revokeProjectRoleToGroup(SERVICE_ADMIN_TOKEN,
                                              SUBSERVICE_ID,
                                              SERVICE_GROUP_ID,
                                              ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "SUBSERVICE_ID": "%s" % SUBSERVICE_ID,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, SUBSERVICE_NAME

    def revokeInheritRoleServiceGroup(self,
                                     SERVICE_NAME,
                                     SERVICE_ID,
                                     SERVICE_ADMIN_USER,
                                     SERVICE_ADMIN_PASSWORD,
                                     SERVICE_ADMIN_TOKEN,
                                     INHERIT_ROLE_NAME,
                                     INHERIT_ROLE_ID,
                                     SERVICE_GROUP_NAME,
                                     SERVICE_GROUP_ID):

        '''Revoke a subservice role to a group in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - INEHRIT_ROLE_NAME: Role name
        - INHERIT_ROLE_ID: Role Id
        - SERVICE_GROUP_NAME: Group service name
        - SERVICE_GROUP_ID: Group service Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "INHERIT_ROLE_NAME": "%s" % INHERIT_ROLE_NAME,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID,
            "SERVICE_GROUP_NAME": "%s" % SERVICE_GROUP_NAME,
            "SERVICE_GROUP_ID": "%s" % SERVICE_GROUP_ID
        }
        self.logger.debug("revokeRoleSubServiceGroup invoked with: %s" % json.dumps(
            data_log, indent=3)
            )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 1. Get service (aka domain)
            #
            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("ID of your service %s:%s" % (SERVICE_NAME,
                                                            SERVICE_ID))

            #
            # 2. Get role
            #
            if not INHERIT_ROLE_ID:
                INHERIT_ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           INHERIT_ROLE_NAME)
            self.logger.debug("ID of role %s: %s" % (INHERIT_ROLE_NAME,
                                                INHERIT_ROLE_ID))

            #
            # 3. Get Group
            #
            if not SERVICE_GROUP_ID:
                SERVICE_GROUP_ID = self.idm.getDomainGroupId(SERVICE_ADMIN_TOKEN,
                                                             SERVICE_ID,
                                                             SERVICE_GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (SERVICE_GROUP_NAME,
                                                      SERVICE_GROUP_ID))

            #
            # 4. Revoke inherit role to group in all subservices
            #
            self.idm.revokeInheritRoleToGroup(SERVICE_ADMIN_TOKEN,
                                              SERVICE_ID,
                                              SERVICE_GROUP_ID,
                                              INHERIT_ROLE_ID)
        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "ID_GROUP": "%s" % SERVICE_GROUP_ID,
            "INHERIT_ROLE_ID": "%s" % INHERIT_ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None


    def removeRole(self,
                   SERVICE_NAME,
                   SERVICE_ID,
                   SERVICE_ADMIN_USER,
                   SERVICE_ADMIN_PASSWORD,
                   SERVICE_ADMIN_TOKEN,
                   ROLE_NAME,
                   ROLE_ID):

        '''Removes an role Service (aka domain user keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role ID
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID
        }
        self.logger.debug("projects invoked with: %s" % json.dumps(data_log,
                                                              indent=3))
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))

            #
            # 2. Get Role ID
            #
            if not ROLE_ID and ROLE_NAME:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
                self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3. Remove role ID
            #
            self.idm.removeRole(SERVICE_ADMIN_TOKEN,
                                SERVICE_ID,
                                ROLE_ID)

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        data_log = {
            "ROLE_ID": ROLE_ID
        }
        self.logger.debug("Summary report : %s" % json.dumps(data_log, indent=3))

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None

    def setPolicyRole(self,
                      SERVICE_NAME,
                      SERVICE_ID,
                      SERVICE_ADMIN_USER,
                      SERVICE_ADMIN_PASSWORD,
                      SERVICE_ADMIN_TOKEN,
                      ROLE_NAME,
                      ROLE_ID,
                      POLICY_FILE_NAME):

        '''Set a new XACML policy for a role in Access Control.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role ID
        - POLICY_FILE_NAME: XACML policy
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "POLICY_FILE_NAME": "%s" % POLICY_FILE_NAME
        }
        self.logger.debug("set policy role invoked with: %s" % json.dumps(data_log,
                                                                indent=3))
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))

            #
            # 2. Get Role ID
            #
            if not ROLE_ID and ROLE_NAME:
                if ROLE_NAME == "Admin":
                    SERVICE_ADMIN_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                          SERVICE_ADMIN_USER)
                    roles = self.roles_assignments(SERVICE_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_TOKEN,
                                                   True)
                    for role in roles['role_assignments']:
                        if role['role']['name'] == 'admin':
                            ROLE_ID=role['role']['id']
                            break
                else:
                    ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                       SERVICE_ID,
                                                       ROLE_NAME)
                self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3. Set Policy Role
            #
            if self.idm.isTokenAdmin(SERVICE_ADMIN_TOKEN, SERVICE_ID):

                self.ac.provisionPolicy(SERVICE_NAME,
                                        SERVICE_ADMIN_TOKEN,
                                        ROLE_ID,
                                        POLICY_FILE_NAME)
            else:
                raise Exception("not admin role found to perform this action")

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None


    def removePolicyFromRole(self,
                      SERVICE_NAME,
                      SERVICE_ID,
                      SERVICE_ADMIN_USER,
                      SERVICE_ADMIN_PASSWORD,
                      SERVICE_ADMIN_TOKEN,
                      ROLE_NAME,
                      ROLE_ID,
                      POLICY_NAME):

        '''Remove a XACML policy for a role in Access Control.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role ID
        - POLICY_NAME: Policy name id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "POLICY_NAME": "%s" % POLICY_NAME
        }
        self.logger.debug("remove policy role invoked with: %s" % json.dumps(data_log,
                                                                indent=3))
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            #
            # 2. Get Role ID
            #
            if not ROLE_ID and ROLE_NAME:
                if ROLE_NAME == "Admin":
                    SERVICE_ADMIN_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                          SERVICE_ADMIN_USER)
                    roles = self.roles_assignments(SERVICE_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_TOKEN,
                                                   True)
                    for role in roles['role_assignments']:
                        if role['role']['name'] == 'admin':
                            ROLE_ID=role['role']['id']
                            break
                else:
                    ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                       SERVICE_ID,
                                                       ROLE_NAME)
                self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3. Delete Policy Role
            #
            if self.idm.isTokenAdmin(SERVICE_ADMIN_TOKEN, SERVICE_ID):

                self.ac.deleteRolePolicy(SERVICE_NAME,
                                         SERVICE_ADMIN_TOKEN,
                                         ROLE_ID,
                                         POLICY_NAME)
            else:
                raise Exception("not admin role found to perform this action")

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {}, SERVICE_NAME, None


    def getPolicyFromRole(self,
                      SERVICE_NAME,
                      SERVICE_ID,
                      SERVICE_ADMIN_USER,
                      SERVICE_ADMIN_PASSWORD,
                      SERVICE_ADMIN_TOKEN,
                      ROLE_NAME,
                      ROLE_ID,
                      POLICY_NAME):

        '''Get a XACML policy for a role in Access Control.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role ID
        - POLICY_NAME: Policy name id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % "***", #SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "ROLE_NAME": "%s" % ROLE_NAME,
            "ROLE_ID": "%s" % ROLE_ID,
            "POLICY_NAME": "%s" % POLICY_NAME
        }
        self.logger.debug("get policy role invoked with: %s" % json.dumps(data_log,
                                                                indent=3))
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            # Ensure SERVICE_NAME
            SERVICE_NAME = self.ensure_service_name(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    SERVICE_NAME)
            self.logger.addFilter(ContextFilterService(SERVICE_NAME))
            self.logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)

            #
            # 2. Get Role ID
            #
            if not ROLE_ID and ROLE_NAME:
                if ROLE_NAME == "Admin":
                    SERVICE_ADMIN_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                          SERVICE_ADMIN_USER)
                    roles = self.roles_assignments(SERVICE_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_ID,
                                                   None,
                                                   None,
                                                   None,
                                                   SERVICE_ADMIN_TOKEN,
                                                   True)
                    for role in roles['role_assignments']:
                        if role['role']['name'] == 'admin':
                            ROLE_ID=role['role']['id']
                            break
                else:
                    ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                       SERVICE_ID,
                                                       ROLE_NAME)
                self.logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3. Get Policy Role
            #
            if self.idm.isTokenAdmin(SERVICE_ADMIN_TOKEN, SERVICE_ID):

                POLICY = self.ac.getRolePolicy(SERVICE_NAME,
                                               SERVICE_ADMIN_TOKEN,
                                               ROLE_ID,
                                               POLICY_NAME)
            else:
                raise Exception("not admin role found to perform this action")

        except Exception as ex:
            error_code = self.composeErrorCode(ex)
            self.logError(self.logger, error_code, ex)
            return error_code

        # Consolidate opetions metrics into flow metrics
        self.collectComponentMetrics()

        return {"policy": POLICY}, SERVICE_NAME, None
