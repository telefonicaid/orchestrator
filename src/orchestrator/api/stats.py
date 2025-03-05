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
import time
import threading
import multiprocessing

from django.conf import settings
from datetime import datetime


manager = multiprocessing.Manager()

def singleton(cls):
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Stats():

    def __init__(self):

        self.data = settings.SHARED_DATA
        self.lock = settings.SHARED_LOCK

        with self.lock:
            if 'initialized' not in self.data:
                self.data["uptime"] = str(datetime.utcnow())
                self.data["service"] = manager.dict({})
                data_sum = json.loads('''{ "sum": {
                    "incomingTransactions": 0,
                    "incomingTransactionRequestSize": 0,
                    "incomingTransactionResponseSize": 0,
                    "incomingTransactionErrors": 0,
                    "serviceTime": 0,
                    "serviceTimeTotal": 0,
                    "outgoingTransactions": 0,
                    "outgoingTransactionRequestSize": 0,
                    "outgoingTransactionResponseSize": 0,
                    "outgoingTransactionErrors": 0
                } }''')
                self.data["sum"] = manager.dict(data_sum["sum"])
                self.data['initialized'] = True

    def add_statistic(self, key, value):
        with self.lock:
            if key in self.data:
                self.data[key] += value
            else:
                self.data[key] = value

    def add_statistic_service(self, service_name, key, value):
        self.data["service"][service_name]["sum"][key] += value

    def add_statistic_subservice(self, service_name, subservice_name, key, value):
        self.data["service"][service_name]["subservs"][subservice_name][key] += value

    def add_statistic_sum(self, key, value):
        self.data["sum"][key] += value

    def init_statistic_service(self, service_name):
        self.data["service"][service_name] = manager.dict({})
        self.data["service"][service_name]["sum"] = manager.dict({})
        self.data["service"][service_name]["subservs"] = manager.dict({})
        data_service = json.loads('''{
                "sum": {
                   "incomingTransactions": 0,
                   "incomingTransactionRequestSize": 0,
                   "incomingTransactionResponseSize": 0,
                   "incomingTransactionErrors": 0,
                   "serviceTime": 0,
                   "serviceTimeTotal": 0,
                   "outgoingTransactions": 0,
                   "outgoingTransactionRequestSize": 0,
                   "outgoingTransactionResponseSize": 0,
                   "outgoingTransactionErrors": 0
                }
            }''')
        self.data["service"][service_name]["sum"] = manager.dict(data_service["sum"])

    def init_statistic_subservice(self, service_name, subservice_name):
        self.data["service"][service_name]["subservs"][subservice_name] = manager.dict({})
        data_subservice = json.loads('''{
              "sub": {
                "incomingTransactions": 0,
                "incomingTransactionRequestSize": 0,
                "incomingTransactionResponseSize": 0,
                "incomingTransactionErrors": 0,
                "serviceTime": 0,
                "serviceTimeTotal": 0,
                "outgoingTransactions": 0,
                "outgoingTransactionRequestSize": 0,
                "outgoingTransactionResponseSize": 0,
                "outgoingTransactionErrors": 0
              }
            }''')
        self.data["service"][service_name]["subservs"][subservice_name] = manager.dict(data_subservice["sub"])

    def get_statistics(self):
        standard_dict = dict(self.data)
        standard_dict["sum"] = dict(self.data["sum"])
        standard_dict["service"] = dict(self.data["service"])
        for serv in dict(self.data["service"]):
            standard_dict["service"][serv] = dict(self.data["service"][serv])
            standard_dict["service"][serv]["sum"] = dict(self.data["service"][serv]["sum"])
            standard_dict["service"][serv]["subservs"] = dict(self.data["service"][serv]["subservs"])
            for subserv in dict(self.data["service"][serv]["subservs"]):
                standard_dict["service"][serv]["subservs"][subserv] = dict(self.data["service"][serv]["subservs"][subserv])
        return standard_dict

    def collectMetrics(self, service_start, service_name = None, subservice_name = None,
                       request = None, response = None, flow = None):
        if not settings.ORC_EXTENDED_METRICS:
            return

        with self.lock:
            service_stop = time.time()
            transactionError = False
            if flow:
                flow_metrics = flow.getFlowMetrics()
            else:
                flow_metrics = {
                    "serviceTime": 0,
                    "serviceTimeTotal": 0,
                    "outgoingTransactions": 0,
                    "outgoingTransactionRequestSize": 0,
                    "outgoingTransactionResponseSize": 0,
                    "outgoingTransactionErrors": 0,
                }
            if service_name != None and not service_name in self.data["service"]:
                self.init_statistic_service(service_name)

            if (service_name != None and subservice_name != None and
                not subservice_name in self.data["service"][service_name]["subservs"]):
                self.init_statistic_subservice(service_name, subservice_name)

            # Analize "response"" to know if is a Response about an error or not
            if response.status_code not in [200, 201, 204]:
                # API error
                transactionError = True

            if service_name != None:
                if subservice_name != None:
                    # Service and Subservice
                    if not transactionError:
                        self.add_statistic_subservice(service_name, subservice_name, "incomingTransactions", 1)
                    else:
                        self.add_statistic_subservice(service_name, subservice_name, "incomingTransactionErrors", 1)
                    self.add_statistic_subservice(service_name, subservice_name, "incomingTransactionRequestSize", len(json.dumps(request.data)))
                    self.add_statistic_subservice(service_name, subservice_name, "incomingTransactionResponseSize", len(json.dumps(response.data)))
                    self.add_statistic_subservice(service_name, subservice_name, "serviceTimeTotal", (service_stop - service_start))
                    self.add_statistic_subservice(service_name, subservice_name, "outgoingTransactions", flow_metrics["outgoingTransactions"])
                    self.add_statistic_subservice(service_name, subservice_name, "outgoingTransactionRequestSize", flow_metrics["outgoingTransactionRequestSize"])
                    self.add_statistic_subservice(service_name, subservice_name, "outgoingTransactionResponseSize", flow_metrics["outgoingTransactionResponseSize"])
                    self.add_statistic_subservice(service_name, subservice_name, "outgoingTransactionErrors", flow_metrics["outgoingTransactionErrors"])
                    self.add_statistic_subservice(service_name, subservice_name, "serviceTimeTotal", flow_metrics["serviceTimeTotal"])

                # Service
                if not transactionError:
                    self.add_statistic_service(service_name, "incomingTransactions", 1)
                else:
                    self.add_statistic_service(service_name, "incomingTransactionErrors", 1)
                self.add_statistic_service(service_name, "incomingTransactionRequestSize", len(json.dumps(request.data)))
                self.add_statistic_service(service_name, "incomingTransactionResponseSize", len(json.dumps(response.data)))
                self.add_statistic_service(service_name, "serviceTimeTotal", (service_stop - service_start))
                self.add_statistic_service(service_name, "outgoingTransactions", flow_metrics["outgoingTransactions"])
                self.add_statistic_service(service_name, "outgoingTransactionRequestSize", flow_metrics["outgoingTransactionRequestSize"])
                self.add_statistic_service(service_name, "outgoingTransactionResponseSize", flow_metrics["outgoingTransactionResponseSize"])
                self.add_statistic_service(service_name, "outgoingTransactionErrors", flow_metrics["outgoingTransactionErrors"])
                self.add_statistic_service(service_name, "serviceTimeTotal", flow_metrics["serviceTimeTotal"])

            # Sum
            if not transactionError:
                self.add_statistic_sum("incomingTransactions", 1)
            else:
                self.add_statistic_sum("incomingTransactionErrors", 1)
            self.add_statistic_sum("incomingTransactionRequestSize", len(json.dumps(request.data)) )
            self.add_statistic_sum("incomingTransactionResponseSize", len(json.dumps(response.data)))
            self.add_statistic_sum("serviceTimeTotal", (service_stop - service_start))
            self.add_statistic_sum("outgoingTransactions", flow_metrics["outgoingTransactions"])
            self.add_statistic_sum("outgoingTransactionRequestSize", flow_metrics["outgoingTransactionRequestSize"])
            self.add_statistic_sum("outgoingTransactionResponseSize", flow_metrics["outgoingTransactionResponseSize"])
            self.add_statistic_sum("outgoingTransactionErrors", flow_metrics["outgoingTransactionErrors"])
            self.add_statistic_sum("serviceTimeTotal", flow_metrics["serviceTimeTotal"])


    def resetMetrics(self):
        with self.lock:
            self.data["service"] = manager.dict({})
            data_sum = json.loads('''{ "sum": {
                    "incomingTransactions": 0,
                    "incomingTransactionRequestSize": 0,
                    "incomingTransactionResponseSize": 0,
                    "incomingTransactionErrors": 0,
                    "serviceTime": 0,
                    "serviceTimeTotal": 0,
                    "outgoingTransactions": 0,
                    "outgoingTransactionRequestSize": 0,
                    "outgoingTransactionResponseSize": 0,
                    "outgoingTransactionErrors": 0
            } }''')
            self.data["sum"] = manager.dict(data_sum["sum"])


    def composeMetrics(self):
        result = self.get_statistics()
        if not settings.ORC_EXTENDED_METRICS:
            return result

        for serv in result["service"]:
            if result["service"][serv]["sum"]["serviceTimeTotal"] > 0:
                result["service"][serv]["sum"]["serviceTime"] = result["service"][serv]["sum"]["serviceTimeTotal"] / (
                    result["service"][serv]["sum"]["incomingTransactions"] +
                    result["service"][serv]["sum"]["incomingTransactionErrors"] +
                    result["service"][serv]["sum"]["outgoingTransactions"] +
                    result["service"][serv]["sum"]["outgoingTransactionErrors"]
                )

            for subserv in result["service"][serv]["subservs"]:
                if result["service"][serv]["subservs"][subserv]["serviceTimeTotal"] > 0:
                    result["service"][serv]["subservs"][subserv]["serviceTime"] = result["service"][serv]["subservs"][subserv]["serviceTimeTotal"] / (
                        result["service"][serv]["subservs"][subserv]["incomingTransactions"] +
                        result["service"][serv]["subservs"][subserv]["incomingTransactionErrors"] +
                        result["service"][serv]["subservs"][subserv]["outgoingTransactions"] +
                        result["service"][serv]["subservs"][subserv]["outgoingTransactionErrors"]
                    )

        if result["sum"]["serviceTimeTotal"] > 0:
            result["sum"]["serviceTime"] = result["sum"]["serviceTimeTotal"] / (
                result["sum"]["incomingTransactions"] +
                result["sum"]["incomingTransactionErrors"] +
                result["sum"]["outgoingTransactions"] +
                result["sum"]["outgoingTransactionErrors"]
            )
        return result
