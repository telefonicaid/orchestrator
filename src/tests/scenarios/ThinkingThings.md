## Scenario

####  Servicios
 * thinkingthings

                     
### SubServicios
 * thinkingthings\
 * thinkingthings\user_x


### Roles
 * admin
 * SubServiceAdmin
 * SubServiceCustomer

### Users
```
adm_tt - admin               - thinkingthings
       - SubServiceAdmin     - thinkingthings\*

user_x - SubServiceAdmin     - thinkingthings\user_x
       - SubServiceCustomer  - thinkingthings\user_x

```

[Provision script](provision_thinkingthings.sh)
