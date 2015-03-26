#!/bin/bash

#####################
# Smart City Valencia
#####################

cd ../../orchestrator/commands/

python ./createNewService.sh http              \
                                localhost      \
                                5000           \
                                admin_domain   \
                                cloud_admin    \
                                password       \
                                sc_vlci        \
                                Smart_City_Valencia  \
                                sc_vlci_admin  \
                                password       \
                                http           \
                                localhost      \
                                8080

cd -
