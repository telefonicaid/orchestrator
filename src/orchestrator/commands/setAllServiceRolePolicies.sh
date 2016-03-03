#!/bin/bash

# Set Keystone and Keypass endpoints
KEYSTONE_HOST=localhost
KEYSTONE_PORT=5000
KEYSTONE_PROTOCOL=http

KEYPASS_HOST=localhost
KEYPASS_PORT=8080
KEYPASS_PROTOCOL=http

# Set service and service admin credentials
SERVICE_NAME=SmartValencia
SERVICE_ADMIN_USER=adm1
SERVICE_ADMIN_PASSWORD=password



# Ensure ServiceCustomer role is created in SERVICE_NAME
SERVICE_ROLE=ServiceCustomer

./createNewServiceRole.py $KEYSTONE_PROTOCOL  \
                          $KEYSTONE_HOST      \
                          $KEYSTONE_PORT      \
                          $SERVICE_NAME       \
                          $SERVICE_ADMIN_USER \
                          $SERVICE_ADMIN_PASSWORD \
                          $SERVICE_ROLE       \
                          $KEYPASS_PROTOCOL   \
                          $KEYPASS_HOST       \
                          $KEYPASS_PORT



IOTMODULES=( "orion" "perseo" "sth" "iotagent" "keypass" )

IOTROLES=( "Admin" "SubServiceAdmin" "ServiceCustomer" "SubServiceCustomer" )


for i in "${IOTMODULES[@]}"
do
    #echo $i

    for j in "${IOTROLES[@]}"
    do
        #echo $j
        SERVICE_ROLE=$j
        
        # policy-COMPONENT-admin2.xml -> Admin
        # policy-COMPONENT-admin.xml -> SubServiceAdmin
        # policy-COMPONENT-customer2.xml -> ServiceCustomer
        # policy-COMPONENT-customer.xml -> SubServiceCustomer        
        if [ $SERVICE_ROLE == "Admin" ]; then
            suffix_name="admin2"
        fi
        if [ $SERVICE_ROLE == "SubServiceAdmin" ]; then
            suffix_name="admin"
        fi
        if [ $SERVICE_ROLE == "ServiceCustomer" ]; then
            suffix_name="customer2"
        fi
        if [ $SERVICE_ROLE == "SubServiceCustomer" ]; then
            suffix_name="customer"
        fi
        
        POLICY_FILE_NAME="policy-${i}-${suffix_name}.xml"
        #echo $POLICY_FILE_NAME
        python ./setRolePolicy.py $KEYSTONE_PROTOCOL  \
                                  $KEYSTONE_HOST      \
                                  $KEYSTONE_PORT      \
                                  $SERVICE_NAME       \
                                  $SERVICE_ADMIN_USER \
                                  $SERVICE_ADMIN_PASSWORD \
                                  $SERVICE_ROLE       \
                                  $POLICY_FILE_NAME   \
                                  $KEYPASS_PROTOCOL   \
                                  $KEYPASS_HOST       \
                                  $KEYPASS_PORT
    done
    
done






