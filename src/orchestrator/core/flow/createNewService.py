import logging
import sys, os
import json

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')

class CreateNewService(FlowBase):

    def createNewService(self,
                         DOMAIN_NAME,
                         DOMAIN_ADMIN_USER,
                         DOMAIN_ADMIN_PASSWORD,
                         DOMAIN_ADMIN_TOKEN,
                         NEW_SERVICE_NAME,
                         NEW_SERVICE_DESCRIPTION,
                         NEW_SERVICE_ADMIN_USER,
                         NEW_SERVICE_ADMIN_PASSWORD):

        '''Creates a new Service (aka domain keystone).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_NAME: Domain name
        - DOMAIN_ADMIN_USER: admin user name in domain
        - DOMAIN_ADMIN_PASSWORD: admin password in domain
        - DOMAIN_ADMIN_TOKEN: admin user token in domain
        - NEW_SERVICE_NAME: New service name
        - NEW_SERVICE_DESCRIPTION: New service description
        - NEW_SERVICE_ADMIN_USER: New service admin username
        - NEW_SERVICE_ADMIN_PASSWORD: New service admin password
        Return:
        - token: service admin token
        - id: service Id
        '''

        SUB_SERVICE_ADMIN_ROLE_NAME="SubServiceAdmin"
        SUB_SERVICE_CUSTOMER_ROLE_NAME="SubServiceCustomer"

        data_log = {
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "DOMAIN_ADMIN_USER":"%s" % DOMAIN_ADMIN_USER,
            "DOMAIN_ADMIN_PASSWORD":"%s" % DOMAIN_ADMIN_PASSWORD,
            "DOMAIN_ADMIN_TOKEN":"%s" % DOMAIN_ADMIN_TOKEN,
            "NEW_SERVICE_NAME":"%s" % NEW_SERVICE_NAME,
            "NEW_SERVICE_DESCRIPTION":"%s" % NEW_SERVICE_DESCRIPTION,
            "NEW_SERVICE_ADMIN_USER":"%s" % NEW_SERVICE_ADMIN_PASSWORD
        }
        logger.debug("createNewService invoked with: %s" % json.dumps(data_log, indent=3))


        try:

            if not DOMAIN_ADMIN_TOKEN:
                DOMAIN_ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                       DOMAIN_ADMIN_USER,
                                                       DOMAIN_ADMIN_PASSWORD)
            logger.debug("DOMAIN_ADMIN_TOKEN=%s" % DOMAIN_ADMIN_TOKEN)


            #
            # 1. Create service (aka domain)
            #
            ID_DOM1 = self.idm.createDomain(DOMAIN_ADMIN_TOKEN,
                                            NEW_SERVICE_NAME,
                                            NEW_SERVICE_DESCRIPTION)
            logger.debug("ID of your new service %s:%s" % (NEW_SERVICE_NAME, ID_DOM1))

            #
            # 2. Create user admin for new service (aka domain)
            #
            ID_ADM1 = self.idm.createUserDomain(DOMAIN_ADMIN_TOKEN,
                                                ID_DOM1,
                                                NEW_SERVICE_NAME,
                                                NEW_SERVICE_ADMIN_USER,
                                                NEW_SERVICE_ADMIN_PASSWORD,
                                                None)  # TODO admin email

            logger.debug("ID of user %s: %s" % (NEW_SERVICE_ADMIN_USER, ID_ADM1))

            #
            # 3. Grant Admin role to $NEW_SERVICE_ADMIN_USER of new service
            #
            ADMIN_ROLE_ID = self.idm.getRoleId(DOMAIN_ADMIN_TOKEN,
                                               ROLE_NAME="admin")
            logger.debug("ID of role  %s: %s" % (NEW_SERVICE_ADMIN_USER, ID_ADM1))

            self.idm.grantDomainRole(DOMAIN_ADMIN_TOKEN, ID_DOM1, ID_ADM1, ADMIN_ROLE_ID)




            NEW_SERVICE_ADMIN_TOKEN = self.idm.getToken(NEW_SERVICE_NAME,
                                                        NEW_SERVICE_ADMIN_USER,
                                                        NEW_SERVICE_ADMIN_PASSWORD)
            logger.debug("NEW_SERVICE_ADMIN_TOKEN %s" % NEW_SERVICE_ADMIN_TOKEN)


            #
            # 4. Create SubService roles
            #
            ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN = self.idm.createDomainRole(
                NEW_SERVICE_ADMIN_TOKEN,
                SUB_SERVICE_ADMIN_ROLE_NAME,
                ID_DOM1)
            logger.debug("ID of role %s: %s" % (SUB_SERVICE_ADMIN_ROLE_NAME,
                                                ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN))

            ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER = self.idm.createDomainRole(
                NEW_SERVICE_ADMIN_TOKEN,
                SUB_SERVICE_CUSTOMER_ROLE_NAME,
                ID_DOM1)
            logger.debug("ID of role %s: %s" % (SUB_SERVICE_CUSTOMER_ROLE_NAME,
                                                ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER))

            #
            # 5. Provision default platform roles AccessControl policies
            #
            self.idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                     ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                     POLICY_FILE_NAME='policy-orion-admin.xml')
            self.idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                     ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                     POLICY_FILE_NAME='policy-perseo-admin.xml')
            self.idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                     ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                     POLICY_FILE_NAME='policy-orion-customer.xml')
            self.idm.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                     ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                     POLICY_FILE_NAME='policy-perseo-customer.xml')

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ID_DOM1":"%s" % ID_DOM1,
            "NEW_SERVICE_ADMIN_TOKEN":"%s" % NEW_SERVICE_ADMIN_TOKEN,
            "ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN":"%s" % ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN, 
            "ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER":"%s" % ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {
            "token": NEW_SERVICE_ADMIN_TOKEN,
            "id": ID_DOM1,
        }

