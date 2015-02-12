import logging

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
        logger.debug("roles invoked with: ")
        logger.debug("DOMAIN_ID=%s" % DOMAIN_ID)
        logger.debug("ADMIN_USER=%s" % ADMIN_USER)
        logger.debug("ADMIN_PASSWORD=%s" % ADMIN_PASSWORD)
        logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            DOMAIN_ROLES = self.idm.getDomainRoles(ADMIN_TOKEN,
                                                   DOMAIN_ID)
            logger.debug("DOMAIN_ROLES=%s" % ADMIN_TOKEN)

            ROLES = DOMAIN_ROLES

            logger.debug("ROLES=%s" % ROLES)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("ROLES=%s" % ROLES)

        return ROLES


    def roles_assignments(self,
                DOMAIN_ID,
                PROJECT_ID,
                ROLE_ID,
                USER_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get roles assignments of a domain (and project).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - PROJECT_ID: id of project (optional)
        - ROLE_ID: id of role (optional)
        - USER_ID: id of user (optional)
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - roles_assginments: array of role assignments
        '''
        logger.debug("roles_assignments invoked with: ")
        logger.debug("DOMAIN_ID=%s" % DOMAIN_ID)
        logger.debug("PROJECT_ID=%s" % PROJECT_ID)
        logger.debug("ROLE_ID=%s" % ROLE_ID)
        logger.debug("USER_ID=%s" % USER_ID)
        logger.debug("ADMIN_USER=%s" % ADMIN_USER)
        logger.debug("ADMIN_PASSWORD=%s" % ADMIN_PASSWORD)
        logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)
        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            if PROJECT_ID:
                PROJECT_ROLES = self.idm.getProjectRoleAssignments(ADMIN_TOKEN,
                                                                   PROJECT_ID)
                logger.debug("PROJECT_ROLES=%s" % PROJECT_ROLES)
                ROLE_ASSIGNMENTS = PROJECT_ROLES

            else:
                DOMAIN_ROLES = self.idm.getDomainRoleAssignments(ADMIN_TOKEN,
                                                                 DOMAIN_ID)
                logger.debug("DOMAIN_ROLES=%s" % DOMAIN_ROLES)
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

        logger.info("Summary report:")
        logger.info("role_assignments=%s" % role_assignments_expanded)

        return { "roles_assignments": role_assignments_expanded }


    def assignRoleServiceUser(self,
                              SERVICE_NAME,
                              SERVICE_ADMIN_USER,
                              SERVICE_ADMIN_PASSWORD,
                              SERVICE_ADMIN_TOKEN,
                              ROLE_NAME,
                              SERVICE_USER_NAME):

        '''Assigns a service role to an user in IoT keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - SERVICE_USER_NAME: User service name
        Return:
        - ?
        '''
        logger.debug("assignRoleServiceUser invoked with: ")
        logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)
        logger.debug("SERVICE_ADMIN_USER=%s" % SERVICE_ADMIN_USER)
        logger.debug("SERVICE_ADMIN_PASSWORD=%s" % SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)
        logger.debug("ROLE_NAME=%s" % ROLE_NAME)
        logger.debug("SERVICE_USER_NAME=%s" % SERVICE_USER_NAME)

        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #
            ID_DOM1 = self.idm.getDomain(SERVICE_ADMIN_TOKEN,
                                    SERVICE_NAME)

            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, ID_DOM1))

            #
            # 2.  Get role
            #
            ID_ROLE = self.idm.getRoleId(SERVICE_ADMIN_TOKEN,
                                         ROLE_NAME)
            logger.debug("ID of user %s: %s" % (ROLE_NAME, ID_ROLE))

            #
            # 3.  Get User
            #
            ID_USER = self.idm.getUserId(SERVICE_ADMIN_TOKEN,
                                         SERVICE_USER_NAME)
            logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, ID_USER))


            #
            # 4.  Grant role to user in service
            #
            self.idm.grantDomainRole(SERVICE_ADMIN_TOKEN,
                                     ID_DOM1,
                                     ID_USER,
                                     ID_ROLE)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("ID_DOM1=%s" % ID_DOM1)
        logger.info("ID_USER=%s" % ID_USER)
        logger.info("ID_ROLE=%s" % ID_ROLE)


    def assignRoleSubServiceUser(self,
                                 SERVICE_NAME,
                                 SUBSERVICE_NAME,
                                 SERVICE_ADMIN_USER,
                                 SERVICE_ADMIN_PASSWORD,
                                 SERVICE_ADMIN_TOKEN,
                                 ROLE_NAME,
                                 SERVICE_USER_NAME):

        '''Assigns a subservice role to an user in IoT keystone.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SUBSERVICE_NAME: SubService name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - SERVICE_USER_NAME: User service name
        '''
        logger.debug("assignRoleSubServiceUser invoked with: ")
        logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)
        logger.debug("SUBSERVICE_NAME=%s" % SUBSERVICE_NAME)
        logger.debug("SERVICE_ADMIN_USER=%s" % SERVICE_ADMIN_USER)
        logger.debug("SERVICE_ADMIN_PASSWORD=%s" % SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)
        logger.debug("ROLE_NAME=%s" % ROLE_NAME)
        logger.debug("SERVICE_USER_NAME=%s" % SERVICE_USER_NAME)
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #

            ID_DOM1 = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                           SERVICE_NAME)

            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, ID_DOM1))



            #
            # 2. Get SubService (aka project)
            #

            ID_PRO1 = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                            SERVICE_NAME,
                                            SUBSERVICE_NAME)

            logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME, ID_PRO1))

            #
            # 3. Get role
            #
            ID_ROLE = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                               ID_DOM1,
                                               ROLE_NAME)
            logger.debug("ID of role %s: %s" % (ROLE_NAME, ID_ROLE))

            #
            # 4. Get User
            #
            ID_USER = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                               ID_DOM1,
                                               SERVICE_USER_NAME)
            logger.debug("ID of user %s: %s" % (SERVICE_USER_NAME, ID_USER))


            #
            # 5. Grant role to user in service
            #
            self.idm.grantProjectRole(SERVICE_ADMIN_TOKEN,
                                      ID_PRO1,
                                      ID_USER,
                                      ID_ROLE)


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("ID_PRO1=%s" % ID_PRO1)
        logger.info("ID_USER=%s" % ID_USER)
        logger.info("ID_ROLE=%s" % ID_ROLE)
