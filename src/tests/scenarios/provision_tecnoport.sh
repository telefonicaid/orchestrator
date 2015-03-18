#!/bin/bash

cd ../../orchestrator/commands/

  ./createNewServiceKeystone.py http            \
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

  ./assignInheritRoleServiceUserKeystone.py http     \
                                    localhost        \
                                    5000             \
                                    Tecnoport2015    \
                                    tecnoport_admin  \
                                    password         \
                                    tecnoport_admin  \
                                    SubServiceAdmin  \
                                    http             \
                                    localhost        \
                                    8080

  ./createNewSubServiceKeystone.py  http          \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      cuts        \
                                      cuts

  ./createNewServiceUserKeystone.py  http           \
                                      localhost     \
                                      5000          \
                                      tecnoport     \
                                      tecnoport_admin   \
                                      password       \
                                      tecnoport_customer\
                                      password

  ./createNewServiceRole.py  http                   \
                                     localhost      \
                                     5001           \
                                     tecnoport      \
                                     tecnoport_admin\
                                     password       \
                                     ServiceCustomer


  ./assignRoleServiceUserKeystone.py http            \
                                      localhost      \
                                      5001           \
                                      tecnoport      \
                                      tecnoport_admin\
                                      password       \
                                      ServiceCustomer\
                                      tecnoport_customer

 ./createNewSubServiceAdminKeystone.py  http      \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      cuts        \
                                      tecnoport_cuts_admin  \
                                      password

  ./createNewSubServiceUserKeystone.py  http         \
                                       localhost     \
                                       5000          \
                                       tecnoport     \
                                       tecnoport_admin         \
                                       password       \
                                       cuts           \
                                       tecnoport_cuts_customer \
                                       password

 ./createNewSubServiceKeystone.py  http           \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      erio        \
                                      erio

 ./createNewSubServiceAdminKeystone.py  http      \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      erio        \
                                      tecnoport_erio_admin  \
                                      password

 ./createNewSubServiceKeystone.py  http           \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      fps         \
                                      fps

 ./createNewSubServiceAdminKeystone.py  http      \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      fps         \
                                      tecnoport_fps_admin  \
                                      password


cd -
