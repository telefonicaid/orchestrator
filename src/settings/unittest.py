"""
(c) Copyright 2015 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
"""
import os

from common import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
    'users': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

LOGGING.update({
    'loggers': {
        'django.request': {
            'handlers': ['console']
        },
        'kdaf_api': {
            'handlers': ['console']
        }
    }
})


INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
COBERTURA_DIR = os.path.join(PROJECT_ROOT, 'target', 'site', 'cobertura')
UNIT_TESTS_DIR = os.path.join(PROJECT_ROOT, 'target', 'surefire-reports')
if not os.path.exists(COBERTURA_DIR):
    os.makedirs(COBERTURA_DIR)

if not os.path.exists(UNIT_TESTS_DIR):
    os.makedirs(UNIT_TESTS_DIR)

NOSE_ARGS = [
    '-s',
    '-v',
    '--cover-erase',
    '--cover-branches',
    '--with-coverage',
    '--cover-package=authorizations,bsc,ts,kow',
    '--cover-xml',
    '--cover-xml-file={0}/coverage-api.xml'.format(COBERTURA_DIR),
    '--with-xunit',
    '--xunit-file={0}/TEST-api.xml'.format(UNIT_TESTS_DIR)
]


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


REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon']='200/sec'
