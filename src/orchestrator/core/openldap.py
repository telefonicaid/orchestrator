#
# Copyright 2018 Telefonica Espana
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

import ldap
import ldap.modlist as modlist

logger = logging.getLogger('orchestrator_core')

class OpenLdapOperations(object):
    '''
       IoT platform: Open LDAP
    '''

    def __init__(self,
                 LDAP_HOST=None,
                 LDAP_PORT=None,
                 LDAP_BASEDN=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):
        self.LDAP_HOST = LDAP_HOST
        self.LDAP_PORT = int(LDAP_PORT)
        self.LDAP_BASEDN = LDAP_BASEDN

    def checkLdap(self):
        conn = ldap.open(self.LDAP_HOST, self.LDAP_PORT)
        assert conn != None

    def bindAdmin(self, USERNAME, PASSWORD):
        conn = ldap.open(self.LDAP_HOST, self.LDAP_PORT)
        # you should set this to ldap.VERSION2 if you're using a v2 directory
        conn.protocol_version = ldap.VERSION3  
        username = "cn=" + USERNAME + "," + self.LDAP_BASEDN
        logger.debug("bind admin %s" % username)

        # Any errors will throw an ldap.LDAPError exception 
        # or related exception so you can ignore the result
        conn.bind_s(username, PASSWORD)
        return conn

    def bindUser(self, USERNAME, PASSWORD):
        conn = ldap.open(self.LDAP_HOST, self.LDAP_PORT)
    
        # you should set this to ldap.VERSION2 if you're using a v2 directory
        conn.protocol_version = ldap.VERSION3  
        username = "uid=" + USERNAME + ", ou=users," + self.LDAP_BASEDN
        logger.debug("bind user %s" % username)

        # Any errors will throw an ldap.LDAPError exception 
        # or related exception so you can ignore the result
        conn.simple_bind_s(username, PASSWORD)
        return conn

    def unbind(self, conn):
        logger.debug("unbind")
        conn.unbind_s()

    def createUser(self,
                   LDAP_ADMIN_USER,
                   LDAP_ADMIN_PASSWORD,
                   NEW_USER_NAME,
                   NEW_USER_PASSWORD,
                   NEW_USER_EMAIL,
                   NEW_USER_DESCRIPTION):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "uid=" + NEW_USER_NAME + ",ou=users," + self.LDAP_BASEDN
            mymodlist = {
                "objectClass": ["account", "posixAccount", "shadowAccount"],
                "uid": [ str(NEW_USER_NAME) ],
                "cn": [ str(NEW_USER_DESCRIPTION) ],
                "uidNumber": ["5000"],
                "gidNumber": ["10000"],
                "loginShell": ["/bin/bash"],
                "homeDirectory": ["/home/"+ str(NEW_USER_NAME)],
                "mail": str(NEW_USER_EMAIL),
                "userPassword": str(NEW_USER_PASSWORD)
            }
            logger.debug("create user mymodlist: %s" % mymodlist)
            result = conn.add_s(dn, ldap.modlist.addModlist(mymodlist))
            logger.debug("ldap create user %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def deleteUserByAdmin(self,
                          LDAP_ADMIN_USER,
                          LDAP_ADMIN_PASSWORD,
                          USER_NAME):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "uid=" + USER_NAME + ",ou=users," + self.LDAP_BASEDN
            result = conn.delete_s(dn)
            logger.debug("ldap delete user by admin %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def deleteUserByHimself(self,
                            USER_NAME,
                            USER_PASSWORD):
        try:
            conn = self.bindUser(USER_NAME, USER_PASSWORD)
            dn = "uid=" + USER_NAME + ",ou=users," + self.LDAP_BASEDN
            result = conn.delete_s(dn)
            logger.debug("ldap delete user by himself %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def authUser(self,
                 USER_NAME,
                 USER_PASSWORD):
        try:
            conn = self.bindUser(USER_NAME, USER_PASSWORD)
            self.unbind(conn)
            return { "details": "OK" }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def listUsers(self,
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    FILTER):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)

            baseDN = "ou=users," + self.LDAP_BASEDN
            searchScope = ldap.SCOPE_SUBTREE
            ## retrieve all attributes
            retrieveAttributes = None
            searchFilter = "cn=" + FILTER # "cn=*jack*"
            ldap_result_id = conn.search(baseDN, searchScope, searchFilter,
                                         retrieveAttributes)
            logger.debug("ldap list users %s" % json.dumps(ldap_result_id))
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
            logger.debug("ldap number of users found %s" % len(result_set))
            self.unbind(conn)
            return { "details": result_set }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def assignGroupUser(self,
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    USER_NAME,
                    GROUP_NAME):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "cn=" + str(GROUP_NAME) + ",ou=groups," + self.LDAP_BASEDN
            results = conn.search_s(dn, ldap.SCOPE_BASE)

            # Get current group members
            groupMembers = []
            oldgroupMembers = []
            for result in results:
                result_dn = result[0]
                result_attrs = result[1]
                if "member" in result_attrs:
                    for member in result_attrs["member"]:
                        groupMembers.append(member)
                        oldgroupMembers.append(member)

            old_value = dict()
            new_value = dict()
            old_value['member'] = oldgroupMembers
            new_value['member'] = groupMembers
            # Add new group member
            new_value['member'].append('uid=' + str(USER_NAME) +',ou=users,' + self.LDAP_BASEDN)

            mymodlist = ldap.modlist.modifyModlist(old_value, new_value)

            result = conn.modify_s(dn, mymodlist)
            logger.debug("ldap assing group user %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def getUserDetail(self,
                    USER_NAME,
                    USER_PASSWORD):
        try:
            conn = self.bindUser(USER_NAME, USER_PASSWORD)
            baseDN = "uid=" + USER_NAME + ",ou=users," + self.LDAP_BASEDN
            searchScope = ldap.SCOPE_SUBTREE
            ## retrieve all attributes
            retrieveAttributes = None
            searchFilter = "cn=*" + USER_NAME + "*"

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
            logger.debug("ldap get user detail %s" % json.dumps(result_set))
            self.unbind(conn)
            return { "details": result_set }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def updateUserByAdmin(self,
                          LDAP_ADMIN_USER,
                          LDAP_ADMIN_PASSWORD,
                          USER_NAME,
                          USER_DATA):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "uid=" + USER_NAME + ",ou=users," + self.LDAP_BASEDN
            old_value = {}
            new_value = {}
            results = conn.search_s(dn, ldap.SCOPE_BASE)
            for result in results:
                result_dn = result[0]
                result_attrs = result[1]
                for attr in result_attrs:
                    for userattr in USER_DATA:
                        if attr == userattr:
                            old_value[attr] = result_attrs[userattr]
                            new_value[attr] = USER_DATA[userattr]

            mymodlist = ldap.modlist.modifyModlist(old_value, new_value)
            result = conn.modify_s(dn, mymodlist)
            logger.debug("ldap update user by admin %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }

    def updateUserByUser(self,
                          USER_NAME,
                          USER_PASSWORD,
                          USER_DETAIL):
        try:
            conn = self.bindUser(USER_NAME, USER_PASSWORD)
            dn = "uid=" + USER_NAME + ",ou=users," + self.LDAP_BASEDN
            old_value = {}
            new_value = {}
            results = conn.search_s(dn, ldap.SCOPE_BASE)
            for result in results:
                result_dn = result[0]
                result_attrs = result[1]
                for attr in result_attrs:
                    for userattr in USER_DATA:
                        if attr == userattr:
                            old_value[attr] = result_attrs[userattr]
                            new_value[attr] = USER_DATA[userattr]

            mymodlist = ldap.modlist.modifyModlist(old_value, new_value)
            result = conn.modify_s(dn, mymodlist)
            logger.debug("ldap update user by user %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError, e:
            logger.warn("exception: %s" % e)
            return { "error": e }
