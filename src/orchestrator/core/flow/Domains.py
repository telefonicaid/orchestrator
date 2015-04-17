import logging
import json

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
        Return:
        - array list of domains
        '''
        data_log = {
            "DOMAIN_NAME":"%s" % DOMAIN_NAME,
            "ADMIN_USER":"%s" % ADMIN_USER,
            "ADMIN_PASSWORD":"%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN":"%s" % ADMIN_TOKEN
        }
        logger.debug("domains invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)


            DOMAINS = self.idm.getDomains(ADMIN_TOKEN)

            logger.debug("DOMAINS=%s" % json.dumps(DOMAINS, indent=3))

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAINS": DOMAINS
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
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
        Return:
        - domain detail
        '''
        data_log = {
            "DOMAIN_ID":"%s" % DOMAIN_ID,
            "DOMAIN_NAME":"%s" % DOMAIN_NAME,
            "ADMIN_USER":"%s" % ADMIN_USER,
            "ADMIN_PASSWORD":"%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN":"%s" % ADMIN_TOKEN
        }
        logger.debug("get_domain invoked with: %s" % json.dumps(data_log, indent=3))
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

            logger.debug("DOMAIN=%s" % DOMAIN)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAIN": DOMAIN
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DOMAIN

    def update_domain(self,
                      DOMAIN_ID,
                      DOMAIN_NAME,
                      ADMIN_USER,
                      ADMIN_PASSWORD,
                      ADMIN_TOKEN,
                      NEW_SERVICE_DESCRIPTION):

        '''Update Domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_SERVICE_DESCRIPTION: New service description
        Return:
        - domain detail
        '''
        data_log = {
            "DOMAIN_ID":"%s" % DOMAIN_ID,
            "DOMAIN_NAME":"%s" % DOMAIN_NAME,
            "ADMIN_USER":"%s" % ADMIN_USER,
            "ADMIN_PASSWORD":"%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN":"%s" % ADMIN_TOKEN,
            "NEW_SERVICE_DESCRIPTION":"%s" % NEW_SERVICE_DESCRIPTION,
        }
        logger.debug("updateDomain invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not ADMIN_TOKEN:
                # UpdateDomain can be only done by cloud_admin
                ADMIN_TOKEN = self.idm.getToken("admin_domain",
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            if not DOMAIN_ID:
                DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                 DOMAIN_NAME)

            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)
            DOMAIN = self.idm.updateDomain(ADMIN_TOKEN, DOMAIN_ID, NEW_SERVICE_DESCRIPTION)

            logger.debug("DOMAIN=%s" % DOMAIN)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAIN": DOMAIN
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DOMAIN

    def delete_domain(self,
                   DOMAIN_ID,
                   DOMAIN_NAME,
                   ADMIN_USER,
                   ADMIN_PASSWORD,
                   ADMIN_TOKEN):

        '''Delete a Domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID:
        - DOMAIN_NAME:
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - domain detail
        '''
        data_log = {
            "DOMAIN_ID":"%s" % DOMAIN_ID,
            "DOMAIN_NAME":"%s" % DOMAIN_NAME,
            "ADMIN_USER":"%s" % ADMIN_USER,
            "ADMIN_PASSWORD":"%s" % ADMIN_PASSWORD,
            "ADMIN_TOKEN":"%s" % ADMIN_TOKEN
        }
        logger.debug("delete_domain invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken("admin_domain",
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)

            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)
            # Another way:
            # if not DOMAIN_ID:
            #     DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
            #                                      DOMAIN_NAME)

            DOMAINS = self.idm.getDomains(ADMIN_TOKEN)

            for domain in DOMAINS['domains']:
                if domain['name'] == DOMAIN_NAME:
                    DOMAIN_ID = domain['id']
                    break

            DOMAIN = self.idm.disableDomain(ADMIN_TOKEN, DOMAIN_ID)

            self.idm.deleteDomain(ADMIN_TOKEN, DOMAIN_ID)

            # Delete policy of roles in Access Control
            self.ac.deleteTenantPolicies(DOMAIN_NAME, ADMIN_TOKEN)

            logger.debug("DOMAIN=%s" % DOMAIN)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DOMAIN": DOMAIN
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DOMAIN
