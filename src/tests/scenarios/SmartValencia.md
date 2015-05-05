## Scenario

####  Servicios
 * SmartValencia

                     
### SubServicios
 * SmartValencia\Electricidad
 * SmartValencia\Basuras


### Roles
 * admin
 * SubServiceAdmin
 * SubServiceCustomer
 * ServiceCustomer


### Users
```
adm1   - admin               - SmartValencia
       - SubServiceAdmin     - SmartValencia\*

Alice  - SubServiceAdmin     - SmartValencia\Electricidad

bob    - SubServiceCustomer  - SmartValencia\Electricidad
       - SubServiceAdmin     - SmartValencia\Basuras

Carl   - ServiceCustomer     - SmartValencia
       - SubServiceCustomer  - SmartValencia\*
```
[Provision script](provision_smartvalencia.sh)
[Provision script](provision_smartcityvalencia.sh)
