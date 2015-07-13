#!/bin/bash

###################
# Thinking Things #
###################

cd ../../orchestrator/commands/

python ./createNewService.py http               \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 thinkingthings \
                                 Thinking_things\
                                 admin_tt       \
                                 password       \
                                 http           \
                                 localhost      \
                                 8080


python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      thinkingthings \
                                      admin_tt       \
                                      password       \
                                      user_x         \
                                      user_x

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       thinkingthings \
                                       adm_tt         \
                                       password       \
                                       user_x         \
                                       password

python ./assignRoleSubServiceUser.py http              \
                                       localhost      \
                                       5000           \
                                       thinkingthings \
                                       user_x         \
                                       admin_tt       \
                                       password       \
                                       SubServiceAdmin\
                                       user_x

python ./assignRoleSubServiceUser.py http              \
                                       localhost      \
                                       5000           \
                                       thinkingthings \
                                       user_x         \
                                       admin_tt       \
                                       password       \
                                       SubServiceCustomer\
                                       user_x

cd -
