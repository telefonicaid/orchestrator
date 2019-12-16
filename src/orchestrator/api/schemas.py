#
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of IoT orchestrator
#
# IoT orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# IoT orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with IoT orchestrator. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT team
#

json = {
    ###############
    "ServiceCreate": {
    ###############
        "name": "ServiceCreate",
        "dependencies": {
            "DOMAIN_NAME": [
                "DOMAIN_ADMIN_USER",
                "DOMAIN_ADMIN_PASSWORD"
            ],
            "DOMAIN_ADMIN_USER": [
                "DOMAIN_NAME",
                "DOMAIN_ADMIN_PASSWORD"
            ],
            "DOMAIN_ADMIN_PASSWORD": [
                "DOMAIN_ADMIN_USER",
                "DOMAIN_NAME"
            ]
        },
        "properties": {
            "DOMAIN_NAME": {
                "type": "string",
            },
            "DOMAIN_ADMIN_USER": {
                "type": "string",
            },
            "DOMAIN_ADMIN_PASSWORD": {
                "type": "string",
            },
            "DOMAIN_ADMIN_TOKEN": {
                "type": "string",
            },
            "NEW_SERVICE_NAME": {
                "type": "string",
                "maxLength": 50,
                "pattern": "^([a-z0-9_]+)$",
            },
            "NEW_SERVICE_DESCRIPTION": {
                "type": "string",
            },
            "NEW_SERVICE_ADMIN_USER": {
                "type": "string",
                "maxLength": 50,
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "NEW_SERVICE_ADMIN_PASSWORD": {
                "type": "string",
                "minLength": 6,
            },
            "NEW_SERVICE_ADMIN_EMAIL": {
                "type": "string",
                "pattern": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
            },
        },
        # "oneof": {
        #     "required": [
        #         "NEW_SERVICE_NAME",
        #         "NEW_SERVICE_ADMIN_USER",
        #         "NEW_SERVICE_ADMIN_PASSWORD",
        #         "DOMAIN_ADMIN_USER"],
        #     "required": [
        #         "NEW_SERVICE_NAME",
        #         "NEW_SERVICE_ADMIN_USER",
        #         "NEW_SERVICE_ADMIN_PASSWORD",
        #         "DOMAIN_ADMIN_TOKEN"],
        # }
        "required": [
                "NEW_SERVICE_NAME",
                "NEW_SERVICE_ADMIN_USER",
                "NEW_SERVICE_ADMIN_PASSWORD"
        ]
    },
    #############
    "ServiceList": {
    #############
        "name": "ServiceList",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "DOMAIN_NAME": {
                "type": "string",
            },
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "DOMAIN_ID": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "NEW_SERVICE_DESCRIPTION": {
                "type": "string",
            },
        },
        # "required": [ ],
    },
    ################
    "SubServiceList": {
    ################
        "name": "SubServiceList",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "SUBSERVICE_NAME": {
                "type": "string",
            },
            "NEW_SUBSERVICE_DESCRIPTION": {
                "type": "string",
            },
        },
        # "required": [ ],
    },
    #################
    "SubServiceCreate": {
    #################
        "name": "SubServiceCreate",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "NEW_SUBSERVICE_NAME": {
                "type": "string",
                "maxLength": 64,
                "pattern": "^([A-Za-z0-9_/.:#-]+)$",
            },
            "NEW_SUBSERVICE_DESCRIPTION": {
                "type": "string",
            },
            "NEW_SUBSERVICE_ADMIN_USER": {
                "type": "string",
                "maxLength": 50,
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "NEW_SUBSERVICE_ADMIN_PASSWORD":{
                "type": "string",
                "minLength": 6,
            },
            "NEW_SUBSERVICE_ADMIN_EMAIL":{
                "type": "string",
                "pattern": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
            },
        },
        "required": [
            "NEW_SUBSERVICE_NAME"
        ],
    },
    #######
    "User": {
    #######
        "name": "User",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "USER_NAME": {
                "type": "string",
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "USER_ID": {
                "type": "string",
            },
            "USER_DATA_VALUE": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "pattern": "^([A-Za-z0-9_]+)$",
                        },
                    "userName": {
                        "type": "string",
                        "pattern": "^([A-Za-z0-9_]+)$",
                        },
                    "password": {
                        "type": "string",
                        "minLength": 6,
                        },
                    "displayName": {
                        "type": "string",
                        },
                    "description": {
                        "type": "string",
                        },
                    "emails": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "pattern": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
                                    },
                                }
                            },
                        "maxItems": 4
                        },
                    },
                "additionalProperties": False,
                # "required": ["user", "emails"]
            },
            "NEW_USER_PASSWORD":{
                "type": "string",
                "minLength": 6,
            },
        },
        # "required": [ ],
    },
    ##########
    "UserList": {
    ##########
        "name": "UserList",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ],
            "NEW_SERVICE_USER_NAME": [
                "NEW_SERVICE_USER_PASSWORD"
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "NEW_SERVICE_USER_NAME": {
                "type": "string",
                "maxLength": 50,
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "NEW_SERVICE_USER_PASSWORD":{
                "type": "string",
                "minLength": 6,
            },
            "NEW_SERVICE_USER_EMAIL":{
                "type": "string",
                "pattern": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
            },
        },
        # "required": [ ],
    },
    #######
    "Group": {
    #######
        "name": "Group",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "GROUP_NAME": {
                "type": "string",
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "GROUP_ID": {
                "type": "string",
            },
        },
        # "required": [ ],
    },
    ##########
    "GroupList": {
    ##########
        "name": "GroupList",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ],
            "NEW_SERVICE_USER_NAME": [
                "NEW_SERVICE_USER_PASSWORD"
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "NEW_SERVICE_GROUP_NAME": {
                "type": "string",
                "maxLength": 50,
                "pattern": "^([A-Za-z0-9_]+)$",
            },
        },
        # "required": [ ],
    },
    ###########
    "RoleList": {
    ###########
        "name": "RoleList",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "NEW_ROLE_NAME": {
                "type": "string",
                "maxLength": 50,
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "XACML_POLICY": {
                "type": "string",
            },
        },
        "required": [
            "NEW_ROLE_NAME"
        ],
    },
    #######
    "Role": {
    #######
        "name": "Role",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "ROLE_NAME": {
                "type": "string",
            },
            "ROLE_ID": {
                "type": "string",
            },
            "POLICY_FILE_NAME": {
                "type": "string",
            },
        },
    },
    ####################
    "RoleAssignmentList": {
    ####################
        "name": "RoleAssignmentList",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "SUBSERVICE_NAME": {
                "type": "string",
            },
            "USER_ID": {
                "type": "string",
            },
            "USER_NAME": {
                "type": "string",
            },
        },
    },
    #############
    "AssignRole": {
    #############
        "name": "AssignRole",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "SERVICE_USER_NAME": {
                "type": "string",
            },
            "SERVICE_USER_ID": {
                "type": "string",
            },
            "SUBSERVICE_NAME": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "ROLE_NAME": {
                "type": "string",
            },
            "ROLE_ID": {
                "type": "string",
            },
        },
        "required": [
            "ROLE_NAME",
            "SERVICE_USER_NAME"
        ],
    },

    ########
    "Trust": {
    ########
        "name": "Trust",
        "dependencies": {
            "SERVICE_ADMIN_USER": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_ADMIN_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_ADMIN_USER": {
                "type": "string",
            },
            "SERVICE_ADMIN_PASSWORD": {
                "type": "string",
            },
            "SERVICE_ADMIN_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SERVICE_NAME": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "SUBSERVICE_NAME": {
                "type": "string",
            },
            "ROLE_NAME": {
                "type": "string",
            },
            "ROLE_ID": {
                "type": "string",
            },
            "TRUSTEE_USER_NAME": {
                "type": "string",
            },
            "TRUSTEE_USER_ID": {
                "type": "string",
            },
            "TRUSTOR_USER_NAME": {
                "type": "string",
            },
            "TRUSTOR_USER_ID": {
                "type": "string",
            },
        },
        # "required": [
        # ],
    },

    #####################
    "IOTModuleActivation": {
    #####################
        "name": "IOTModuleActivation",
        "dependencies": {
            "SERVICE_USER_NAME": [
                "SERVICE_ADMIN_PASSWORD"
            ],
            "SERVICE_USER_PASSWORD": [
                "SERVICE_ADMIN_USER",
            ]
        },
        "properties": {
            "SERVICE_USER_NAME": {
                "type": "string",
            },
            "SERVICE_USER_PASSWORD": {
                "type": "string",
            },
            "SERVICE_USER_TOKEN": {
                "type": "string",
            },
            "SERVICE_ID": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "IOTMODULE": {
                "type": "string",
            },
        },
        # "required": [ ],
    },
    #######
    "LdapUser": {
    #######
        "name": "LdapUser",
        "dependencies": {
            "LDAP_ADMIN_USER": [
                "LDAP_ADMIN_PASSWORD"
            ],
            "LDAP_ADMIN_PASSWORD": [
                "LDAP_ADMIN_USER"
            ],
            "NEW_USER_PASSWORD": [
                "NEW_USER_NAME"
            ],
            "USER_PASSWORD": [
                "USER_NAME"
            ],
        },
        "properties": {
            "LDAP_ADMIN_USER": {
                "type": "string",
            },
            "LDAP_ADMIN_PASSWORD": {
                "type": "string",
            },
            "USER_NAME": {
                "type": "string",
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "USER_PASSWORD": {
                "type": "string",
            },
            "NEW_USER_NAME": {
                "type": "string",
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "NEW_USER_PASSWORD":{
                "type": "string",
                "minLength": 6,
            },
            "NEW_USER_EMAIL": {
                "type": "string",
                "pattern": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
            },
            "NEW_USER_DESCRIPTION": {
                "type": "string"
            },
            "GROUP_NAMES": {
                "type": "array",
                "items": {
                    "type": "string",
                    "properties": {
                        "value": {
                            "type": "string",
                            "pattern": "^([A-Za-z0-9_]+)$"
                        }
                    },
                    "maxItems": 8
                }
            },
            "USER_DATA": {
                "type": "object",
                "properties": {
                    "USER_PASSWORD": {
                        "type": "string",
                        "minLength": 6,
                        },
                    "USER_DESCRIPTION": {
                        "type": "string",
                        },
                    "USER_EMAIL": {
                        "type": "string",
                        "pattern": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
                        },
                    "GROUP_NAMES": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "pattern": "^([A-Za-z0-9_]+)$"
                                    }
                                },
                            "maxItems": 8
                            }
                        }
                    },
                "additionalProperties": False,
            }
        }
        # "required": [ ],
    },
    #######
    "LdapGroup": {
    #######
        "name": "LdapGroup",
        "dependencies": {
            "LDAP_ADMIN_USER": [
                "LDAP_ADMIN_PASSWORD"
            ],
            "LDAP_ADMIN_PASSWORD": [
                "LDAP_ADMIN_USER"
            ]
        },
        "properties": {
            "LDAP_ADMIN_USER": {
                "type": "string",
            },
            "LDAP_ADMIN_PASSWORD": {
                "type": "string",
            },
            "GROUP_NAME": {
                "type": "string",
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "NEW_GROUP_NAME": {
                "type": "string",
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "NEW_GROUP_DESCRIPTION": {
                "type": "string"
            },
        }
        # "required": [ ],
}
