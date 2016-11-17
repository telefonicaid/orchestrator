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


class Groups(FlowBase):

    def groups(self,
              SERVICE_NAME,
              SERVICE_ID,
              SERVICE_ADMIN_USER,
              SERVICE_ADMIN_PASSWORD,
              SERVICE_ADMIN_TOKEN,
              START_INDEX=None,
              COUNT=None):

        '''Get groups.

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - START_INDEX: where pagination start
        - COUNT: number of results
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "START_INDEX": "%s" % START_INDEX,
            "COUNT": "%s" % COUNT,
        }
        self.logger.debug("FLOW groups invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            SERVICE_GROUPS = self.idm.getDomainGroups(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_ID,
                                                      START_INDEX,
                                                      COUNT)

            self.logger.debug("SERVICE_GROUPS=%s" % json.dumps(SERVICE_GROUPS,
                                                               indent=3))

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "SERVICE_GROUPS": SERVICE_GROUPS,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return SERVICE_GROUPS


    def group(self,
             SERVICE_ID,
             GROUP_ID,
             SERVICE_ADMIN_USER,
             SERVICE_ADMIN_PASSWORD,
             SERVICE_ADMIN_TOKEN):

        '''Get group detail

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_ID: Service ID
        - GROUP_ID: Group ID
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token

        '''
        data_log = {
            "SERVICE_ID": "%s" % SERVICE_ID,
            "GROUP_ID": "%s" % GROUP_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
        }
        self.logger.debug("FLOW group invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                    SERVICE_ID,
                    SERVICE_ADMIN_USER,
                    SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            DETAIL_GROUP = self.idm.detailUser(SERVICE_ADMIN_TOKEN,
                                               GROUP_ID)
            self.logger.debug("DETAIL_GROUP=%s" % json.dumps(DETAIL_GROUP, indent=3))

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "DETAIL_GROUP": DETAIL_GROUP,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))
        return DETAIL_GROUP


    def updateGroup(self,
                   SERVICE_NAME,
                   SERVICE_ID,
                   SERVICE_ADMIN_USER,
                   SERVICE_ADMIN_PASSWORD,
                   SERVICE_ADMIN_TOKEN,
                   GROUP_NAME,
                   GROUP_ID):

        '''Update an Group Service (aka domain group keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - GROUP_NAME: Group name
        - GROUP_ID: Group Id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "GROUP_NAME": "%s" % GROUP_NAME,
            "GROUP_ID": "%s" % GROUP_ID
        }
        self.logger.debug("FLOW updateGroup invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 2. Get group ID
            #
            if not GROUP_ID:
                GROUP_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                    SERVICE_ID,
                                                    GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (GROUP_NAME, GROUP_ID))

            #
            # 3. UpdateGroup
            #
            self.idm.updateGroup(SERVICE_ADMIN_TOKEN,
                                 GROUP_ID)

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "GROUP_ID": GROUP_ID,
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": GROUP_ID}


    def removeGroup(self,
                   SERVICE_NAME,
                   SERVICE_ID,
                   SERVICE_ADMIN_USER,
                   SERVICE_ADMIN_PASSWORD,
                   SERVICE_ADMIN_TOKEN,
                   GROUP_NAME,
                   GROUP_ID):

        '''Removes an group Service (aka domain group keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - GROUP_NAME: Group name
        - GROUP_ID: Group id
        '''
        data_log = {
            "SERVICE_NAME": "%s" % SERVICE_NAME,
            "SERVICE_ID": "%s" % SERVICE_ID,
            "SERVICE_ADMIN_USER": "%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD": "%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN": self.get_extended_token(SERVICE_ADMIN_TOKEN),
            "GROUP_NAME": "%s" % GROUP_NAME,
            "GROUP_ID": "%s" % GROUP_ID
        }
        self.logger.debug("FLOW remove group invoked with: %s" % json.dumps(
            data_log,
            indent=3)
        )
        try:
            if not SERVICE_ADMIN_TOKEN:
                if not SERVICE_ID:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken(
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
                    SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME)
                else:
                    SERVICE_ADMIN_TOKEN = self.idm.getToken2(
                        SERVICE_ID,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD)
            self.logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)

            #
            # 2. Get group ID
            #
            if not GROUP_ID:
                GROUP_ID = self.idm.getDomainGroupId(SERVICE_ADMIN_TOKEN,
                                                     SERVICE_ID,
                                                     GROUP_NAME)
            self.logger.debug("ID of group %s: %s" % (GROUP_NAME, GROUP_ID))

            #
            # 3. Remove group ID
            #
            self.idm.removeGroup(SERVICE_ADMIN_TOKEN,
                                 GROUP_ID)

        except Exception, ex:
            self.logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "GROUP_ID": GROUP_ID
        }
        self.logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {}
