import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class Roles(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    def roles(self,
                DOMAIN_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Roles of a domain (and project).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        '''

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
            return { "error": str(ex) }

        logger.info("Summary report:")

        return ROLES

    def roles_assignments(self,
                DOMAIN_ID,
                PROJECT_ID,
                ROLE_ID,
                USER_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Roles of a domain (and project).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - PROJECT_ID: id of project (optional)
        - ROLE_ID: id of role (optional)
        - USER_ID: id of user (optional)
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        '''

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


            # Try to filter by PROJECT_ID each ROLE
            # Filter ROLE_ID and USER_ID ?
            res = []
            for role_assignment in ROLE_ASSIGNMENTS:
                if ROLE_ID:
                    if (role_assignment['role']['id'] == ROLE_ID):
                        # TODO: Expand role name into role_assignment role['role']
                        res.append(role_assignment)
                        continue
                if PROJECT_ID:
                    if (role_assignment['scope']['project']['id'] == PROJECT_ID):
                        # TODO: Expand project name into role_assignment role['scope']['project']
                        res.append(role_assignment)
                        continue
                if USER_ID:
                    if (role_assignment['user']['id'] == USER_ID):
                        # TODO: Expand user name into role_assignment role['user']
                        res.append(role_assignment)
                        continue

            domain_roles = self.idm.getDomainRoles(ADMIN_TOKEN, DOMAIN_ID)
            domain_users = self.idm.getDomainUsers(ADMIN_TOKEN, DOMAIN_ID)
            domain_projects = self.idm.getDomainProjects(ADMIN_TOKEN, DOMAIN_ID)

            # for assign in res:
            #     assign['user']['name'] = filter(lambda x: x['id'] == str(assign['user']['id']), domain_users)[0]['name']

            logger.debug("ROLES=%s" % res)

        except Exception, ex:
            logger.error(ex)
            return { "error": str(ex) }

        logger.info("Summary report:")

        return { "roles-assginments": res }

