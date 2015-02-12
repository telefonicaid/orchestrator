import logging

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class Domains(FlowBase):

    def domains(self,
                DOMAIN_NAME,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Domains.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        '''

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)


            DOMAINS = self.idm.getDomains(ADMIN_TOKEN)

            logger.debug("DOMAINS=%s" % DOMAINS)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("DOMAINS=%s" % DOMAINS)
        return DOMAINS

    def get_domain(self,
                DOMAIN_ID,
                DOMAIN_NAME,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        '''

        try:
            if not ADMIN_TOKEN:
                if DOMAIN_ID:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
                else:
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)

            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            DOMAIN = self.idm.getDomain(ADMIN_TOKEN, DOMAIN_ID)

            logger.debug("DOMAINS=%s" % DOMAIN)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("DOMAIN=%s" % DOMAIN)

        return DOMAIN



