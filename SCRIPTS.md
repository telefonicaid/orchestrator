# Command line scripts

Orchestrator actions can be done through API or invoking command line scripts.

Usage:

```
$ python ./<orchestrator_script_name>.py <args>
```

These are current command line availables:

* [createNewService.py](SCRIPTS.md#createnewservicepy)
* [createNewServiceRole.py](SCRIPTS.md#createnewservicerolepy)
* [createNewServiceUser.py](SCRIPTS.md#createnewserviceuserpy)
* [createNewSubService.py](SCRIPTS.md#createnewsubservicepy)
* [printServices.py](SCRIPTS.md#printservicespy)
* [printSubServices.py](SCRIPTS.md#printsubservicespy)
* [printServiceUsers.py](SCRIPTS.md#printserviceuserspy)
* [printServiceRoless.py](SCRIPTS.md#printservicerolespy)
* [printServiceRolePolicies.py](SCRIPTS.md#printservicerolepoliciespy)
* [removeService.py](SCRIPTS.md#removeServicepy)
* [removeSubService.py](SCRIPTS.md#removeSubServicepy)
* [removeServiceRole.py](SCRIPTS.md#removeServiceRolepy)
* [changeUserPassword.py](SCRIPTS.md#changeUserPasswordpy)
* [assignRoleServiceUser.py](SCRIPTS.md#assignroleserviceuserpy)
* [assignRoleSubServiceUser.py](SCRIPTS.md#assignrolesubserviceuserpy)
* [assignInheritRoleServiceUser.py](SCRIPTS.md#assigninheritroleserviceuserpy)
* [listRoleAssignments.py](SCRIPTS.md#listRoleAssignmentspy)
* [unassignInheritRoleServiceUser.py](SCRIPTS.md#unassigninheritroleserviceuserpy)
* [unassignRoleServiceUser.py](SCRIPTS.md#unassignroleserviceuserpy)
* [unassignRoleSubServiceUser.py](SCRIPTS.md#unassignrolesubserviceuserpy)
* [createTrustToken.py](SCRIPTS.md#createtrusttokenpy)
* [printServiceUserTrusts.py](SCRIPTS.md#printserviceusertrustspy)


### createNewService.py
This script creates a new service in IoT keystone
including admin user with role admin, subservice roles
and configures keypass policies for orion and perseo
```
Usage: ./createNewService.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <DOMAIN_NAME>                   Admin Domain name
  <DOMAIN_ADMIN_USER>             Regional Service Provider username
  <DOMAIN_ADMIN_PASSWORD>         Regional Service Provider password
  <NEW_SERVICE_NAME>              New service name
  <NEW_SERVICE_DESCRIPTION>       New service description
  <NEW_SERVICE_ADMIN_USER>        New service admin username
  <NEW_SERVICE_ADMIN_PASSWORD>    New service admin password
  <KEYPASS_PROTOCOL>              HTTP or HTTPS
  <KEYPASS_HOST>                  Keypass (or PEPProxy) HOSTNAME or IP
  <KEYPASS_PORT>                  Keypass (or PEPProxy) PORT

  Typical usage:
     ./createNewService.py http                 \
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
```

### createNewServiceRole.py
This script creates a new role service in IoT keystone
```
Usage: ./createNewServiceRole.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <NEW_ROLE_NAME>                 Name of new role

  Typical usage:
     ./createNewServiceRole.py http             \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 ServiceCustomer\
```

### createNewServiceUser.py
This script creates a new service user in IoT keystone
```
Usage: ./createNewServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <NEW_USER_NAME>                 Name of new user
  <NEW_USER_PASSWORD>             Password of new user

  Typical usage:
     ./createNewServiceUser.py http             \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 Electricidad   \
                                 bob            \
                                 password       \
```

### createNewSubService.py
This script creates a new sub service in IoT keystone
```
Usage: ./createNewSubService.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <NEW_SUBSERVICE_NAME>           New subservice name
  <NEW_SUBSERVICE_DESCRIPTION>    New subservice description

  Typical usage:
     ./createNewSubService.py http              \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 Electricidad   \
                                 electricidad   \
```

### assignRoleServiceUser.py
This script assigns a role to a service user IoT keystone
```
Usage: ./assignRoleServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <ROLE_NAME>                     Name of role
  <SERVICE_USER>                  Service username

  Typical usage:
     ./assignRoleServiceUser.py http            \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 ServiceCustomer\
                                 Carl           \
```

### assignRoleSubServiceUser.py
This script assigns a role to a service user IoT keystone
```
Usage: ./assignRoleSubServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SUBSERVICE_NAME>               SubService name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <ROLE_NAME>                     Name of role
  <SERVICE_USER>                  Service username

  Typical usage:
     ./assignRoleSubServiceUser.py http         \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 Electricidad   \
                                 adm1           \
                                 password       \
                                 ServiceCustomer\
                                 Carl           \
```

### assignInheritRoleServiceUser.py
This script assigns a role to a service user IoT keystone
```
Usage: ./assignInheritRoleServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <SERVICE_USER_NAME>             Service username
  <ROLE_NAME>                     Name of role

  Typical usage:
     ./assignInheritRoleServiceUser.py http     \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 adm1           \
                                 SubServiceAdmin\
```

### printServices.py
This script prints services
```
Usage: ./printServices.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <DOMAIN_NAME>                   Admin Domain name
  <DOMAIN_ADMIN_USER>             Regional Service Provider username
  <DOMAIN_ADMIN_PASSWORD>         Regional Service Provider password

  Typical usage:
     ./printServices.py http                    \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
```

### printSubServices.py
This script prints subservices of service
```
Usage: ./printSubServices.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password

  Typical usage:
     ./printSubServices.py http                 \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
```

### unassignInheritRoleServiceUser.py
This script revoke a role to a service user IoT keystone
```
Usage: ./unassignInheritRoleServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <SERVICE_USER_NAME>             Service username
  <ROLE_NAME>                     Name of role

  Typical usage:
     ./unassignInheritRoleServiceUser.py http   \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 adm1           \
                                 SubServiceAdmin\
```

### unassignRoleServiceUser.py
This script revokes a role to a service user IoT keystone
```
Usage: ./unassignRoleServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <ROLE_NAME>                     Name of role
  <SERVICE_USER>                  Service username

  Typical usage:
     ./unassignRoleServiceUser.py http          \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 ServiceCustomer\
                                 Carl           \
```

### unassignRoleSubServiceUser.py
This script revokes a role to a service user IoT keystone
```
Usage: ./unassignRoleSubServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SUBSERVICE_NAME>               SubService name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <ROLE_NAME>                     Name of role
  <SERVICE_USER>                  Service username

  Typical usage:
     ./unassignRoleSubServiceUser.py http       \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 Electricidad   \
                                 adm1           \
                                 password       \
                                 ServiceCustomer\
                                 Carl           \
```

### createTrustToken.py
This script creates a new Trust Token in IoT keystone
```

Usage: ./src/orchestrator/commands/createTrustToken.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SUBSERVICE_NAME>               SubService name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <ROLE_NAME>                     Name of role
  <TRUSTEE_USER_NAME>             Trustee user name
  <TRUSTOR_USER_NAME>             Trustor user name

  Typical usage:
     ./src/orchestrator/commands/createTrustToken.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 Electricidad   \
                                 adm1           \
                                 password       \
                                 SubServiceAdmin\
                                 pep            \
                                 adm1           \
```

### listRoleAssignments.py
This script prints roles in a service
```
Usage: ./listRoleAssignments.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password

  Typical usage:
     ./listRoleAssignments.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
```

### removeService.py
This script removes a Service (aka keystone domain) in IoT Platform
```
Usage: ./removeService.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <DOMAIN_ADMIN_USER>             Regional Service Provider username
  <DOMAIN_ADMIN_PASSWORD>         Regional Service Provider password
  <KEYPASS_PROTOCOL>              HTTP or HTTPS
  <KEYPASS_HOST>                  Keypass (or PEPProxy) HOSTNAME or IP
  <KEYPASS_PORT>                  Keypass (or PEPProxy) PORT

  Typical usage:
     ./removeService.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValenciaB \
                                 cloud_admin    \
                                 password       \
                                 http           \
                                 localhost      \
                                 8080           \
```

### removeSubService.py
This script removes a SubService (aka keystone domain) in IoT Platform
```
Usage: ./removeSubService.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SUBSERVICE_NAME>               SubService name
  <SERVICE_ADMIN_USER>            Service Admin username
  <SERVICE_ADMIN_PASSWORD>        Service Admin password

  Typical usage:
     ./removeSubService.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
```

### removeSubService.py
This script removes a SubService (aka keystone domain) in IoT Platform
```
Usage: ./removeSubService.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SUBSERVICE_NAME>               SubService name
  <SERVICE_ADMIN_USER>            Service Admin username
  <SERVICE_ADMIN_PASSWORD>        Service Admin password

  Typical usage:
     ./removeSubService.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
```

### changeUserPassword.py
This script changes service user password in IoT keystone
```
Usage: ./changeUserPassword.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <USER_NAME>                     User name
  <NEW_USER_PASSWORD>             New user password

  Typical usage:
     ./changeUserPassword.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 bob            \
                                 new_password   \
```

### printServiceRoles.py
This script prints roles in a service
```
Usage: ./printServiceRoles.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password

  Typical usage:
     ./printServiceRoles.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
```

### printServiceUsers.py
This script prints users in a service
```
Usage: ./printServiceUsers.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password

  Typical usage:
     ./printServiceUsers.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
```

### printServiceUserTrusts.py
This script prints all user trusts in IoT keystone
```
Usage: ./printServiceUserTrusts.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <ROLE_NAME>                     Name of role
  <TRUSTEE_USER_NAME>             Trustee user name

  Typical usage:
     ./printServiceUserTrusts.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 adm1           \
```

### printServiceRolePolicies.py
This script prints service role XACML policies
```
Usage: ./printServiceRolePolicies.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            Service admin username
  <SERVICE_ADMIN_PASSWORD>        Service admin password
  <ROLE_NAME>                     Role name
  <KEYPASS_PROTOCOL>              HTTP or HTTPS
  <KEYPASS_HOST>                  Keypass (or PEPProxy) HOSTNAME or IP
  <KEYPASS_PORT>                  Keypass (or PEPProxy) PORT

  Typical usage:
     ./printServiceRolePolicies.py http         \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 adm1           \
                                 password       \
                                 SubServiceAdmin\
                                 http           \
                                 localhost      \
                                 8080           \
```
