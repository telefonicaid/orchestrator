## Scenario

####  Servicios
 * ThinkingThings

                     
### SubServicios
 * ThinkingThings\
 * ThinkingThings\user_x


### Roles
 * admin
 * SubServiceAdmin
 * SubServiceCustomer

### Users
```
adm_tt - admin               - ThinkingThings
       - SubServiceAdmin     - ThinkingThings\*

user_x - SubServiceAdmin     - ThinkingThings\user_x
       - SubServiceCustomer  - ThinkingThings\user_x

```

[Provision script](provision_thinkingthings.sh)
