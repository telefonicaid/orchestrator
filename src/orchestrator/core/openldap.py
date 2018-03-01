#
# Copyright 2018 Telefonica España
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
import logging

from orchestrator.common.util import RestOperations
from orchestrator.core.ldap import LdapOperations

import ldap
import ldap.modlist as modlist

logger = logging.getLogger('orchestrator_core')

class OpenLdapOperations(LdapOperations):
    '''
       IoT platform: Open LDAP
    '''

    def __init__(self,
                 LDAP_PROTOCOL=None,
                 LDAP_HOST=None,
                 LDAP_PORT=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):

        self.LDAP_PROTOCOL = LDAP_PROTOCOL
        self.LDAP_HOST = LDAP_HOST
        self.LDAP_PORT = LDAP_PORT


    def checkLdap(self):
        None
        # TBD
        
    def bind_admin(self, USERNAME, PASSWORD):
        conn = ldap.open(self.LDAP_HOST, self.LDAP_PORT)
    
        # you should set this to ldap.VERSION2 if you're using a v2 directory
        conn.protocol_version = ldap.VERSION3  
        username = "cn=" + USERNAME + ", dc=openstack, dc=org"
    
        # Any errors will throw an ldap.LDAPError exception 
        # or related exception so you can ignore the result
        conn.bind_s(username, PASSWORD)
        return bind

    def bind_admin(self, USERNAME, PASSWORD):
        conn = ldap.open(self.LDAP_HOST, self.LDAP_PORT)
    
        # you should set this to ldap.VERSION2 if you're using a v2 directory
        conn.protocol_version = ldap.VERSION3  
        username = "uid=" + USERNAME + ", ou=Users, dc=openstack, dc=org"
    
        # Any errors will throw an ldap.LDAPError exception 
        # or related exception so you can ignore the result
        conn.simple_bind_s(username, PASSWORD)
        return bind

    def unbind(self, conn):
        conn.unbind_s()

    def createUser(self,
                   LDAP_ADMIN_USER,
                   LDAP_ADMIN_PASSWORD,
                   NEW_USER_NAME,
                   NEW_USER_PASSWORD,
                   NEW_USER_EMAIL,
                   NEW_USER_DESCRIPTION):
        try:
            conn = self.bind_admin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "uid=" + NEW_USER_NAME + ",ou=users,dc=openstack,dc=org"
            mymodlist = {
                "objectClass": ["account", "posixAccount", "shadowAccount"],
                "uid": [ NEW_USER_NAME ],
                "cn": [ NEW_USER_DESCRIPTION ],
                #"uidNumber": ["5000"],
                "gidNumber": ["10000"],
                "loginShell": ["/bin/bash"],
                "homeDirectory": ["/home/"+ NEW_USER_NAME],
                "userPassword": NEW_USER_PASSWORD
            }
            result = conn.add_s(dn, modlist.addModlist(mymodlist))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            return { "error": e }
            
    def deleteUserByAdmin(self,
                          LDAP_ADMIN_USER,
                          LDAP_ADMIN_PASSWORD,
                          USER_NAME):
        try:
            conn = self.bind_admin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "uid=" + USER_NAME + ",ou=users,dc=openstack,dc=org"
            result = conn.delete_s(dn)
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            return { "error": e }

    def deleteUserByHimself(self,
                            USER_NAME,
                            USER_PASSWORD):
        try:
            conn = self.bind_user(USER_NAME, USER_PASSWORD)
            dn = "uid=" + USER_NAME + ",ou=users,dc=openstack,dc=org"
            result = conn.delete_s(dn)            
            self.unbind(conn)
            return { "details": result }    
        except ldap.LDAPError, e:
            return { "error": e }

    def listUsers(self,
                  LDAP_ADMIN_USER,
                  LDAP_ADMIN_PASSWORD,
                  FILTER):
        try:
            conn = self.bind_admin(USER_NAME, USER_PASSWORD)

            baseDN = "ou=users, o=openstack.org"
            searchScope = ldap.SCOPE_SUBTREE
            ## retrieve all attributes
            retrieveAttributes = None 
            searchFilter = FILTER # "cn=*jack*"

            ldap_result_id = conn.search(baseDN, searchScope, searchFilter,
                                         retrieveAttributes)
            result_set = []
            while 1:
                result_type, result_data = conn.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    ## here you don't have to append to a list
                    ## you could do whatever you want with the individual entry
                    ## The appending to list is just for illustration. 
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            #print result_set
            self.unbind(conn)
            return { "details": result_set }
        except ldap.LDAPError, e:
            return { "error": e }

    def assignGroupUser(self,
                   LDAP_ADMIN_USER,
                   LDAP_ADMIN_PASSWORD,
                   USER_NAME,
                   GROUP_NAME):
        try:
            conn = self.bind_admin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "uid=" + USER_NAME + ",ou=users,dc=openstack,dc=org"

            # A dict to help build the "body" of the object
            attrs = {}
            attrs['member'] = [ 'cn=' + GROUP_NAME +',ou=users,dc=openstack,dc=org' ]

            # Do the actual synchronous add-operation to the ldapserver
            result = conn.add_s(dn, modlist.addModlist(attrs))
            self.unbind(conn)
            return { "details": result_set }
        except ldap.LDAPError, e:
            return { "error": e }
