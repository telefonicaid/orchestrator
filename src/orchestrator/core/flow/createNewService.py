import logging
import sys, os

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')

class CreateNewService(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT,
                 KEYPASS_PROTOCOL,
                 KEYPASS_HOST,
                 KEYPASS_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT,
                                 KEYPASS_PROTOCOL, KEYPASS_HOST, KEYPASS_PORT)
        

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
        - TOKEN: service admin token
        '''
    
        SUB_SERVICE_ADMIN_ROLE_NAME="SubServiceAdmin"
        SUB_SERVICE_CUSTOMER_ROLE_NAME="SubServiceCustomer"
        
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
                                                NEW_SERVICE_ADMIN_PASSWORD)
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
            

        #except Exception, ex:
        except AssertionError, ex:        
            logger.error(ex)
            
            # Get line where exception was produced
            #exc_type, exc_obj, exc_tb = sys.exc_info()
            #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)

            res = { "error": str(ex), "code": 400 }
            
            if isinstance(ex.message, tuple):
                res['code'] = ex.message[0]

            return res


        logger.info("Summary report:")
        logger.info("ID_DOM1=%s" % ID_DOM1)
        logger.info("NEW_SERVICE_ADMIN_TOKEN=%s" % NEW_SERVICE_ADMIN_TOKEN)
        logger.info("ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN=%s" % ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN)
        logger.info("ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER=%s" % ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER)
        
        return {
            "token": NEW_SERVICE_ADMIN_TOKEN,
            "id": ID_DOM1,
        }

