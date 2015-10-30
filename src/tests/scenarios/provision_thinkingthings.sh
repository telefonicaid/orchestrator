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
                                 4passw0rd      \
                                 http           \
                                 localhost      \
                                 8080


python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      thinkingthings \
                                      admin_tt       \
                                      4passw0rd      \
                                      user_x         \
                                      user_x

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       thinkingthings \
                                       admin_tt       \
                                       4passw0rd      \
                                       user_x         \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       thinkingthings \
                                       user_x         \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceAdmin\
                                       user_x

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       thinkingthings \
                                       user_x         \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       user_x

cd -
