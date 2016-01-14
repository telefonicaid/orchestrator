"""
(c) Copyright 2015 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
"""
from common import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Keystone Endpoint
KEYSTONE = {
    "host": "localhost",
    "port": "5001",
    "protocol":"http"
}

# Keypass endpoint (tipically without pep)
KEYPASS = {
    "host": "localhost",
    "port": "17070",
    "protocol":"http"
}

# IoTA endpoint
IOTA = {
    "host": "localhost",
    "port": "4041",
    "protocol":"http"
}

# Context Broker enpodint (with or without pep, but recommended with)
ORION = {
    "host": "localhost",
    "port": "10026",
    "protocol":"http"
}

# Context Adapter enpodint (BlackButton scenario)
CA = {
    "host": "localhost",
    "port": "9999",
    "protocol":"http"
}

# CYGNUS endpoint (just for use as reference in Orion Subscriptions)
CYGNUS = {
    "host": "localhost",
    "port": "5050",
    "protocol":"http"
}

# STH endpoint (just for use as reference in Orion Subscriptions)
STH = {
    "host": "localhost",
    "port": "18666",
    "protocol":"http"
}

# PERSEO endpoint (just for use as reference in Orion Subscriptions)
PERSEO = {
    "host": "localhost",
    "port": "19090",
    "protocol":"http"
}

#IOTMODULES = [ "STH", "CYGNUS", "PERSEO", "CA" ]
