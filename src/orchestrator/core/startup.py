from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

import logging
import os

logger = logging.getLogger('orchestrator_api')


def read_banner():
    banner_dir = os.path.dirname(__file__)
    handle=open(banner_dir + '/'+ 'banner.txt','r+')
    var=handle.read()
    return var

def run():
    logger.info("Starting Service %s " % read_banner())
