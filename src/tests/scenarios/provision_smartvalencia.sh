#!/bin/bash

cd ../../orchestrator/commands/

  ./createNewServiceKeystone.py http            \
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

  ./assignInheritRoleServiceUserKeystone.py http     \
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

  ./createNewSubServiceKeystone.py  http             \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Electricidad   \
                                      electricidad

  ./createNewSubServiceAdminKeystone.py  http        \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Electricidad   \
                                      Alice          \
                                      password

  ./createNewSubServiceKeystone.py  http             \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Basuras        \
                                      basuras

  ./createNewSubServiceUserKeystone.py  http          \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       Electricidad   \
                                       bob            \
                                       password

  ./assignRoleSubServiceUserKeystone.py http          \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       Basuras        \
                                       SubServiceAdmin\
                                       bob           

  ./createNewServiceUserKeystone.py  http            \
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


  ./assignRoleServiceUserKeystone.py http             \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       ServiceCustomer\
                                       Carl           

  ./assignInheritRoleServiceUserKeystone.py http      \
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
