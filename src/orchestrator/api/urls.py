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
                                    )


urlpatterns = patterns('',
     url(r'^service[/]?$', ServiceCreate_RESTView.as_view(), name='new_service_rest_view'),
     url(r'^service/(?P<service_id>\w+)[/]?$', ServiceList_RESTView.as_view(), name='service_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice[/]?$', SubServiceCreate_RESTView.as_view(), name='new_subservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice/(?P<subservice_id>\w+)?$', SubServiceList_RESTView.as_view(), name='subservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/user[/]?$', UserList_RESTView.as_view(), name='new_user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/user/(?P<user_id>\w+)?$', User_RESTView.as_view(), name='user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role[/]?$', RoleList_RESTView.as_view(), name='new_role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role/(?P<role_id>\w+)?$', Role_RESTView.as_view(), name='role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role_assignments[/]?$', AssignRoleUser_RESTView.as_view(), name='assign_role_rest_view'),
)
