import logging
import json

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class Roles(FlowBase):

    def roles(self,
                DOMAIN_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Roles of a domain

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - array list of roles
        '''
        data_log = {
            "DOMAIN_ID":"%s" % DOMAIN_ID,
            "ADMIN_USER":"%s" % ADMIN_USER,
            "ADMIN_PASSWORD":"%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN":"%s" % ADMIN_TOKEN
        }
        logger.debug("roles invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            DOMAIN_ROLES = self.idm.getDomainRoles(ADMIN_TOKEN,
                                                   DOMAIN_ID)
            logger.debug("DOMAIN_ROLES=%s" % json.dumps(DOMAIN_ROLES, indent=3))

            ROLES = DOMAIN_ROLES

            logger.debug("ROLES=%s" %  json.dumps(ROLES, indent=3))

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ROLES":"%s" % ROLES
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return ROLES


    def roles_assignments(self,
                DOMAIN_ID,
                PROJECT_ID,
                ROLE_ID,
                USER_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN,
                EFFECTIVE):

        '''Get roles assignments of a domain (and project).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - PROJECT_ID: id of project (optional)
        - ROLE_ID: id of role (optional)
        - USER_ID: id of user (optional)
        - ADMIN_USER: Service admin username
        - ADMIN_PASSWORD: Service admin password
        - ADMIN_TOKEN: Service admin token
        - EFFECTIVE: effective roles
        Return:
        - roles_assginments: array of role assignments
        '''
        data_log = {
            "DOMAIN_ID":"%s" % DOMAIN_ID,
            "PROJECT_ID":"%s" % PROJECT_ID,
            "ROLE_ID":"%s" % ROLE_ID,
            "USER_ID":"%s" % USER_ID,
            "ADMIN_USER":"%s" % ADMIN_USER,
            "ADMIN_PASSWORD":"%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN":"%s" % ADMIN_TOKEN,
            "EFFECTIVE:":"%s" % EFFECTIVE
        }
        logger.debug("roles_assignments invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            if PROJECT_ID:
                PROJECT_ROLES = self.idm.getProjectRoleAssignments(ADMIN_TOKEN,
                                                                   PROJECT_ID,
                                                                   EFFECTIVE)
                logger.debug("PROJECT_ROLES=%s" % json.dumps(PROJECT_ROLES, indent=3))
                ROLE_ASSIGNMENTS = PROJECT_ROLES

            else:
                DOMAIN_ROLES = self.idm.getDomainRoleAssignments(ADMIN_TOKEN,
                                                                 DOMAIN_ID,
                                                                 EFFECTIVE)
                logger.debug("DOMAIN_ROLES=%s" % json.dumps(DOMAIN_ROLES, indent=3))
                ROLE_ASSIGNMENTS = DOMAIN_ROLES

            role_assignments_expanded = []
            for role_assignment in ROLE_ASSIGNMENTS['role_assignments']:
                # # 'OR' Filter
                # if ROLE_ID:
                #     if (role_assignment['role']['id'] == ROLE_ID):
                #         role_assignments_expanded.append(role_assignment)
                #         continue
                # if PROJECT_ID:
                #     if (role_assignment['scope']['project']['id'] == PROJECT_ID):
                #         role_assignments_expanded.append(role_assignment)
                #         continue
                # if USER_ID:
                #     if (role_assignment['user']['id'] == USER_ID):
                #         role_assignments_expanded.append(role_assignment)
                #         continue
                # 'AND' filter
                if ROLE_ID:
                    if not (role_assignment['role']['id'] == ROLE_ID):
                        continue
                if PROJECT_ID:
                    if not (role_assignment['scope']['project']['id'] == PROJECT_ID):
                        continue
                if USER_ID:
                    if not (role_assignment['user']['id'] == USER_ID):
                        continue
                role_assignments_expanded.append(role_assignment)


            # Cache these data? -> memcached/redis
            domain_roles = self.idm.getDomainRoles(ADMIN_TOKEN, DOMAIN_ID)
            # TOOD: add to domain_roles also tenant roles like admin and service
            domain_users = self.idm.getDomainUsers(ADMIN_TOKEN, DOMAIN_ID)
            domain_projects = self.idm.getDomainProjects(ADMIN_TOKEN, DOMAIN_ID)

            for assign in role_assignments_expanded:
                # Expand user detail
                match_list = [x for x in domain_users['users'] if x['id'] == str(assign['user']['id'])]
                if len(match_list) > 0:
                    assign['user'].update(match_list[0])
                # Expand role detail
                match_list = [x for x in domain_roles['roles'] if str(x['id']) == str(assign['role']['id'])]
                if len(match_list) > 0:
                    assign['role'].update(match_list[0])
                # Expand project detail
                if 'project' in assign['scope']:
                    match_list = [x for x in domain_projects['projects'] if x['id'] == str(assign['scope']['project']['id'])]
                    if len(match_list) > 0:
                        assign['scope']['project'].update(match_list[0])


            logger.debug("ROLES=%s" % role_assignments_expanded)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "role_assignments":"%s" % role_assignments_expanded,
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return { "role_assignments": role_assignments_expanded }


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
            "SERVICE_NAME":"%s" % SERVICE_NAME,
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN,
            "ROLE_NAME":"%s" % ROLE_NAME,
            "ROLE_ID":"%s" % ROLE_ID,
            "SERVICE_USER_NAME":"%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID":"%s" % SERVICE_USER_ID
        }
        logger.debug("assignRoleServiceUser invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                            SERVICE_ADMIN_USER,
                                                            SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                             SERVICE_ADMIN_USER,
                                                             SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #
            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, SERVICE_ID))

            #
            # 2.  Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getRoleId(SERVICE_ADMIN_TOKEN,
                                             ROLE_NAME)
            logger.debug("ID of user %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 3.  Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                                     SERVICE_USER_NAME)
            logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, SERVICE_USER_ID))


            #
            # 4.  Grant role to user in service
            #
            self.idm.grantDomainRole(SERVICE_ADMIN_TOKEN,
                                     SERVICE_ID,
                                     SERVICE_USER_ID,
                                     ROLE_ID)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SERVICE_USER_ID":"%s" % SERVICE_USER_ID,
            "ROLE_ID":"%s" % ROLE_ID
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))


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
            "SERVICE_NAME":"%s" % SERVICE_NAME,
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SUBSERVICE_NAME":"%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID":"%s" % SUBSERVICE_ID,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN,
            "ROLE_NAME":"%s" % ROLE_NAME,
            "ROLE_ID":"%s" % ROLE_ID,
            "SERVICE_USER_NAME":"%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID":"%s" % SERVICE_USER_ID
        }
        logger.debug("assignRoleSubServiceUser invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                            SERVICE_ADMIN_USER,
                                                            SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                             SERVICE_ADMIN_USER,
                                                             SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #
            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, SERVICE_ID))



            #
            # 2. Get SubService (aka project)
            #
            if not SUBSERVICE_ID:
                SUBSERVICE_ID = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)

            logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME, SUBSERVICE_ID))

            #
            # 3. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))

            #
            # 4. Get User
            #
            if not SERVICE_USER_ID:
                SERVICE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           SERVICE_USER_NAME)
            logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, SERVICE_USER_ID))


            #
            # 5. Grant role to user in service
            #
            self.idm.grantProjectRole(SERVICE_ADMIN_TOKEN,
                                      SUBSERVICE_ID,
                                      SERVICE_USER_ID,
                                      ROLE_ID)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "SUBSERVICE_ID":"%s" % SUBSERVICE_ID,
            "SERVICE_USER_ID":"%s" % SERVICE_USER_ID,
            "ROLE_ID":"%s" % ROLE_ID
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

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
            "SERVICE_NAME":"%s" % SERVICE_NAME,
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN,
            "INHERIT_ROLE_NAME":"%s" % INHERIT_ROLE_NAME,
            "INHERIT_ROLE_ID":"%s" % INHERIT_ROLE_ID,
            "SERVICE_USER_NAME":"%s" % SERVICE_USER_NAME,
            "SERVICE_USER_ID":"%s" % SERVICE_USER_ID
        }
        logger.debug("assignRoleSubServiceUser invoked with: %s" % json.dumps(data_log, indent=3))
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                            SERVICE_ADMIN_USER,
                                                            SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(SERVICE_ID,
                                                             SERVICE_ADMIN_USER,
                                                             SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #
            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, SERVICE_ID))

            #
            # 2. Get role
            #
            if not INHERIT_ROLE_ID:
                INHERIT_ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           INHERIT_ROLE_NAME)
            logger.debug("ID of role %s: %s" % (INHERIT_ROLE_NAME, INHERIT_ROLE_ID))

            #
            # 3. Get User
            #
            ID_USER = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                         SERVICE_USER_NAME)
            logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, ID_USER))


            #
            # 4. Grant inherit role to user in all subservices
            #
            self.idm.grantInheritRole(SERVICE_ADMIN_TOKEN,
                                      ID_USER,
                                      INHERIT_ROLE_ID)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ID_USER":"%s" % ID_USER,
            "INHERIT_ROLE_ID":"%s" % INHERIT_ROLE_ID
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
