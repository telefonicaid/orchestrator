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
        self.LDAP_PORT = int(LDAP_PORT) if LDAP_PORT else 0
        self.LDAP_BASEDN = LDAP_BASEDN

    def checkLdap(self):
        conn = ldap.initialize('ldap://'+str(self.LDAP_HOST)+':'+str(self.LDAP_PORT))
        # Just for check connection
        conn.simple_bind_s("","")

    def bindAdmin(self, USERNAME, PASSWORD):
        conn = ldap.initialize('ldap://'+str(self.LDAP_HOST)+':'+str(self.LDAP_PORT))
        conn.protocol_version = ldap.VERSION3  
        username = "cn=" + USERNAME + "," + self.LDAP_BASEDN
        logger.debug("bind admin %s" % username)
        conn.bind_s(username, PASSWORD)
        return conn

    def bindUser(self, USERNAME, PASSWORD):
        conn = ldap.initialize('ldap://'+str(self.LDAP_HOST)+':'+str(self.LDAP_PORT))
        conn.protocol_version = ldap.VERSION3  
        username = "uid=" + USERNAME + ", ou=users," + self.LDAP_BASEDN
        logger.debug("bind user %s" % username)
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
                "objectClass": [ b"top",
                                 b"posixAccount",
                                 b"shadowAccount",
                                 b"organizationalPerson",
                                 b"inetOrgPerson"],
                "uid": [ NEW_USER_NAME.encode('utf-8') ],
                "cn": [ NEW_USER_NAME.encode('utf-8') ],
                "uidNumber": [b"5000"],
                "gidNumber": [b"10000"],
                "loginShell": [b"/bin/bash"],
                "homeDirectory": [("/home/" + NEW_USER_NAME).encode('utf-8')],
                "mail": NEW_USER_EMAIL.encode('utf-8'),
                "sn": NEW_USER_NAME.encode('utf-8'),
                "userPassword": NEW_USER_PASSWORD.encode('utf-8')
            }
            logger.debug("create user mymodlist: %s" % mymodlist)
            result = conn.add_s(dn, ldap.modlist.addModlist(mymodlist))
            logger.debug("ldap create user %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError as e:
            logger.warn("createUser exception: %s" % e)
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
        except ldap.LDAPError as e:
            logger.warn("deleteUserByAdmin exception: %s" % e)
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
        except ldap.LDAPError as e:
            logger.warn("deleteUserByHimself exception: %s" % e)
            return { "error": e }

    def authUser(self,
                 USER_NAME,
                 USER_PASSWORD):
        try:
            conn = self.bindUser(USER_NAME, USER_PASSWORD)
            self.unbind(conn)
            return { "details": "OK" }
        except ldap.LDAPError as e:
            logger.warn("authUser exception: %s" % e)
            return { "error": e }

    def listUsers(self,
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    FILTER):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            baseDN = "ou=users," + self.LDAP_BASEDN
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = ['uid','sn','mail','cn']
            searchFilter = "uid=" + FILTER
            ldap_result_id = conn.search(baseDN, searchScope, searchFilter,
                                         retrieveAttributes)
            logger.debug("ldap list users %s" % json.dumps(ldap_result_id))
            result_set = []
            while 1:
                result_type, result_data = conn.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data[0])
            logger.debug("ldap number of users found %s" % len(result_set))
            self.unbind(conn)
            res = {}
            if result_set != []:
                res = { "details": result_set }
            else:
                res = { "error": FILTER + " not found" }
            return res
        except ldap.LDAPError as e:
            logger.warn("listUsers exception: %s" % e)
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
            new_value['member'].append(str('uid=' + str(USER_NAME) +',ou=users,' + self.LDAP_BASEDN).encode('utf-8'))
            mymodlist = ldap.modlist.modifyModlist(old_value, new_value)
            result = conn.modify_s(dn, mymodlist)
            logger.debug("ldap assing group user %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError as e:
            logger.warn("assignGroupUser exception: %s" % e)
            return { "error": e }

    def getUserGroups(self,
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    USER_NAME):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            baseDN = self.LDAP_BASEDN
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = ['cn']
            searchFilter='(|(&(objectClass=*)(member=uid=%s,ou=users,%s)))' % (
                USER_NAME, self.LDAP_BASEDN)
            results = conn.search_s(baseDN, ldap.SCOPE_SUBTREE,
                                    searchFilter, retrieveAttributes)
            groups = []
            for result in results:
                result_dn = result[0]
                result_attrs = result[1]
                if ('cn' in result_attrs and len(result_attrs['cn']) > 0):
                    groups.append(result_attrs['cn'][0].decode('utf-8'))

            logger.debug("ldap groups of user: %s" % json.dumps(groups))
            self.unbind(conn)
            return { "details": groups }
        except ldap.LDAPError as e:
            logger.warn("getUserGroups exception: %s" % e)
            return { "error": e }

    def getUserDetail(self,
                    USER_NAME,
                    USER_PASSWORD):
        try:
            conn = self.bindUser(USER_NAME, USER_PASSWORD)
            baseDN = "uid=" + USER_NAME + ",ou=users," + self.LDAP_BASEDN
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = ['uid','sn','mail','cn']
            searchFilter = "uid=" + USER_NAME
            ldap_result_id = conn.search(baseDN, searchScope, searchFilter,
                                         retrieveAttributes)
            result = None
            while 1:
                result_type, result_data = conn.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result = result_data[0]
            details = {key:[v.decode('utf-8') for v in values] for key, values in result[1].items()}
            logger.debug("ldap get user detail %s" % json.dumps(details))
            self.unbind(conn)
            return { "details": details }
        except ldap.LDAPError as e:
            logger.warn("getUserDetail exception: %s" % e)
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
            logger.debug("ldap update user by admin %s" % json.dumps(result[0]))
            self.unbind(conn)
            return { "details": result[0] }
        except ldap.LDAPError as e:
            logger.warn("updateUserByAdmin exception: %s" % e)
            return { "error": e }

    def updateUserByHimself(self,
                          USER_NAME,
                          USER_PASSWORD,
                          USER_DATA):
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
            logger.debug("ldap update user by user %s" % json.dumps(result[0]))
            self.unbind(conn)
            return { "details": result[0] }
        except ldap.LDAPError as e:
            logger.warn("updateUserByUser exception: %s" % e)
            return { "error": e }

    def createGroup(self,
                   LDAP_ADMIN_USER,
                   LDAP_ADMIN_PASSWORD,
                   NEW_GROUP_NAME,
                   NEW_GROUP_DESCRIPTION):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "cn=" + NEW_GROUP_NAME + ",ou=groups," + self.LDAP_BASEDN
            mymodlist = {
                "objectClass": [b"top",
                                b"groupofnames"],
                "cn": [ str(NEW_GROUP_NAME).encode('utf-8') ],
                'member' : [ b'ou=groups,dc=openstack,dc=org' ],
                "description": str(NEW_GROUP_DESCRIPTION).encode('utf-8')
            }
            logger.debug("create group mymodlist: %s" % mymodlist)
            result = conn.add_s(dn, ldap.modlist.addModlist(mymodlist))
            logger.debug("ldap create group %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError as e:
            logger.warn("createGroup exception: %s" % e)
            return { "error": e }

    def deleteGroupByAdmin(self,
                          LDAP_ADMIN_USER,
                          LDAP_ADMIN_PASSWORD,
                          GROUP_NAME):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "cn=" + GROUP_NAME + ",ou=groups," + self.LDAP_BASEDN
            result = conn.delete_s(dn)
            logger.debug("ldap delete group by admin %s" % json.dumps(result))
            self.unbind(conn)
            return { "details": result }
        except ldap.LDAPError as e:
            logger.warn("deleteGroupByAdmin exception: %s" % e)
            return { "error": e }

    def updateGroupByAdmin(self,
                          LDAP_ADMIN_USER,
                          LDAP_ADMIN_PASSWORD,
                          GROUP_NAME,
                          GROUP_DESCRIPTION):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            dn = "cn=" + GROUP_NAME + ",ou=groups," + self.LDAP_BASEDN
            old_value = {}
            new_value = {}
            results = conn.search_s(dn, ldap.SCOPE_BASE)
            logger.debug("ldap update group search results %s" % results)
            for result in results:
                result_dn = result[0]
                result_attrs = result[1]
                for attr in result_attrs:
                    for userattr in ['description']:
                        if attr == userattr:
                            old_value[attr] = result_attrs[userattr]
                            new_value[attr] = [str(GROUP_DESCRIPTION).encode('utf-8')]
            logger.debug("ldap update group old_value %s new_value %s " % (old_value, new_value))
            mymodlist = ldap.modlist.modifyModlist(old_value, new_value)
            result = conn.modify_s(dn, mymodlist)
            logger.debug("ldap update group by admin %s" % json.dumps(result[0]))
            self.unbind(conn)
            return { "details": result[0] }
        except ldap.LDAPError as e:
            logger.warn("updateGroupByAdmin exception: %s" % e)
            return { "error": e }

    def listGroups(self,
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    FILTER):
        try:
            conn = self.bindAdmin(LDAP_ADMIN_USER, LDAP_ADMIN_PASSWORD)
            baseDN = "ou=groups," + self.LDAP_BASEDN
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = ['description','cn']
            searchFilter = "cn=" + FILTER
            ldap_result_id = conn.search(baseDN, searchScope, searchFilter,
                                         retrieveAttributes)
            logger.debug("ldap list groups %s" % json.dumps(ldap_result_id))
            result_set = []
            while 1:
                result_type, result_data = conn.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data[0])
            logger.debug("ldap number of groups found %s" % len(result_set))
            self.unbind(conn)
            res = {}
            if result_set != []:
                res = { "details": result_set }
            else:
                res = { "error": FILTER + " not found" }
            return res
        except ldap.LDAPError as e:
            logger.warn("listGroups exception: %s" % e)
            return { "error": e }
