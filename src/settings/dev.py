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

KEYSTONE = {
    "host": "localhost",
    "port": "5001",
    "protocol":"http"
}

KEYPASS = {
    "host": "localhost",
    "port": "7070",
    "protocol":"http"
}

IOTA = {
    "host": "localhost",
    "port": "4041",
    "protocol":"http"
}

ORION = {
    "host": "localhost",
    "port": "1026",
    "protocol":"http"
}

CA = {
    "host": "localhost",
    "port": "9999",
    "protocol":"http"
}

CYGNUS = {
    "host": "localhost",
    "port": "5050",
    "protocol":"http"
}
