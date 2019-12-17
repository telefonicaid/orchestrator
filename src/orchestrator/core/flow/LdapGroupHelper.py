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

class LdapGroupHelper(FlowBase):

    def composeErrorCodeLdap(self, ex):
        # get just first result of composeErrorCode, without service/subservice info
        return self.composeErrorCode(ex)[0]


    def createNewGroup(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      NEW_GROUP_NAME,
                      NEW_GROUP_DESCRIPTION):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "NEW_GROUP_NAME": "%s" % NEW_GROUP_NAME,
            "NEW_GROUP_DESCRIPTION": "%s" % NEW_GROUP_DESCRIPTION,
        }
        self.logger.debug("FLOW createNewGroup invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            res = self.ldap.createGroup(
                   LDAP_ADMIN_USER,
                   LDAP_ADMIN_PASSWORD,
                   NEW_GROUP_NAME,
                   NEW_GROUP_DESCRIPTION)
            self.logger.debug("res=%s" % res)

            if not 'error' in res:
                self.logger.info("ldap group %s was created" % NEW_GROUP_NAME)
                return {}
            else:
                raise Exception(400, "None group was created in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR creating group %s: %s" % (
                NEW_GROUP_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def deleteGroup(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      GROUP_NAME):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "GROUP_NAME": "%s" % GROUP_NAME,
        }
        self.logger.debug("FLOW deleteGroup invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            if LDAP_ADMIN_USER and LDAP_ADMIN_PASSWORD:
                res = self.ldap.deleteGroupByAdmin(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    GROUP_NAME)
            self.logger.debug("res=%s" % res)
            if not "error" in res:
                self.logger.info("ldap group %s was deleted" % GROUP_NAME)
                return {}
            else:
                raise Exception(400, "None group deleted in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR deleting group %s: %s" % (
                GROUP_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def listGroups(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      FILTER):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "FILTER:": "%s" % FILTER
        }
        self.logger.debug("FLOW listGroups invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            res = self.ldap.listGroups(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    FILTER)
            self.logger.debug("res=%s" % res)

            if not "error" in res:
                return res
            else:
                raise Exception(404, "None groups were retrieved from ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR retrieving groups %s: %s" % (
                FILTER,
                ex))
            return self.composeErrorCodeLdap(ex)


    def getGroupDetailByAdmin(self,
                             LDAP_ADMIN_USER,
                             LDAP_ADMIN_PASSWORD,
                             GROUP_NAME):

        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "GROUP_NAME": "%s" % GROUP_NAME,
        }
        self.logger.debug("FLOW getGroupDetailByAdmin invoked with: %s" % json.dumps(
            data_log,
            indent=3))

        try:
            group = self.ldap.listGroups(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    "*"+GROUP_NAME+"*")
            self.logger.debug("res=%s" % group)

            if not "error" in group:
                return group
            else:
                raise Exception(400, "None group detail was retrieved from ldap: group %s" % (group))
        except Exception, ex:
            self.logger.warn("ERROR retrieving group detail %s: %s" % (
                GROUP_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)


    def updateGroup(self,
                      LDAP_ADMIN_USER,
                      LDAP_ADMIN_PASSWORD,
                      GROUP_NAME,
                      GROUP_DESCRIPTION):
        data_log = {
            "LDAP_ADMIN_USER": "%s" % LDAP_ADMIN_USER,
            "LDAP_ADMIN_PASSWORD": "%s" % "***", #LDAP_ADMIN_PASSWORD,
            "GROUP_NAME": "%s" % GROUP_NAME,
            "GROUP_DESCRIPTION:": "%s" % GROUP_DESCRIPTION
        }
        self.logger.debug("FLOW updateGroup invoked with: %s" % json.dumps(
            data_log,
            indent=3))
        try:
            if LDAP_ADMIN_USER and LDAP_ADMIN_PASSWORD:
                res = self.ldap.updateGroupByAdmin(
                    LDAP_ADMIN_USER,
                    LDAP_ADMIN_PASSWORD,
                    GROUP_NAME,
                    GROUP_DESCRIPTION)
            self.logger.debug("res=%s" % res)

            if not "error" in res:
                self.logger.info("ldap group %s was updated" % GROUP_NAME)
                return res
            else:
                raise Exception(400, "None group was updated in ldap: %s" % res['error'])
        except Exception, ex:
            self.logger.warn("ERROR updating group %s: %s" % (
                GROUP_NAME,
                ex))
            return self.composeErrorCodeLdap(ex)
