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
                                    Role_RESTView,
                                    RoleList_RESTView,
                                    AssignRoleUser_RESTView,
                                    Trust_RESTView,
                                    SubServiceDevice_RESTView,
                                    )


urlpatterns = patterns('',
     url(r'^service[/]?$', ServiceCreate_RESTView.as_view(), name='new_service_rest_view'),
     url(r'^service/(?P<service_id>\w+)[/]?$', ServiceList_RESTView.as_view(), name='service_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice[/]?$', SubServiceCreate_RESTView.as_view(), name='new_subservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)?$', SubServiceList_RESTView.as_view(), name='subservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)/register_device[/]?$', SubServiceDevice_RESTView.as_view(), name='subservicedevice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/user[/]?$', UserList_RESTView.as_view(), name='new_user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/user/(?P<user_id>\w+)?$', User_RESTView.as_view(), name='user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role[/]?$', RoleList_RESTView.as_view(), name='new_role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role/(?P<role_id>\w+)?$', Role_RESTView.as_view(), name='role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role_assignments[/]?$', AssignRoleUser_RESTView.as_view(), name='assign_role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/trust[/]?$', Trust_RESTView.as_view(), name='new_trust_rest_view'),
)
