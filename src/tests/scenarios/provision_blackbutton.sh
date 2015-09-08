#!/bin/bash

###################
# BlackButton     #
###################

cd ../../orchestrator/commands/

python ./createNewService.py http               \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 blackbutton    \
                                 BlackButton    \
                                 admin_tt       \
                                 4passw0rd      \
                                 http           \
                                 localhost      \
                                 8080

python ./assignInheritRoleServiceUser.py http        \
                                    localhost        \
                                    5000             \
                                    blackbutton      \
                                    admin_tt         \
                                    4passw0rd        \
                                    admin_tt         \
                                    SubServiceAdmin  \
                                    http             \
                                    localhost        \
                                    8080

python ./assignInheritRoleServiceUser.py http        \
                                    localhost        \
                                    5000             \
                                    blackbutton      \
                                    admin_tt         \
                                    4passw0rd        \
                                    admin_tt         \
                                    SubServiceCustomer  \
                                    http             \
                                    localhost        \
                                    8080

python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      blackbutton    \
                                      admin_tt       \
                                      4passw0rd      \
                                      telepizza      \
                                      TelePizza

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_tt       \
                                       4passw0rd      \
                                       admin_telepizza \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       telepizza      \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceAdmin\
                                       admin_telepizza

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       telepizza      \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       admin_telepizza

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_tt       \
                                       4passw0rd      \
                                       client_telepizza \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       telepizza      \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       client_telepizza


python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      blackbutton    \
                                      admin_tt       \
                                      4passw0rd      \
                                      carrefour      \
                                      Carrefour

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_tt       \
                                       4passw0rd      \
                                       admin_carrefour \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       carrefour      \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceAdmin\
                                       admin_carrefour

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       carrefour      \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       admin_carrefour

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_tt       \
                                       4passw0rd      \
                                       client_carrefour \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       carrefour      \
                                       admin_tt       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       client_carrefour


cd -
