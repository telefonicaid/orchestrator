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
from django.conf.urls import (url, include, patterns)
from django.contrib.auth.decorators import login_required

from orchestrator.api.views import (ServiceList_RESTView,
                                    ServiceCreate_RESTView,
                                    SubServiceList_RESTView,
                                    SubServiceCreate_RESTView,
                                    User_RESTView,
                                    UserList_RESTView,
                                    Group_RESTView,
                                    GroupList_RESTView,
                                    Role_RESTView,
                                    RolePolicy_RESTView,
                                    RoleList_RESTView,
                                    AssignRoleUser_RESTView,
                                    Trust_RESTView,
                                    SubServiceIoTADevice_RESTView,
                                    SubServiceIoTADevices_RESTView,
                                    SubServiceIoTAService_RESTView,
                                    IOTModuleActivation_RESTView,
                                    OrchVersion_RESTView,
                                    OrchLogLevel_RESTView,
                                    OrchMetrics_RESTView
                                    )
from orchestrator.api.ldap_view import (LdapUser_RESTView,
                                        LdapAuth_RESTView)


urlpatterns = patterns('',
     url(r'^service[/]?$', ServiceCreate_RESTView.as_view(), name='new_service_rest_view'),
     url(r'^service/(?P<service_id>\w+)[/]?$', ServiceList_RESTView.as_view(), name='service_rest_view'),
     url(r'^service/(?P<service_id>\w+)/module_activation[/]?$', IOTModuleActivation_RESTView.as_view(), name='servicemodule_rest_view'),
     url(r'^service/(?P<service_id>\w+)/module_activation/(?P<iot_module>\w+)$', IOTModuleActivation_RESTView.as_view(), name='servicemodule_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice[/]?$', SubServiceCreate_RESTView.as_view(), name='new_subservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)?$', SubServiceList_RESTView.as_view(), name='subservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)/register_device[/]?$', SubServiceIoTADevice_RESTView.as_view(), name='subserviceiotadevice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)/register_devices[/]?$', SubServiceIoTADevices_RESTView.as_view(), name='subserviceiotadevices_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)/register_service[/]?$', SubServiceIoTAService_RESTView.as_view(), name='subserviceiotaservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)/module_activation[/]?$', IOTModuleActivation_RESTView.as_view(), name='subservicemodule_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)/module_activation/(?P<iot_module>\w+)$', IOTModuleActivation_RESTView.as_view(), name='subservicemodule_rest_view'),
     url(r'^service/(?P<service_id>\w+)/user[/]?$', UserList_RESTView.as_view(), name='new_user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/user/(?P<user_id>\w+)?$', User_RESTView.as_view(), name='user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/group[/]?$', GroupList_RESTView.as_view(), name='new_group_rest_view'),
     url(r'^service/(?P<service_id>\w+)/group/(?P<group_id>\w+)?$', Group_RESTView.as_view(), name='group_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role[/]?$', RoleList_RESTView.as_view(), name='new_role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role/(?P<role_id>\w+)?$', Role_RESTView.as_view(), name='role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role/(?P<role_id>\w+)/policy/(?P<policy_id>\w+)?$', RolePolicy_RESTView.as_view(), name='role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role_assignments[/]?$', AssignRoleUser_RESTView.as_view(), name='assign_role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/trust[/]?$', Trust_RESTView.as_view(), name='new_trust_rest_view'),
     url(r'^version[/]?$', OrchVersion_RESTView.as_view(), name='orch_version_rest_view'),
     url(r'^admin/log?$', OrchLogLevel_RESTView.as_view(), name='orch_loglevel_rest_view'),
     url(r'^admin/metrics?$', OrchMetrics_RESTView.as_view(), name='orch_metrics_rest_view'),
     url(r'^ldap/user?$', LdapUser_RESTView.as_view(), name='ldap_user_rest_view'),
     url(r'^ldap/auth?$', LdapAuth_RESTView.as_view(), name='ldap_auth_rest_view'),
)
