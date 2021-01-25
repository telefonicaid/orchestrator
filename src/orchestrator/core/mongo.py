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
            db.entities.create_index([("location.coords", pymongo.GEOSPHERE)])
            db.entities.create_index("expDate", expireAfterSeconds=0)
            db.entities.create_index([("_id.servicePath", pymongo.ASCENDING),
                                      ("_id.id", pymongo.ASCENDING),
                                      ("_id.type", pymongo.ASCENDING)])
            db.entities.create_index("creDate")
        except Exception, e:
            logger.warn("createIndex database %s exception: %s" % (databaseName,e))


    def createSTHIndexes(self, SERVICE_NAME, SUBSERVICE_NAME):
        try:
            # For STH, as described in https://github.com/telefonicaid/fiware-sth-comet/blob/master/doc/manuals/db_indexes.md
            databaseName = 'sth_' + SERVICE_NAME
            db = self.client[databaseName]
            collectionName = 'sth_/' + SUBSERVICE_NAME + '.aggr'
            db[collectionName].create_index([("_id.entityId", pymongo.ASCENDING),
                                             ("_id.entityType", pymongo.ASCENDING),
                                             ("_id.attrName", pymongo.ASCENDING),
                                             ("_id.resolution", pymongo.ASCENDING),
                                             ("_id.origin", pymongo.ASCENDING)])
            collectionName = 'sth_/' + SUBSERVICE_NAME
            db[collectionName].create_index([("entityId", pymongo.ASCENDING),
                                             ("entityType", pymongo.ASCENDING),
                                             ("attrName", pymongo.ASCENDING),
                                             ("recvTime", pymongo.ASCENDING)])
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
