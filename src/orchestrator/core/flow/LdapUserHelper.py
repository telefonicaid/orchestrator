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

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')

class LdapUserHelper(FlowBase):

    def createNewUser(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      NEW_USER_NAME,
                      NEW_USER_PASSWORD,
                      NEW_USER_EMAIL,
                      NEW_USER_DESCRIPTION,
                      GROUP_NAMES):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % LDAP_ADMIN_PASSWORD,
            "NEW_USER_NAME": "%s" % NEW_USER_NAME,
            "NEW_USER_PASSWORD": "%s" % NEW_USER_PASSWORD,
            "NEW_USER_EMAIL": "%s" % NEW_USER_EMAIL,
            "NEW_USER_DESCRIPTION": "%s" % NEW_USER_DESCRIPTION,
            "GROUP_NAMES": "%s" % GROUP_NAMES
        }
        self.logger.debug("FLOW createNewUser invoked with: %s" % json.dumps(
            data_log,
            indent=3))

        try:
            res = self.ldap.createUser(
                   LDAP_ADMIN_USER,
                   LDAP_ADMIN_PASSWORD,
                   NEW_USER_NAME,
                   NEW_USER_PASSWORD,
                   NEW_USER_EMAIL,
                   NEW_USER_DESCRIPTION)
            self.logger.debug("res=%s" % res)

            if not 'error' in res:
                for GROUP_NAME in GROUP_NAMES:
                    self.logger.debug("FLOW createNewUser assing to group: %s" % GROUP_NAME)
                    res = self.ldap.assignGroupUser(
                        LDAP_ADMIN_USER,
                        LDAP_ADMIN_PASSWORD,
                        NEW_USER_NAME,
                        GROUP_NAME)
                    self.logger.debug("res=%s" % res)

                    if 'error' in res:
                        self.logger.warn("FLOW createNewUser removing user: %s" % NEW_USER_NAME)
                        self.ldap.deleteUserByAdmin(
                                              LDAP_ADMIN_USER,
                                              LDAP_ADMIN_PASSWORD,
                                              NEW_USER_NAME)
                        raise Exception("not group was asigned to user created in ldap: %s" % res['error'])
                return {}, None, None
            else:
                raise Exception("not user was created in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR creating user %s: %s" % (
                NEW_USER_NAME,
                ex))
            # Delete user if was created
            return self.composeErrorCode(ex)


    def deleteUser(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      USER_NAME,
                      USER_PASSWORD):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % LDAP_ADMIN_PASSWORD,
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % USER_PASSWORD,
        }
        self.logger.debug("FLOW deleteUser invoked with: %s" % json.dumps(
            data_log,
            indent=3))

        try:
            if LDAP_ADMIN_USER and LDAP_ADMIN_PASSWORD:
                res = self.ldap.deleteUserByAdmin(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    USER_NAME)
            elif USER_NAME and USER_PASSWORD:
                res = self.ldap.deleteUserByHimself(
                    USER_NAME,
                    USER_PASSWORD)
            self.logger.debug("res=%s" % res)

            if not "error" in res:
                return {}, None, None
            else:
                raise Exception("not user deleted in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR deleting user %s: %s" % (
                USER_NAME,
                ex))
            # Delete user if was created
            return self.composeErrorCode(ex)


    def listUsers(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      FILTER):

        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % LDAP_ADMIN_PASSWORD,
            "FILTER:": "%s" % FILTER
        }
        self.logger.debug("FLOW listUsers invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            res = self.ldap.listUsers(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    FILTER)
            self.logger.debug("res=%s" % res)

            if not "error" in res:
                return res, None, None
            else:
                raise Exception("not users were retrieved from ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR retrieving users %s: %s" % (
                FILTER,
                ex))
            # Delete user if was created
            return self.composeErrorCode(ex)


    def getUserDetail(self,
                      USER_NAME,
                      USER_PASSWORD):

        data_log = {
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % USER_PASSWORD
        }
        self.logger.debug("FLOW getUserDetail invoked with: %s" % json.dumps(
            data_log,
            indent=3))

        try:
            res = self.ldap.getUserDetail(
                    USER_NAME,
                    USER_PASSWORD)
            self.logger.debug("res=%s" % res)

            if not "error" in res:
                return res, None, None
            else:
                raise Exception("not user detail was retrieved from ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR retrieving user detail %s: %s" % (
                USER_NAME,
                ex))
            # Delete user if was created
            return self.composeErrorCode(ex)


    def getUserAuth(self,
                    USER_NAME,
                    USER_PASSWORD):

        data_log = {
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % USER_PASSWORD
        }
        self.logger.debug("FLOW getUserAuth invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            res = self.ldap.authUser(
                    USER_NAME,
                    USER_PASSWORD)
            self.logger.debug("res=%s" % res)

            if not "error" in res:
                return res, None, None
            else:
                raise Exception("not user was auth by ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR autenticating user%s: %s" % (
                USER_NAME,
                ex))
            # Delete user if was created
            return self.composeErrorCode(ex)                

    def updateUser(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      USER_NAME,
                      USER_PASSWORD,
                      USER_DATA):

        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % LDAP_ADMIN_PASSWORD,
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % USER_PASSWORD,
            "USER_DATA:": "%s" % USER_DATA
        }
        self.logger.debug("FLOW updateUser invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            if LDAP_ADMIN_USER and LDAP_ADMIN_PASSWORD:
                res = self.ldap.updateUserByAdmin(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    USER_NAME,
                    USER_DATA)

                if GROUPNAMES in USER_DATA:
                    for GROUP_NAME in GROUP_NAMES:
                        self.logger.debug("FLOW updateUser assign to group: %s" % GROUP_NAME)
                        res = self.ldap.assignGroupUser(
                            LDAP_ADMIN_USER,
                            LDAP_ADMIN_PASSWORD,
                            NEW_USER_NAME,
                            GROUP_NAME)
                        self.logger.debug("res=%s" % res)
            elif USERNAME and USER_PASSWORD:
                res = self.ldap.updateUserByHimself(
                    USER_NAME,
                    USER_PASSWORD,
                    USER_DATA)
            self.logger.debug("res=%s" % res)

            if not "error" in res:
                return res, None, None
            else:
                raise Exception("not user was updated in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR updating user %s: %s" % (
                USER_NAME,
                ex))
            # Delete user if was created
            return self.composeErrorCode(ex)
