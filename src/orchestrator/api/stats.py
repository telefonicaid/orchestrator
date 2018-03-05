import logging
import json
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.throttling import AnonRateThrottle

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from datetime import datetime


class Stats(object):

    # Start Time
    uptime = datetime.utcnow()

    # All stats
    num_post_service = 0
    num_get_service = 0
    num_put_service = 0
    num_delete_service = 0

    num_post_subservice = 0
    num_get_subservice = 0
    num_put_subservice = 0
    num_delete_subservice = 0

    num_delete_user = 0
    num_put_user = 0
    num_get_user = 0
    num_post_user = 0

    num_get_userlist = 0
    num_post_userlist = 0

    num_delete_group = 0
    num_put_group = 0
    num_get_group = 0
    num_post_group = 0

    num_get_grouplist = 0
    num_post_grouplist = 0

    num_delete_role = 0
    num_post_role = 0
    num_get_role = 0
    num_get_role_policies = 0
    num_post_role_policies = 0

    num_delete_policy_from_role = 0
    num_get_policy_from_role = 0

    num_delete_roleassignment = 0
    num_post_roleassignment = 0
    num_get_roleassignment = 0

    num_post_trust = 0

    num_post_device = 0
    num_delete_device = 0

    num_post_devices = 0
    num_post_entity_service = 0

    num_get_module_activation = 0
    num_post_module_activation = 0
    num_delete_module_activation = 0

    num_update_loglevel = 0

    num_api_errors = 0
    num_flow_errors = 0

    service = {}
    sum = {
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

    def collectMetrics(self, service_start, service_name, subservice_name,
                       request, response, flow):
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
            self.service[service_name] = {
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
            not subservice_name in self.service[service_name]["subservs"]):
            self.service[service_name]["subservs"][subservice_name] = {
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
                    self.service[service_name]["subservs"][subservice_name]["incomingTransactions"] += 1
                else:
                    self.service[service_name]["subservs"][subservice_name]["incomingTransactionErrors"] += 1
                self.service[service_name]["subservs"][subservice_name]["incomingTransactionRequestSize"] += len(json.dumps(request.data))
                self.service[service_name]["subservs"][subservice_name]["incomingTransactionResponseSize"] += len(json.dumps(response.data))
                self.service[service_name]["subservs"][subservice_name]["serviceTimeTotal"] += (service_stop - service_start)

                self.service[service_name]["subservs"][subservice_name]["outgoingTransactions"] += flow_metrics["outgoingTransactions"]
                self.service[service_name]["subservs"][subservice_name]["outgoingTransactionRequestSize"] += flow_metrics["outgoingTransactionRequestSize"]
                self.service[service_name]["subservs"][subservice_name]["outgoingTransactionResponseSize"] += flow_metrics["outgoingTransactionResponseSize"]
                self.service[service_name]["subservs"][subservice_name]["outgoingTransactionErrors"] += flow_metrics["outgoingTransactionErrors"]
                self.service[service_name]["subservs"][subservice_name]["serviceTimeTotal"] += flow_metrics["serviceTimeTotal"]



            # Service
            if not transactionError:
                self.service[service_name]["sum"]["incomingTransactions"] += 1
            else:
                self.service[service_name]["sum"]["incomingTransactionErrors"] += 1
            self.service[service_name]["sum"]["incomingTransactionRequestSize"] += len(json.dumps(request.data))
            self.service[service_name]["sum"]["incomingTransactionResponseSize"] += len(json.dumps(response.data))
            self.service[service_name]["sum"]["serviceTimeTotal"] += (service_stop - service_start)
            self.service[service_name]["sum"]["outgoingTransactions"] += flow_metrics["outgoingTransactions"]
            self.service[service_name]["sum"]["outgoingTransactionRequestSize"] += flow_metrics["outgoingTransactionRequestSize"]
            self.service[service_name]["sum"]["outgoingTransactionResponseSize"] += flow_metrics["outgoingTransactionResponseSize"]
            self.service[service_name]["sum"]["outgoingTransactionErrors"] += flow_metrics["outgoingTransactionErrors"]
            self.service[service_name]["sum"]["serviceTimeTotal"] += flow_metrics["serviceTimeTotal"]

        # Sum
        if not transactionError:
            self.sum["incomingTransactions"] += 1
        else:
            self.sum["incomingTransactionErrors"] += 1
        self.sum["incomingTransactionRequestSize"] += len(json.dumps(request.data))
        self.sum["incomingTransactionResponseSize"] += len(json.dumps(response.data))
        self.sum["serviceTimeTotal"] += (service_stop - service_start)
        self.sum["outgoingTransactions"] += flow_metrics["outgoingTransactions"]
        self.sum["outgoingTransactionRequestSize"] += flow_metrics["outgoingTransactionRequestSize"]
        self.sum["outgoingTransactionResponseSize"] += flow_metrics["outgoingTransactionResponseSize"]
        self.sum["outgoingTransactionErrors"] += flow_metrics["outgoingTransactionErrors"]
        self.sum["serviceTimeTotal"] += flow_metrics["serviceTimeTotal"]


    def resetMetrics(self):
        self.service = {}
        self.sum = {
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

        result = {
            "service": self.service,
            "sum": self.sum
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
