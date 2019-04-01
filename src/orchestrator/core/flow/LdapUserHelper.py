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

    def composeErrorCodeLdap(self, ex):
        # get just first result of composeErrorCode, without service/subservice info
        return self.composeErrorCode(ex)[0]


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
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "NEW_USER_NAME": "%s" % NEW_USER_NAME,
            "NEW_USER_PASSWORD": "%s" % "***", #NEW_USER_PASSWORD,
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
                        raise Exception(400, "None group was asigned to user created in ldap: %s" % res['error'])
                self.logger.info("ldap user %s was created" % NEW_USER_NAME)
                return {}
            else:
                raise Exception(400, "None user was created in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR creating user %s: %s" % (
                NEW_USER_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def askForCreateNewUser(self,
                      NEW_USER_NAME,
                      NEW_USER_PASSWORD,
                      NEW_USER_EMAIL,
                      NEW_USER_DESCRIPTION,
                      GROUP_NAMES):
        data_log = {
            "NEW_USER_NAME": "%s" % NEW_USER_NAME,
            "NEW_USER_PASSWORD": "%s" % "***", #NEW_USER_PASSWORD,
            "NEW_USER_EMAIL": "%s" % NEW_USER_EMAIL,
            "NEW_USER_DESCRIPTION": "%s" % NEW_USER_DESCRIPTION,
            "GROUP_NAMES": "%s" % GROUP_NAMES
        }
        self.logger.debug("FLOW askForCreateNewUser invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            subject = "ask for a new user %s creation" % NEW_USER_NAME
            text = json.dumps(data_log)
            res = self.mailer.sendMail(None, subject=subject, text=text)
            if not "error" in res:
                self.logger.info("ldap user %s was asked to be created" % NEW_USER_NAME)
                return res
            else:
                raise Exception(400, "None user was asked to be created in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR asking for create user %s: %s" % (
                NEW_USER_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def deleteUser(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      USER_NAME,
                      USER_PASSWORD):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % "***", #USER_PASSWORD,
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
                self.logger.info("ldap user %s was deleted" % USER_NAME)
                return {}
            else:
                raise Exception(400, "None user deleted in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR deleting user %s: %s" % (
                USER_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def listUsers(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      FILTER):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
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
                return res
            else:
                raise Exception(404, "None users were retrieved from ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR retrieving users %s: %s" % (
                FILTER,
                ex))
            return self.composeErrorCodeLdap(ex)


    def getUserDetail(self,
                      USER_NAME,
                      USER_PASSWORD):
        data_log = {
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % "***", #USER_PASSWORD
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
                return res
            else:
                raise Exception(400, "None user detail was retrieved from ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR retrieving user detail %s: %s" % (
                USER_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def getUserDetailByAdmin(self,
                             LDAP_ADMIN_USER,
                             LDAP_ADMIN_PASSWORD,
                             USER_NAME):

        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "USER_NAME": "%s" % USER_NAME,
        }
        self.logger.debug("FLOW getUserDetailByAdmin invoked with: %s" % json.dumps(
            data_log,
            indent=3))

        try:
            groups = self.ldap.getUserGroups(
                             LDAP_ADMIN_USER,
                             LDAP_ADMIN_PASSWORD,
                             USER_NAME)
            self.logger.debug("groups=%s" % groups)

            user = self.ldap.listUsers(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    "*"+USER_NAME+"*")
            self.logger.debug("res=%s" % user)

            if not "error" in groups and not "error" in user:
                if (len(user['details']) > 0) and (len(user['details'][0]) > 1):
                    if 'uid' in user['details'][0][1]:
                        user['details'][0][1]['member'] = groups['details']
                return user
            else:
                raise Exception(400, "None user detail was retrieved from ldap: user %s groups %s" % (user, groups))
        except Exception, ex:
            self.logger.warn("ERROR retrieving user detail %s: %s" % (
                USER_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def authUser(self,
                    USER_NAME,
                    USER_PASSWORD):
        data_log = {
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % "***", #USER_PASSWORD
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
                return res
            else:
                raise Exception(401, "None user was auth by ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR authenticating user %s: %s" % (
                USER_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def updateUser(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      USER_NAME,
                      USER_PASSWORD,
                      USER_DATA):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "USER_NAME": "%s" % USER_NAME,
            "USER_PASSWORD": "%s" % "***", #USER_PASSWORD,
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
                if 'GROUPNAMES' in USER_DATA:
                    for GROUP_NAME in USER_DATA['GROUP_NAMES']:
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
                self.logger.info("ldap user %s was updated" % USER_NAME)
                return res
            else:
                raise Exception(400, "None user was updated in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR updating user %s: %s" % (
                USER_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)
