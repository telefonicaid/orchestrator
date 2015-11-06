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
        "name": "Service",
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
            "DOMAIN_ADMIN_USER": [
                "DOMAIN_ADMIN_PASSWORD"
            ],
            "DOMAIN_ADMIN_PASSWORD": [
                "DOMAIN_ADMIN_USER",
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
            "DOMAIN_ID": {
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
                "maxLength": 50,
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "NEW_SUBSERVICE_DESCRIPTION": {
                "type": "string",
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
    "RoleList": {
    #######
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
            "NEW_ROLE_NAME": {
                "type": "string",
                "maxLength": 50,
                "pattern": "^([A-Za-z0-9_]+)$",
            },
            "XACML_POLICY": {
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
            "USER_ID": {
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
            "TRUSTEE_USER__ID": {
                "type": "string",
            },
            "TRUSTOR_USER_NAME": {
                "type": "string",
            },
            "TRUSTOR_USER__ID": {
                "type": "string",
            },
        },
        # "required": [
        # ],
    },

    #############
    "IoTADevice": {
    #############
        "name": "IoTADevice",
        "dependencies": {
            "SERVICE_USER_NAME": [
                "SERVICE_USER_PASSWORD"
            ],
            "SERVICE_USER_PASSWORD": [
                "SERVICE_USER_NAME",
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
            "SERVICE_NAME": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "SUBSERVICE_NAME": {
                "type": "string",
            },
            "DEVICE_ID": {
                "type": "string",
                "pattern": "^[^'\"=;()]*$",
            },
            "ENTITY_TYPE": {
                "type": "string",
                "pattern": "^[^'\"=;()]*$",
            },
            "PROTOCOL": {
                "type": "string",
            },
            "ATT_ICCID": {
                "type": "string",
            },
            "ATT_IMEI": {
                "type": "string",
            },
            "ATT_IMSI": {
                "type": "string",
            },
            "ATT_INTERACTION_TYPE": {
                "type": "string",
                "enum": ["synchronous", "asynchronous"]
            },
            "ATT_SERVICE_ID": {
                "type": "string",
            },
            "ATT_GEOLOCATION": {
                "type": "string",
            },
        },
        "required": [
            "DEVICE_ID",
            # "ENTITY_TYPE",
            # "PROTOCOL"
        ],
    },


    ##############
    "IoTAService": {
    ##############
        "name": "IoTAService",
        "dependencies": {
            "SERVICE_USER_NAME": [
                "SERVICE_USER_PASSWORD"
            ],
            "SERVICE_USER_PASSWORD": [
                "SERVICE_USER_NAME",
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
            "SERVICE_NAME": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "SUBSERVICE_NAME": {
                "type": "string",
            },
            "ENTITY_TYPE": {
                "type": "string",
                "pattern": "^[^'\"=;()]*$",
            },
            "ENTITY_ID": {
                "type": "string",
                "pattern": "^[^'\"=;()]*$",
            },
            "ATT_NAME": {
                "type": "string",
            },
            "ATT_PROVIDER": {
                "type": "string",
            },
            "ATT_ENDPOINT": {
                "type": "string",
            },
            "ATT_METHOD": {
                "type": "string",
            },
            "ATT_AUTHENTICATION": {
                "type": "string",
                "enum": ["context-adapter", "third-party"]
            },
            "ATT_INTERACTION_TYPE": {
                "type": "string",
                "enum": ["synchronous", "asynchronous"]
            },
            "ATT_MAPPING": {
                "type": "string",
            },
            "ATT_TIMEOUT": {
                "type": "integer",
            },

        },
        "required": [
            "ENTITY_TYPE",
            "ENTITY_ID",
            "PROTOCOL",
        ],
    },


    #############
    "IoTADevices": {
    #############
        "name": "IoTADevices",
        "dependencies": {
            "SERVICE_USER_NAME": [
                "SERVICE_USER_PASSWORD"
            ],
            "SERVICE_USER_PASSWORD": [
                "SERVICE_USER_NAME",
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
            "SERVICE_NAME": {
                "type": "string",
            },
            "SUBSERVICE_ID": {
                "type": "string",
            },
            "SUBSERVICE_NAME": {
                "type": "string",
            },
        },
        # "required": [
        # ],
    },

    ##################
    "ModuleActivation": {
    ##################
        "name": "ModuleActivation",
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
            "MODULE": {
                "type": "string",
            },
        },
        # "required": [ ],
    },

}
