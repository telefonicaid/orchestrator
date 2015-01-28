from django.conf.urls import (url, include, patterns)
from django.contrib.auth.decorators import login_required

from orchestrator.api.views import (Service_RESTView, 
                                    SubService_RESTView, 
                                    User_RESTView,
                                    Role_RESTView,
                                    AssignRoleServiceUser_RESTView,
                                    AssignRoleSubServiceUser_RESTView,
                                    # Users_RESTView,
                                    # Domains_RESTView,
                                    # Projects_RESTView,
                                    # Roles_RESTView
                                    )


urlpatterns = patterns('',
     url(r'^service[/]?$', Service_RESTView.as_view(), name='new_service_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice[/]?$', SubService_RESTView.as_view(), name='subservice_rest_view'),
     url(r'^service/(?P<service_id>\w+)/subservice[/](?P<subservice_id>\w+)?$', SubService_RESTView.as_view(), name='list-subservice_rest_view'),                       
     url(r'^service/(?P<service_id>\w+)/user[/]?$', User_RESTView.as_view(), name='user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role[/]?$', Role_RESTView.as_view(), name='role_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role-assignRoleService[/]?$', AssignRoleServiceUser_RESTView.as_view(), name='assign_role_service_user_rest_view'),
     url(r'^service/(?P<service_id>\w+)/role-assignRoleSubService[/]?$', AssignRoleSubServiceUser_RESTView.as_view(), name='assign_role_subservice_user_rest_view'),
    # TO DO: IoT Portal nomenclature (domain, project)

)
