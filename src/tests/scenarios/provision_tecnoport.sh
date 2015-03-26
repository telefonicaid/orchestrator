#!/bin/bash

cd ../../orchestrator/commands/

  ./createNewService.py http                    \
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

  ./assignInheritRoleServiceUser.py http             \
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

  ./createNewSubService.py  http                  \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      cuts        \
                                      cuts

  ./createNewServiceUser.py  http                   \
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


  ./assignRoleServiceUser.py http                    \
                                      localhost      \
                                      5001           \
                                      tecnoport      \
                                      tecnoport_admin\
                                      password       \
                                      ServiceCustomer\
                                      tecnoport_customer

 ./createNewSubServiceAdmin.py  http              \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      cuts        \
                                      tecnoport_cuts_admin  \
                                      password

  ./createNewSubServiceUser.py  http                 \
                                       localhost     \
                                       5000          \
                                       tecnoport     \
                                       tecnoport_admin         \
                                       password       \
                                       cuts           \
                                       tecnoport_cuts_customer \
                                       password

 ./createNewSubService.py  http                   \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      erio        \
                                      erio

 ./createNewSubServiceAdmin.py  http              \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      erio        \
                                      tecnoport_erio_admin  \
                                      password

 ./createNewSubService.py  http                   \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      fps         \
                                      fps

 ./createNewSubServiceAdmin.py  http              \
                                      localhost   \
                                      5000        \
                                      tecnoport   \
                                      tecnoport_admin \
                                      password    \
                                      fps         \
                                      tecnoport_fps_admin  \
                                      password


cd -
