## Scenario

####  Servicios
* tecnoport  TecnoPort 2025

### SubServicios
* tecnoport\cuts
* tecnoport\erio
* tecnoport\fps

### Roles
* admin
* SubServiceAdmin
* SubServiceCustomer
* ServiceCustomer

### Users
```
tecnoport_admin       - admin
                      - SubServiceAdmin\*
tecnoport_cuts_admin  - SubServiceAdmin 
                      - ServiceCustomer 
tecnoport_erio_admin  - SubServiceAdmin              
tecnoport_fps_admin   - SubServiceAdmin

repsol_admin          - admin
                      - SubServiceAdmin 
```
