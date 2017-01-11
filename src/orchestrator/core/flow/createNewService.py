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


class CreateNewService(FlowBase):

    def createNewService(self,
                         DOMAIN_NAME,
                         DOMAIN_ADMIN_USER,
                         DOMAIN_ADMIN_PASSWORD,
                         DOMAIN_ADMIN_TOKEN,
                         NEW_SERVICE_NAME,
                         NEW_SERVICE_DESCRIPTION,
                         NEW_SERVICE_ADMIN_USER,
                         NEW_SERVICE_ADMIN_PASSWORD,
                         NEW_SERVICE_ADMIN_EMAIL):

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
        - NEW_SERVICE_ADMIN_EMAIL: New service admin email (optional)
        Return:
        - token: service admin token
        - id: service Id
        '''

        SUB_SERVICE_ADMIN_ROLE_NAME = "SubServiceAdmin"
        SUB_SERVICE_CUSTOMER_ROLE_NAME = "SubServiceCustomer"
        SERVICE_CUSTOMER_ROLE_NAME = "ServiceCustomer"

        data_log = {
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "DOMAIN_ADMIN_USER": "%s" % DOMAIN_ADMIN_USER,
            "DOMAIN_ADMIN_PASSWORD": "%s" % DOMAIN_ADMIN_PASSWORD,
            "DOMAIN_ADMIN_TOKEN": self.get_extended_token(DOMAIN_ADMIN_TOKEN),
            "NEW_SERVICE_NAME": "%s" % NEW_SERVICE_NAME,
            "NEW_SERVICE_DESCRIPTION": "%s" % NEW_SERVICE_DESCRIPTION,
            "NEW_SERVICE_ADMIN_USER": "%s" % NEW_SERVICE_ADMIN_USER,
            "NEW_SERVICE_ADMIN_PASSWORD": "%s" % NEW_SERVICE_ADMIN_PASSWORD,
            "NEW_SERVICE_ADMIN_EMAIL": "%s" % NEW_SERVICE_ADMIN_EMAIL
        }
        self.logger.debug("FLOW createNewService invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        ID_DOM1=None
        try:

            if not DOMAIN_ADMIN_TOKEN:
                DOMAIN_ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                       DOMAIN_ADMIN_USER,
                                                       DOMAIN_ADMIN_PASSWORD)
            self.logger.debug("DOMAIN_ADMIN_TOKEN=%s" % DOMAIN_ADMIN_TOKEN)

            #
            # 1. Create service (aka domain)
            #
            ID_DOM1 = self.idm.createDomain(DOMAIN_ADMIN_TOKEN,
                                            NEW_SERVICE_NAME,
                                            NEW_SERVICE_DESCRIPTION)
            self.logger.debug("ID of your new service %s:%s" % (NEW_SERVICE_NAME,
                                                           ID_DOM1))

            #
            # 2. Create user admin for new service (aka domain)
            #
            try:
                ID_ADM1 = self.idm.createUserDomain(DOMAIN_ADMIN_TOKEN,
                                                ID_DOM1,
                                                NEW_SERVICE_NAME,
                                                NEW_SERVICE_ADMIN_USER,
                                                NEW_SERVICE_ADMIN_PASSWORD,
                                                NEW_SERVICE_ADMIN_EMAIL,
                                                None)
            except Exception, ex:
                self.logger.warn("ERROR creating user %s: %s" % (
                    NEW_SERVICE_ADMIN_USER,
                    ex))
                self.logger.info("removing uncomplete created domain %s" % ID_DOM1)
                self.idm.disableDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
                self.idm.deleteDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
                return self.composeErrorCode(ex)

            self.logger.debug("ID of user %s: %s" % (NEW_SERVICE_ADMIN_USER,
                                                ID_ADM1))

            #
            # 3. Grant Admin role to $NEW_SERVICE_ADMIN_USER of new service
            #
            ADMIN_ROLE_ID = self.idm.getRoleId(DOMAIN_ADMIN_TOKEN,
                                               ROLE_NAME="admin")
            self.logger.debug("ID of role  %s: %s" % ("admin",
                                                 ADMIN_ROLE_ID))

            self.idm.grantDomainRole(DOMAIN_ADMIN_TOKEN, ID_DOM1, ID_ADM1,
                                     ADMIN_ROLE_ID)

            NEW_SERVICE_ADMIN_TOKEN = self.idm.getToken(
                NEW_SERVICE_NAME,
                NEW_SERVICE_ADMIN_USER,
                NEW_SERVICE_ADMIN_PASSWORD)
            self.logger.debug("NEW_SERVICE_ADMIN_TOKEN %s" % NEW_SERVICE_ADMIN_TOKEN)

            #
            # 4. Create SubService roles
            #
            ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN = self.idm.createDomainRole(
                NEW_SERVICE_ADMIN_TOKEN,
                SUB_SERVICE_ADMIN_ROLE_NAME,
                ID_DOM1)
            self.logger.debug("ID of role %s: %s" % (SUB_SERVICE_ADMIN_ROLE_NAME,
                                                ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN))

            ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER = self.idm.createDomainRole(
                NEW_SERVICE_ADMIN_TOKEN,
                SUB_SERVICE_CUSTOMER_ROLE_NAME,
                ID_DOM1)
            self.logger.debug("ID of role %s: %s" % (SUB_SERVICE_CUSTOMER_ROLE_NAME,
                                                ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER))
            #
            # 4.1 Create ServiceCustomer role
            #
            ID_NEW_SERVICE_ROLE_SERVICECUSTOMER = self.idm.createDomainRole(
                NEW_SERVICE_ADMIN_TOKEN,
                SERVICE_CUSTOMER_ROLE_NAME,
                ID_DOM1)
            self.logger.debug("ID of role %s: %s" % (SERVICE_CUSTOMER_ROLE_NAME,
                                                ID_NEW_SERVICE_ROLE_SERVICECUSTOMER))

            #
            # 4.5 Inherit subserviceadim
            #
            self.idm.grantInheritRole(NEW_SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      ID_ADM1,
                                      ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN)
            #
            # 5. Provision default platform roles AccessControl policies
            #

            # Policies for SubServiceAdmin Role
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-orion-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-perseo-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-iotagent-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-sth-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-keypass-admin.xml')
            # Policies for SubServiceCustomer Role
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-orion-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-perseo-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-iotagent-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-sth-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-keypass-customer.xml')
            # Policies for Admin Role
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-orion-admin2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-perseo-admin2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-iotagent-admin2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-sth-admin2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-keypass-admin2.xml')
            # Policies for ServiceCustomer Role
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-orion-customer2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-perseo-customer2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-iotagent-customer2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-sth-customer2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-keypass-customer2.xml')

            #
            # 6. Create groups for new service (aka domain)
            #
            ADMIN_GROUP_NAME = "AdminGroup"
            SERVICE_CUSTOMER_GROUP_NAME = "ServiceCustomerGroup"
            SUB_SERVICE_ADMIN_GROUP_NAME = "SubServiceAdminGroup"
            SUB_SERVICE_CUSTOMER_GROUP_NAME = "SubServiceCustomerGroup"

            try:
                ID_ADMIN_GROUP = self.idm.createGroupDomain(DOMAIN_ADMIN_TOKEN,
                                                      ID_DOM1,
                                                      NEW_SERVICE_NAME,
                                                      ADMIN_GROUP_NAME,
                                                      None)

                ID_SERVICE_CUSTOMER_GROUP = self.idm.createGroupDomain(DOMAIN_ADMIN_TOKEN,
                                                      ID_DOM1,
                                                      NEW_SERVICE_NAME,
                                                      SERVICE_CUSTOMER_GROUP_NAME,
                                                      None)

                ID_SUB_SERVICE_ADMIN_GROUP = self.idm.createGroupDomain(DOMAIN_ADMIN_TOKEN,
                                                      ID_DOM1,
                                                      NEW_SERVICE_NAME,
                                                      SUB_SERVICE_CUSTOMER_GROUP_NAME,
                                                      None)

                ID_SUB_SERVICE_CUSTOMER_GROUP = self.idm.createGroupDomain(DOMAIN_ADMIN_TOKEN,
                                                      ID_DOM1,
                                                      NEW_SERVICE_NAME,
                                                      SUB_SERVICE_ADMIN_GROUP_NAME,
                                                      None)


            except Exception, ex:
                self.logger.warn("ERROR creating groups  %s" % (
                    ex))
                self.logger.info("removing uncomplete created domain %s" % ID_DOM1)
                self.idm.disableDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
                self.idm.deleteDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
                return self.composeErrorCode(ex)

            self.logger.debug("ID of group %s: %s" % (ADMIN_GROUP_NAME,
                                                      ID_ADMIN_GROUP))
            self.logger.debug("ID of group %s: %s" % (SERVICE_CUSTOMER_GROUP_NAME,
                                                      ID_SERVICE_CUSTOMER_GROUP))
            self.logger.debug("ID of group %s: %s" % (SUB_SERVICE_ADMIN_GROUP_NAME,
                                                      ID_SUB_SERVICE_ADMIN_GROUP))
            self.logger.debug("ID of group %s: %s" % (SUB_SERVICE_CUSTOMER_GROUP_NAME,
                                                      ID_SUB_SERVICE_CUSTOMER_GROUP))


            self.idm.grantDomainRoleToGroup(DOMAIN_ADMIN_TOKEN,
                                     ID_DOM1,
                                     ID_ADMIN_GROUP,
                                     ADMIN_ROLE_ID)

            self.idm.grantDomainRoleToGroup(DOMAIN_ADMIN_TOKEN,
                                     ID_DOM1,
                                     ID_SERVICE_CUSTOMER_GROUP,
                                     ID_NEW_SERVICE_ROLE_SERVICECUSTOMER)

            self.idm.grantInheritRoleToGroup(NEW_SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      ID_ADMIN_GROUP,
                                      ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN)

            self.idm.grantInheritRoleToGroup(NEW_SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      ID_SERVICE_CUSTOMER_GROUP,
                                      ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER)

            self.idm.grantInheritRoleToGroup(NEW_SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      ID_SUB_SERVICE_ADMIN_GROUP,
                                      ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN)

            self.idm.grantInheritRoleToGroup(NEW_SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      ID_SUB_SERVICE_CUSTOMER_GROUP,
                                      ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER)

        except Exception, ex:
            if ID_DOM1:
                self.logger.info("removing uncomplete created domain %s" % ID_DOM1)
                self.idm.disableDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
                self.idm.deleteDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ID_DOM1": "%s" % ID_DOM1,
            "NEW_SERVICE_ADMIN_TOKEN": "%s" % NEW_SERVICE_ADMIN_TOKEN,
            "ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN": "%s" % ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
            "ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER": "%s" % ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
            "ID_NEW_SERVICE_ROLE_SERVICECUSTOMER": "%s" % ID_NEW_SERVICE_ROLE_SERVICECUSTOMER
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {
            "token": NEW_SERVICE_ADMIN_TOKEN,
            "id": ID_DOM1,
        }, DOMAIN_NAME, None
