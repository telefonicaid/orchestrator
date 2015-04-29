#!/bin/bash

cd ../../orchestrator/commands/

python  ./createNewService.py http              \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 tecnoport      \
                                 TecnoPort2015  \
                                 tecnoport_admin\
                                 password       \
                                 http           \
                                 localhost      \
                                 8080

python ./assignInheritRoleServiceUser.py http        \
                                    localhost        \
                                    5000             \
                                    tecnoport        \
                                    tecnoport_admin  \
                                    password         \
                                    tecnoport_admin  \
                                    SubServiceAdmin  \
                                    http             \
                                    localhost        \
                                    8080

python  ./createNewSubService.py  http            \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      cuts        \
                                      cuts

python ./createNewServiceUser.py  http              \
                                      localhost     \
                                      5000          \
                                      tecnoport     \
                                      tecnoport_admin   \
                                      password       \
                                      tecnoport_customer\
                                      password

python ./createNewServiceRole.py  http              \
                                     localhost      \
                                     5001           \
                                     tecnoport      \
                                     tecnoport_admin\
                                     password       \
                                     ServiceCustomer\
                                     http           \
                                     localhost      \
                                     8080

python  ./assignRoleServiceUser.py http              \
                                      localhost      \
                                      5001           \
                                      tecnoport      \
                                      tecnoport_admin\
                                      password       \
                                      ServiceCustomer\
                                      tecnoport_customer

python ./createNewServiceUser.py  http               \
                                      localhost      \
                                      5000           \
                                      tecnoport      \
                                      tecnoport_admin\
                                      password       \
                                      tecnoport_cuts_admin          \
                                      password

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       tecnoport      \
                                       cuts           \
                                       tecnoport_admin\
                                       password       \
                                       SubServiceAdmin\
                                       tecnoport_cuts_admin

python ./createNewServiceUser.py  http               \
                                      localhost      \
                                      5000           \
                                      tecnoport      \
                                      tecnoport_admin\
                                      password       \
                                      tecnoport_cuts_customer          \
                                      password

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       tecnoport      \
                                       cuts           \
                                       tecnoport_admin\
                                       password       \
                                       SubServiceCustomer\
                                       tecnoport_cuts_customer

python ./createNewSubService.py  http             \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      erio        \
                                      erio

python ./createNewServiceUser.py  http               \
                                      localhost      \
                                      5000           \
                                      tecnoport      \
                                      tecnoport_admin\
                                      password       \
                                      tecnoport_erio_admin          \
                                      password

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       tecnoport      \
                                       erio           \
                                       tecnoport_admin\
                                       password       \
                                       SubServiceAdmin\
                                       tecnoport_erio_admin

python ./createNewSubService.py  http             \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      fps         \
                                      fps

python ./createNewServiceUser.py  http               \
                                      localhost      \
                                      5000           \
                                      tecnoport      \
                                      tecnoport_admin\
                                      password       \
                                      tecnoport_fps_admin          \
                                      password

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       tecnoport      \
                                       fps            \
                                       tecnoport_admin\
                                       password       \
                                       SubServiceAdmin\
                                       tecnoport_fps_admin

cd -
