#!/bin/bash

KEYSTONE_PROTOCOL=http
KEYSTONE_HOST=localhost
KEYSTONE_PORT=5000
KEYPASS_PROTOCOL=http
KEYPASS_HOST=localhost
KEYPASS_PORT=8080


function checkResult() {
    if [ $1 -eq 0 ]; then
        echo -n
        echo -e "- $2 ....... OK"
    else
        echo -e "Error found while $2. Code: $1. Aborting"
        exit $1
    fi
}

cd ../../orchestrator/commands/

python ./createNewService.py $KEYSTONE_PROTOCOL \
                                 $KEYSTONE_HOST \
                                 $KEYSTONE_PORT \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 smartcity      \
                                 smartcity      \
                                 adm1           \
                                 password       \
                                 $KEYPASS_PROTOCOL  \
                                 $KEYPASS_HOST  \
                                 $KEYPASS_PORT
checkResult $? "Creating service"

python ./assignInheritRoleServiceUser.py $KEYSTONE_PROTOCOL \
                                    $KEYSTONE_HOST   \
                                    $KEYSTONE_PORT   \
                                    smartcity        \
                                    adm1             \
                                    password         \
                                    adm1             \
                                    SubServiceAdmin
checkResult $? "assignInheritRole to admin"

python ./createNewSubService.py  $KEYSTONE_PROTOCOL  \
                                      $KEYSTONE_HOST \
                                      $KEYSTONE_PORT \
                                      smartcity      \
                                      adm1           \
                                      password       \
                                      Electricidad   \
                                      electricidad
checkResult $? "Creating sub service Electricidad"

python ./createNewServiceUser.py  $KEYSTONE_PROTOCOL \
                                      $KEYSTONE_HOST \
                                      $KEYSTONE_PORT \
                                      smartcity      \
                                      adm1           \
                                      password       \
                                      Alice          \
                                      password
checkResult $? "Creating user Alice"

python ./assignRoleSubServiceUser.py $KEYSTONE_PROTOCOL  \
                                       $KEYSTONE_HOST \
                                       $KEYSTONE_PORT \
                                       smartcity      \
                                       Electricidad   \
                                       adm1           \
                                       password       \
                                       SubServiceAdmin\
                                       Alice
checkResult $? "Assing role SubServiceAdmin to user Alice"

python ./createNewSubService.py  $KEYSTONE_PROTOCOL  \
                                      $KEYSTONE_HOST \
                                      $KEYSTONE_PORT \
                                      smartcity      \
                                      adm1           \
                                      password       \
                                      Basuras        \
                                      basuras
checkResult $? "Creating subservice Basuras"

python ./createNewServiceUser.py  $KEYSTONE_PROTOCOL  \
                                       $KEYSTONE_HOST \
                                       $KEYSTONE_PORT \
                                       smartcity      \
                                       adm1           \
                                       password       \
                                       bob            \
                                       password
checkResult $? "Creating user bob"

python ./assignRoleSubServiceUser.py $KEYSTONE_PROTOCOL  \
                                       $KEYSTONE_HOST \
                                       $KEYSTONE_PORT \
                                       smartcity      \
                                       Basuras        \
                                       adm1           \
                                       password       \
                                       SubServiceAdmin\
                                       bob
checkResult $? "Assign subServiceAdmin role to user bob"

python ./createNewServiceUser.py  $KEYSTONE_PROTOCOL \
                                      $KEYSTONE_HOST \
                                      $KEYSTONE_PORT \
                                      smartcity      \
                                      adm1           \
                                      password       \
                                      Carl           \
                                      password
checkResult $? "Creating user Carl"

# ServiceCustomer is already created at new service creation time
# python ./createNewServiceRole.py  $KEYSTONE_PROTOCOL \
#                                       $KEYSTONE_HOST \
#                                       $KEYSTONE_PORT \
#                                       smartcity      \
#                                       adm1           \
#                                       password       \
#                                       ServiceCustomer\
#                                       $KEYSTONE_PROTOCOL  \
#                                       $KEYSTONE_HOST \
#                                       $KEYPASS_PORT
# checkResult $? "creating new ServiceCustomer role"

python ./assignRoleServiceUser.py $KEYSTONE_PROTOCOL  \
                                       $KEYSTONE_HOST \
                                       $KEYSTONE_PORT \
                                       smartcity      \
                                       adm1           \
                                       password       \
                                       ServiceCustomer\
                                       Carl
checkResult $? "Assign ServiceCustomer role to user Carl"

python ./assignInheritRoleServiceUser.py $KEYSTONE_PROTOCOL \
                                    $KEYSTONE_HOST    \
                                    $KEYSTONE_PORT    \
                                    smartcity         \
                                    adm1              \
                                    password          \
                                    Carl              \
                                    SubServiceCustomer
checkResult $? "Assign subServiceCustomer role to user Carl"

cd -
