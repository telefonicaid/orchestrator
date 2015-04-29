## Scenario

####  Servicios
 * SmartCity

                     
### SubServicios
 * SmartCity\Electricidad
 * SmartCity\Basuras


### Roles
 * admin
 * SubServiceAdmin
 * SubServiceCustomer
 * ServiceCustomer


### Users
```
adm1   - admin               - SmartCity
       - SubServiceAdmin     - SmartCity\*

Alice  - SubServiceAdmin     - SmartCity\Electricidad

bob    - SubServiceCustomer  - SmartCity\Electricidad
       - SubServiceAdmin     - SmartCity\Basuras

Carl   - ServiceCustomer     - SmartCity
       - SubServiceCustomer  - SmartCity\*
```
[Provision script](provision_smartcity.sh)
