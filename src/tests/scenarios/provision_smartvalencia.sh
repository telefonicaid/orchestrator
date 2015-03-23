#!/bin/bash

cd ../../orchestrator/commands/

  ./createNewService.py http                    \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 SmartValencia  \
                                 smartvalencia  \
                                 adm1           \
                                 password       \
                                 http           \
                                 localhost      \
                                 8080

  ./assignInheritRoleServiceUser.py http             \
                                    localhost        \
                                    5000             \
                                    SmartValencia    \
                                    adm1             \
                                    password         \
                                    adm1             \
                                    SubServiceAdmin  \
                                    http             \
                                    localhost        \
                                    8080

  ./createNewSubService.py  http                     \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Electricidad   \
                                      electricidad

  ./createNewSubServiceAdmin.py  http                \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Electricidad   \
                                      Alice          \
                                      password

  ./createNewSubService.py  http                     \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Basuras        \
                                      basuras

  ./createNewSubServiceUser.py  http                  \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       Electricidad   \
                                       bob            \
                                       password

  ./assignRoleSubServiceUser.py http                  \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       Basuras        \
                                       SubServiceAdmin\
                                       bob           

  ./createNewServiceUser.py  http                    \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Carl           \
                                      password

  ./createNewServiceRole.py  http                    \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      ServiceCustomer


  ./assignRoleServiceUser.py http                     \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       ServiceCustomer\
                                       Carl           

  ./assignInheritRoleServiceUser.py http              \
                                    localhost         \
                                    5000              \
                                    SmartValencia     \
                                    adm1              \
                                    password          \
                                    Carl              \
                                    SubServiceCustomer\
                                    http              \
                                    localhost         \
                                    8080


cd -
