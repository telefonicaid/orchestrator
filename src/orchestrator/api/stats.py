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

from django.conf import settings
from datetime import datetime

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
        self.lock = threading.Lock()

        with self.lock:
            if 'initialized' not in self.data:
                # Start Time
                self.data["uptime"] = str(datetime.utcnow())

                self.data["service"] = {}
                self.data["sum"] = {
                    "incomingTransactions": 0,
                    "incomingTransactionRequestSize": 0,
                    "incomingTransactionResponseSize": 0,
                    "incomingTransactionErrors": 0,
                    "serviceTime": 0,
                    "serviceTimeTotal": 0,
                    "outgoingTransactions": 0,
                    "outgoingTransactionRequestSize": 0,
                    "outgoingTransactionResponseSize": 0,
                    "outgoingTransactionErrors": 0,
                }
                self.data['initialized'] = True



    def add_statistic(self, key, value):
        with self.lock:
            if key in self.data:
                self.data[key] += value
            else:
                self.data[key] = value

    def collectMetrics(self, service_start, service_name, subservice_name,
                       request, response, flow):
        with self.lock:
            if not settings.ORC_EXTENDED_METRICS:
                # Do nothing
                return

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

            if service_name and not service_name in self.service:
                self.data.service[service_name] = {
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
                        "outgoingTransactionErrors": 0,
                    },
                    "subservs": {}
                }

            if (service_name and subservice_name and
                not subservice_name in self.data.service[service_name]["subservs"]):
                self.data.service[service_name]["subservs"][subservice_name] = {
                    "incomingTransactions": 0,
                    "incomingTransactionRequestSize": 0,
                    "incomingTransactionResponseSize": 0,
                    "incomingTransactionErrors": 0,
                    "serviceTime": 0,
                    "serviceTimeTotal": 0,
                    "outgoingTransactions": 0,
                    "outgoingTransactionRequestSize": 0,
                    "outgoingTransactionResponseSize": 0,
                    "outgoingTransactionErrors": 0,
                }

            # Analize "response"" to know if is a Response about an error or not
            if response.status_code not in [200, 201, 204]:
                # API error
                transactionError = True

            if service_name:
                if subservice_name:
                    # Service and Subservice
                    if not transactionError:
                        self.data.service[service_name]["subservs"][subservice_name]["incomingTransactions"] += 1
                    else:
                        self.data.service[service_name]["subservs"][subservice_name]["incomingTransactionErrors"] += 1
                    self.data.service[service_name]["subservs"][subservice_name]["incomingTransactionRequestSize"] += len(json.dumps(request.data))
                    self.data.service[service_name]["subservs"][subservice_name]["incomingTransactionResponseSize"] += len(json.dumps(response.data))
                    self.data.service[service_name]["subservs"][subservice_name]["serviceTimeTotal"] += (service_stop - service_start)

                    self.data.service[service_name]["subservs"][subservice_name]["outgoingTransactions"] += flow_metrics["outgoingTransactions"]
                    self.data.service[service_name]["subservs"][subservice_name]["outgoingTransactionRequestSize"] += flow_metrics["outgoingTransactionRequestSize"]
                    self.data.service[service_name]["subservs"][subservice_name]["outgoingTransactionResponseSize"] += flow_metrics["outgoingTransactionResponseSize"]
                    self.data.service[service_name]["subservs"][subservice_name]["outgoingTransactionErrors"] += flow_metrics["outgoingTransactionErrors"]
                    self.data.service[service_name]["subservs"][subservice_name]["serviceTimeTotal"] += flow_metrics["serviceTimeTotal"]



                # Service
                if not transactionError:
                    self.data.service[service_name]["sum"]["incomingTransactions"] += 1
                else:
                    self.data.service[service_name]["sum"]["incomingTransactionErrors"] += 1
                self.data.service[service_name]["sum"]["incomingTransactionRequestSize"] += len(json.dumps(request.data))
                self.data.service[service_name]["sum"]["incomingTransactionResponseSize"] += len(json.dumps(response.data))
                self.data.service[service_name]["sum"]["serviceTimeTotal"] += (service_stop - service_start)
                self.data.service[service_name]["sum"]["outgoingTransactions"] += flow_metrics["outgoingTransactions"]
                self.data.service[service_name]["sum"]["outgoingTransactionRequestSize"] += flow_metrics["outgoingTransactionRequestSize"]
                self.data.service[service_name]["sum"]["outgoingTransactionResponseSize"] += flow_metrics["outgoingTransactionResponseSize"]
                self.data.service[service_name]["sum"]["outgoingTransactionErrors"] += flow_metrics["outgoingTransactionErrors"]
                self.data.service[service_name]["sum"]["serviceTimeTotal"] += flow_metrics["serviceTimeTotal"]

            # Sum
            if not transactionError:
                self.data.sum["incomingTransactions"] += 1
            else:
                self.data.sum["incomingTransactionErrors"] += 1
            self.data.sum["incomingTransactionRequestSize"] += len(json.dumps(request.data))
            self.data.sum["incomingTransactionResponseSize"] += len(json.dumps(response.data))
            self.data.sum["serviceTimeTotal"] += (service_stop - service_start)
            self.data.sum["outgoingTransactions"] += flow_metrics["outgoingTransactions"]
            self.data.sum["outgoingTransactionRequestSize"] += flow_metrics["outgoingTransactionRequestSize"]
            self.data.sum["outgoingTransactionResponseSize"] += flow_metrics["outgoingTransactionResponseSize"]
            self.data.sum["outgoingTransactionErrors"] += flow_metrics["outgoingTransactionErrors"]
            self.data.sum["serviceTimeTotal"] += flow_metrics["serviceTimeTotal"]


    def resetMetrics(self):
        with self.lock:
            self.data.service = {}
            self.data.sum = {
                "incomingTransactions": 0,
                "incomingTransactionRequestSize": 0,
                "incomingTransactionResponseSize": 0,
                "incomingTransactionErrors": 0,
                "serviceTime": 0,
                "serviceTimeTotal": 0,
                "outgoingTransactions": 0,
                "outgoingTransactionRequestSize": 0,
                "outgoingTransactionResponseSize": 0,
                "outgoingTransactionErrors": 0,
            }


    def composeMetrics(self):
        with self.lock:
            result = {
                "service": self.data.service,
                "sum": self.data.sum
            }

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
