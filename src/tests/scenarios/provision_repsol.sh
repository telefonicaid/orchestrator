#!/bin/bash

#####################
# Smart City Repsol
#####################

cd ../../orchestrator/commands/

python ./createNewService.py http               \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 repsolglp      \
                                 Repsol_GLP     \
                                 repsol_admin   \
                                 password       \
                                 http           \
                                 localhost      \
                                 8080
cd -
