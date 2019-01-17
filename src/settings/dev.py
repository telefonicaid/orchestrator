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

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

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

# Context Broker enpodint (with or without pep, but recommended with)
ORION = {
    "host": "localhost",
    "port": "1026",
    "protocol":"http"
}

# PEP PERSEO endpoint (with or without pep, but recommended with)
PEP_PERSEO = {
    "host": "localhost",
    "port": "9090",
    "protocol":"http",
}

#
## IOTMODULES
#
# STH endpoint (just for use as reference in Orion Subscriptions)
STH = {
    "host": "localhost",
    "port": "18666",
    "protocol":"http",
    "notifypath":"/notify"
}

# PERSEO endpoint (just for use as reference in Orion Subscriptions)
PERSEO = {
    "host": "localhost",
    "port": "19090",
    "protocol":"http",
    "notifypath":"/notices"
}

# CYGNUS endpoint (just for use as reference in Orion Subscriptions)
CYGNUS = {
    "host": "localhost",
    "port": "5050",
    "protocol":"http",
    "notifypath":"/notify"
}

IOTMODULES = [ "CYGNUS", "PERSEO" ]


# LDAP endpoint
LDAP = {
    "host": "localhost",
    "port": "389",
    "basedn": "dc=openstack,dc=org"
}

MAILER = {
    "host": "localhost",
    "port": "587",
    "user": "smtpuser@yourdomain.com",
    "password": "yourpassword",
    "from": "smtpuser",
    "to": "smtpuser"
}

MONGODB = {
    "URI": "mongodb://localhost:27017"
}

PEP = {
    "user": "pep",
    "password": "pep"
}

IOTAGENT = {
    "user": "iotagent",
    "password": "iotagent"
}
