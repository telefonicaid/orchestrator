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
tecnoport_admin       - admin               - tecnoport
                      - SubServiceAdmin    - tecnoport\*
tecnoport_cuts_admin  - SubServiceAdmin     - tecnoport\cuts
                      - ServiceCustomer     - tecnoport\cuts
tecnoport_erio_admin  - SubServiceAdmin     - tecnoport\erio
tecnoport_fps_admin   - SubServiceAdmin     - tecnoport\fps

```

[Provision script](provision_tecnoport.sh)
