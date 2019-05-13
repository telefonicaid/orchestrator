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

import pymongo

logger = logging.getLogger('orchestrator_core')

class MongoDBOperations(object):
    '''
       IoT platform: MongoDB
    '''

    def __init__(self,
                 MONGODB_URI=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):
        self.MONGODB_URI = MONGODB_URI
        self.client = pymongo.MongoClient(self.MONGODB_URI)

    def checkMongo(self):
        self.client.list_databases()

    def createOrionIndexes(self, SERVICE_NAME):
        # Creating recommended indexes to improve performance, as described in Orion Administration Manual
        # at https://fiware-orion.readthedocs.io/en/master/admin/perf_tuning/index.html
        try:
            # For Orion
            databaseName = 'orion-' + SERVICE_NAME
            db = self.client[databaseName]
            db.entities.create_index("_id.id")
            db.entities.create_index("_id.type")
            db.entities.create_index("_id.servicePath")
            db.entities.create_index("_id.creDate")
        except Exception, e:
            logger.warn("createIndex database %s exception: %s" % (databaseName,e))


    def createSTHIndexes(self, SERVICE_NAME, SUBSERVICE_NAME):
        try:
            # For STH
            databaseName = 'sth_' + SERVICE_NAME
            db = self.client[databaseName]
            collectionName = 'sth_/' + SUBSERVICE_NAME
            db[collectionName].create_index("_id.entityId")
            db[collectionName].create_index("_id.attrName")
            db[collectionName].create_index("_id.resolution")
            db[collectionName].create_index("_id.origin")
        except Exception, e:
            logger.warn("createIndex database %s exception: %s" % (databaseName,e))

    def removeDatabases(self, SERVICE_NAME):
        try:
            databaseName = 'orion-' + SERVICE_NAME
            self.client.drop_database(databaseName)
            databaseName = 'sth_' + SERVICE_NAME
            self.client.drop_database(databaseName)
        except Exception, e:
            logger.warn("remove database %s exception: %s" % (databaseName,e))
