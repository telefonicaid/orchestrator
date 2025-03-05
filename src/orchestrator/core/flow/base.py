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
import logging
import uuid
from functools import reduce

from orchestrator.core.keystone import IdMKeystoneOperations as IdMOperations
from orchestrator.core.keypass import AccCKeypassOperations as AccCOperations
from orchestrator.core.orion import CBOrionOperations as CBOperations
from orchestrator.core.perseo import PerseoOperations as PerseoOperations
from orchestrator.core.openldap import OpenLdapOperations as OpenLdapOperations
from orchestrator.core.mailer import MailerOperations as MailerOperations
from orchestrator.core.mongo import MongoDBOperations as MongoDBOperations
from orchestrator.common.util import ContextFilterCorrelatorId
from orchestrator.common.util import ContextFilterTransactionId
from orchestrator.common.util import ContextFilterService
from orchestrator.common.util import ContextFilterSubService
from orchestrator.common.util import ContextFilterFrom

from settings.dev import IOTMODULES
from settings import dev as settings

class FlowBase(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT,
                 KEYPASS_PROTOCOL=None,
                 KEYPASS_HOST=None,
                 KEYPASS_PORT=None,
                 ORION_PROTOCOL="http",
                 ORION_HOST="localhost",
                 ORION_PORT="1026",
                 PERSEO_PROTOCOL="http",
                 PERSEO_HOST="localhost",
                 PERSEO_PORT="9090",
                 LDAP_HOST="localhost",
                 LDAP_PORT="389",
                 LDAP_BASEDN="dc=openstack,dc=org",
                 MAILER_HOST="localhost",
                 MAILER_PORT="587",
                 MAILER_TLS="true",
                 MAILER_USER="smtpuser@yourdomain.com",
                 MAILER_PASSWORD="yourpassword",
                 MAILER_FROM="smtpuser",
                 MAILER_TO="smtpuser",
                 MONGODB_URI="mongodb://127.0.0.1:27017",
                 TRANSACTION_ID=None,
                 CORRELATOR_ID=None,
                 FROM=None):

        # Generate Transaction ID
        self.TRANSACTION_ID = str(uuid.uuid4())

        if not CORRELATOR_ID:
            self.CORRELATOR_ID = self.TRANSACTION_ID
        else:
            self.CORRELATOR_ID = CORRELATOR_ID

        self.FROM = FROM

        self.logger = logging.getLogger('orchestrator_core')

        # Put collector into logger
        self.logger.addFilter(ContextFilterCorrelatorId(self.CORRELATOR_ID))
        self.logger.addFilter(ContextFilterTransactionId(self.TRANSACTION_ID))
        self.logger.addFilter(ContextFilterService(None))
        self.logger.addFilter(ContextFilterSubService(""))
        self.logger.addFilter(ContextFilterFrom(self.FROM))

        self.idm = IdMOperations(KEYSTONE_PROTOCOL,
                                 KEYSTONE_HOST,
                                 KEYSTONE_PORT)

        self.ac = AccCOperations(KEYPASS_PROTOCOL,
                                 KEYPASS_HOST,
                                 KEYPASS_PORT,
                                 CORRELATOR_ID=self.CORRELATOR_ID,
                                 TRANSACTION_ID=self.TRANSACTION_ID)

        self.cb = CBOperations(ORION_PROTOCOL,
                               ORION_HOST,
                               ORION_PORT,
                               CORRELATOR_ID=self.CORRELATOR_ID,
                               TRANSACTION_ID=self.TRANSACTION_ID)

        self.perseo = PerseoOperations(PERSEO_PROTOCOL,
                                       PERSEO_HOST,
                                       PERSEO_PORT,
                                       CORRELATOR_ID=self.CORRELATOR_ID,
                                       TRANSACTION_ID=self.TRANSACTION_ID)

        self.ldap = OpenLdapOperations(LDAP_HOST,
                                       LDAP_PORT,
                                       LDAP_BASEDN,
                                       CORRELATOR_ID=self.CORRELATOR_ID,
                                       TRANSACTION_ID=self.TRANSACTION_ID)

        self.mailer = MailerOperations(MAILER_HOST,
                                       MAILER_PORT,
                                       MAILER_TLS,
                                       MAILER_USER,
                                       MAILER_PASSWORD,
                                       MAILER_FROM,
                                       MAILER_TO,
                                       CORRELATOR_ID=self.CORRELATOR_ID,
                                       TRANSACTION_ID=self.TRANSACTION_ID)

        self.mongodb = MongoDBOperations(MONGODB_URI,
                                         CORRELATOR_ID=self.CORRELATOR_ID,
                                         TRANSACTION_ID=self.TRANSACTION_ID)

        self.endpoints = {}
        self.iotmodules_aliases = {}

        self.sum = {
            "serviceTime": 0,
            "serviceTimeTotal": 0,
            "outgoingTransactions": 0,
            "outgoingTransactionRequestSize": 0,
            "outgoingTransactionResponseSize": 0,
            "outgoingTransactionErrors": 0,
        }


    def composeErrorCode(self, ex):
        '''
        Compose error detail and code from AssertionError exception ex
        '''
        # Get line where exception was produced
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        res = {"error": str(ex), "code": 500}
        try:
            if isinstance(ex.args, tuple) and (
                    (len(ex.args) > 0)):
                if not isinstance(ex.args[0], tuple):  # Python 2.6
                    res['code'] = ex.args[0]
                    if res['code'] == 400 and len(ex.args) > 1 and \
                       ex.args[1].startswith('SPASSWORD'):
                        res['error'] = ex.args[1]
                else: # Python 3
                    res['code'] = ex.args[0][0]
                    if res['code'] == 400 and len(ex.args[0]) > 1 and \
                       ex.args[0][1].startswith('SPASSWORD'):
                        res['error'] = ex.args[0][1]
            elif isinstance(ex.message, tuple):  # Python 2.7
                res['code'] = ex.message[0]
                if res['code'] == 400 and len(ex.message) > 1 and \
                   ex.message[1].startswith('SPASSWORD'):
                    res['error'] = ex.message[1]
        finally:
            return res, None, None


    def logError(self, logger, error_code, ex):
        '''
        Log as error level error_code if is < 400 or > 500
        '''
        try:
            if (isinstance(error_code[0]['code'], int) and
                (error_code[0]['code'] < 400 or error_code[0]['code'] >= 500)):
                self.logger.error(ex)
            else:
                self.logger.debug(ex)
        except:
            self.logger.debug(ex)

    def get_endpoint_iot_module(self, iot_module):
        assert iot_module in IOTMODULES
        if iot_module in self.endpoints:
            return self.endpoints[iot_module]
        else:
            comppackage = __import__("settings.dev", fromlist=iot_module)
            iot_module_conf = getattr(comppackage, iot_module)
            assert 'protocol' in iot_module_conf
            assert 'host' in iot_module_conf
            assert 'port' in iot_module_conf
            notifypath = "/notify" if not 'notifypath' in iot_module_conf else iot_module_conf['notifypath']
            iot_mddule_enpoint = iot_module_conf['protocol'] + "://" + \
              iot_module_conf['host'] + ":" + \
              iot_module_conf['port'] + notifypath
            self.endpoints[iot_module] = iot_mddule_enpoint
            return iot_mddule_enpoint


    def get_alias_iot_module(self, iot_module):
        assert iot_module in IOTMODULES
        if iot_module in self.iotmodules_aliases:
            return self.alias[iot_module]
        else:
            comppackage = __import__("settings.dev", fromlist=iot_module)
            iot_module_conf = getattr(comppackage, iot_module)
            alias = iot_module
            if 'alias' in iot_module_conf:
                alias = iot_module_conf['alias']
                self.iotmodules_aliases[iot_module] = alias
            return alias


    def ensure_service_name(self, USER_TOKEN, SERVICE_ID, SERVICE_NAME):
        if not SERVICE_NAME:
            self.logger.debug("Not SERVICE_NAME provided, getting it from token")
            try:
                SERVICE_NAME = self.idm.getDomainNameFromToken(
                    USER_TOKEN,
                    SERVICE_ID)
            except Exception as ex:
                # This op could be executed by cloud_admin user
                SERVICE = self.idm.getDomain(USER_TOKEN,
                                             SERVICE_ID)
                SERVICE_NAME = SERVICE['domain']['name']
        return SERVICE_NAME


    def ensure_subservice_name(self, USER_TOKEN, SERVICE_ID, SUBSERVICE_ID,
                               SUBSERVICE_NAME):
        if not SUBSERVICE_NAME:
            self.logger.debug("Not SUBSERVICE_NAME provided, getting it from token")
            try:
                SUBSERVICE_NAME = self.idm.getProjectNameFromToken(
                     USER_TOKEN,
                     SERVICE_ID,
                     SUBSERVICE_ID)
            except Exception as ex:
                # This op could be executed by cloud_admin user
                SUBSERVICE = self.idm.getProject(USER_TOKEN,
                                                 SUBSERVICE_ID)
                SUBSERVICE_NAME = SUBSERVICE['project']['name'][1:]
        return SUBSERVICE_NAME


    def get_extended_token(self, USER_TOKEN):
        token_extended = {
            "token": USER_TOKEN
        }
        if USER_TOKEN:
            try:
                token_detail = self.idm.getTokenDetail(USER_TOKEN)
                token_extended["user"] = token_detail['token']['user']['name']

                # Include service scope if available
                if 'domain' in token_detail['token']['user']:
                    token_extended['domain'] = \
                        token_detail['token']['user']['domain']['name']

                # Include subservice scope if available
                if 'project' in token_detail['token']:
                    token_extended['project'] = \
                        token_detail['token']['project']['name'][1:]

            except Exception as ex:
                # Probably expired?
                token_extended["error"] = str(ex)

        return token_extended

    def collectComponentMetrics(self):
        all = []
        if not settings.ORC_EXTENDED_METRICS:
            # Do nothing
            return
        try:
            all.append(self.idm.IdMRestOperations.getOutgoingMetrics())
            all.append(self.ac.AccessControlRestOperations.getOutgoingMetrics())
            all.append(self.cb.CBRestOperations.getOutgoingMetrics())
            all.append(self.perseo.PerseoRestOperations.getOutgoingMetrics())
            # TODO: Take care of the following operation takes too much time
            self.sum = reduce(lambda x, y: {k: v + y[k] for k, v in x.items()}, all)
        except Exception as ex:
            self.logger.error("ERROR collecting component metrics: %s", ex)

    def getFlowMetrics(self):
        return self.sum
