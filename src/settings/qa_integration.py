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

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon']='30/sec'
