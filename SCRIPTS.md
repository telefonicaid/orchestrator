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
* [assignRoleServiceUser.py](SCRIPTS.md#assignroleserviceuserpy)
* [assignRoleSubServiceUser.py](SCRIPTS.md#assignrolesubserviceuserpy)
* [assignInheritRoleServiceUser.py](SCRIPTS.md#assigninheritroleserviceuserpy)
* [printServices.py](SCRIPTS.md#printservicespy)
* [printSubServices.py](SCRIPTS.md#printsubservicespy)
* [unassignInheritRoleServiceUser.py](SCRIPTS.md#unassigninheritroleserviceuserpy)
* [unassignRoleServiceUser.py](SCRIPTS.md#unassignroleserviceuserpy)
* [unassignRoleSubServiceUser.py](SCRIPTS.md#unassignrolesubserviceuserpy)



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
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
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
This script creates a new service in IoT keystone
including admin user with role admin, subservice roles
and configures keypass policies for orion and perseo
```
Usage: ./createNewServiceUser.py [args]
Args:
  <KEYSTONE_PROTOCOL>             HTTP or HTTPS
  <KEYSTONE_HOST>                 Keystone HOSTNAME or IP
  <KEYSTONE_PORT>                 Keystone PORT
  <SERVICE_NAME>                  Service name
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
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
This script creates a new service in IoT keystone
including admin user with role admin, subservice roles
and configures keypass policies for orion and perseo
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
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
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
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
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
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
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
     ./printServices.py http           \
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
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
  <SERVICE_USER_NAME>             Service username
  <ROLE_NAME>                     Name of role

  Typical usage:
     ./unassignInheritRoleServiceUser.py http           \
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
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
  <ROLE_NAME>                     Name of role
  <SERVICE_USER>                  Service username

  Typical usage:
     ./unassignRoleServiceUser.py http           \
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
  <SERVICE_ADMIN_USER>            New service admin username
  <SERVICE_ADMIN_PASSWORD>        New service admin password
  <ROLE_NAME>                     Name of role
  <SERVICE_USER>                  Service username

  Typical usage:
     ./unassignRoleSubServiceUser.py http           \
                                 localhost      \
                                 5000           \
                                 SmartValencia  \
                                 Electricidad   \
                                 adm1           \
                                 password       \
                                 ServiceCustomer\
                                 Carl           \
```
