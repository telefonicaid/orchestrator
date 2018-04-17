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
        try:
            client.list_databases()
            return True
        except Exception, e:
            logger.warn("checkMongo exception: %s" % e)
            return False

    def createIndexes(self, SERVICE_NAME):
        try:        
            databaseName = 'orion-' + SERVICE_NAME
            db = self.client[databaseName]
            db.entities.create_index("_id.id")
            db.entities.create_index("_id.type")
            db.entities.create_index("_id.servicePath")
            db.entities.create_index("_id.creDate")
        except Exception, e:
            logger.warn("createIndex exception: %s" % e)

    def removeDatabase(self, SERVICE_NAME):
        try:        
            databaseName = 'orion-' + SERVICE_NAME
            self.client.drop_database(databaseName)
        except Exception, e:
            logger.warn("createIndex exception: %s" % e)            
        
