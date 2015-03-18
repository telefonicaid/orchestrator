#!/bin/bash

###################
# Thinking Things #
###################

cd ../../orchestrator/commands/

./createNewServiceKeystone.py http              \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 ThinkingThings \
                                 Thinking_things\
                                 admin   \
                                 password       \
                                 http           \
                                 localhost      \
                                 8080
cd -
