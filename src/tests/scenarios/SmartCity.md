## Scenario

####  Servicios
 * smartcity

                     
### SubServicios
 * smartcity\Electricidad
 * smartcity\Basuras


### Roles
 * admin
 * SubServiceAdmin
 * SubServiceCustomer
 * ServiceCustomer


### Users
```
adm1   - admin               - smartcity
       - SubServiceAdmin     - smartcity\*

Alice  - SubServiceAdmin     - smartcity\Electricidad

bob    - SubServiceCustomer  - smartcity\Electricidad
       - SubServiceAdmin     - smartcity\Basuras

Carl   - ServiceCustomer     - smartcity
       - SubServiceCustomer  - smartcity\*
```
[Provision script](provision_smartcity.sh)
