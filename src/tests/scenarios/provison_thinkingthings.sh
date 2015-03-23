#!/bin/bash

###################
# Thinking Things #
###################

cd ../../orchestrator/commands/

./createNewService.py http                      \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 ThinkingThings \
                                 Thinking_things\
                                 admin_tt       \
                                 password       \
                                 http           \
                                 localhost      \
                                 8080


./createNewSubKeystone.py  http                      \
                                      localhost      \
                                      5000           \
                                      ThinkingThings \
                                      admin_tt       \
                                      password       \
                                      user_x         \
                                      user_x


  ./createNewSubServiceUser.py  http                  \
                                       localhost      \
                                       5000           \
                                       ThinkingThings \
                                       adm_tt         \
                                       password       \
                                       user_x         \
                                       user_x         \
                                       password

  ./assignRoleSubServiceUserpy http                   \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       admin_tt       \
                                       password       \
                                       user_x         \
                                       SubServiceAdmin\
                                       user_x

cd -
