# Orchestrator Tests:


- [Unit Tests](./src/tests/core/test_idm.py)
Run unit tests with:
```
        $ python3 ./test_idm.py
```


- [End2End Tests](./src/tests/api/test_api.py)
Run e2e tests with:

```
        $ python3 ./test_api.py
```

- [End2End LDAP Tests](./src/tests/api/test_ldap_api.py)
Run e2e LDAP tests with:

```
        $ python3 ./test_ldap_api.py
```

- [Comamnd Tests](./src/tests/api/test_commands.py)
Run scripts tests with:

```
        $ python3 ./test_commands.py
```

There is a config file to run Orchestrator build into Travis CI service:
[Travis conf file](.travis.yml)
