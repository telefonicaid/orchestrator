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
                                 admin_bb       \
                                 4passw0rd      \
                                 http           \
                                 localhost      \
                                 8080

python ./assignInheritRoleServiceUser.py http        \
                                    localhost        \
                                    5000             \
                                    blackbutton      \
                                    admin_bb         \
                                    4passw0rd        \
                                    admin_bb         \
                                    SubServiceAdmin  \
                                    http             \
                                    localhost        \
                                    8080

python ./assignInheritRoleServiceUser.py http        \
                                    localhost        \
                                    5000             \
                                    blackbutton      \
                                    admin_bb         \
                                    4passw0rd        \
                                    admin_bb         \
                                    SubServiceCustomer  \
                                    http             \
                                    localhost        \
                                    8080

python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      blackbutton    \
                                      admin_bb       \
                                      4passw0rd      \
                                      telepizza      \
                                      TelePizza

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_bb       \
                                       4passw0rd      \
                                       admin_telepizza \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       telepizza      \
                                       admin_bb       \
                                       4passw0rd      \
                                       SubServiceAdmin\
                                       admin_telepizza

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       telepizza      \
                                       admin_bb       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       admin_telepizza

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_bb       \
                                       4passw0rd      \
                                       client_telepizza \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       telepizza      \
                                       admin_bb       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       client_telepizza


python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      blackbutton    \
                                      admin_bb       \
                                      4passw0rd      \
                                      carrefour      \
                                      Carrefour

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_bb       \
                                       4passw0rd      \
                                       admin_carrefour \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       carrefour      \
                                       admin_bb       \
                                       4passw0rd      \
                                       SubServiceAdmin\
                                       admin_carrefour

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       carrefour      \
                                       admin_bb       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       admin_carrefour

python  ./createNewServiceUser.py  http               \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       admin_bb       \
                                       4passw0rd      \
                                       client_carrefour \
                                       4passw0rd

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       blackbutton    \
                                       carrefour      \
                                       admin_bb       \
                                       4passw0rd      \
                                       SubServiceCustomer\
                                       client_carrefour


python ./registerSubServiceDevice.py  http             \
                                      localhost        \
                                      5000             \
                                      blackbutton      \
                                      telepizza        \
                                      admin_bb         \
                                      4passw0rd        \
                                      button_dev_01    \
                                      BlackButton      \
                                      TT_BLACKBUTTON   \
                                      button_dev_01    \
                                      AAA              \
                                      1234567890       \
                                      0987654321       \
                                      synchronous      \
                                      S-001            \
                                      40.4188,-3.6919  \
                                      http             \
                                      localhost        \
                                      4041             \
                                      http             \
                                      localhost        \
                                      1026

cd -
