import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class Projects(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    def projects(self,
                DOMAIN_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Projects of a domain.

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


            PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
                                                  DOMAIN_ID)

            logger.debug("PROJECTS=%s" % PROJECTS)

        except Exception, ex:
            logger.error(ex)
            return { "error": str(ex) }

        logger.info("Summary report:")

        return PROJECTS

    def get_project(self,
                DOMAIN_ID,
                PROJECT_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Projects of a domain.

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


            PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
                                                  DOMAIN_ID)
            for project in PROJECTS:
                if project['id'] == PROJECT_ID:
                    PROJECT = project

            logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            logger.error(ex)
            return { "error": str(ex) }

        logger.info("Summary report:")

        return PROJECT



