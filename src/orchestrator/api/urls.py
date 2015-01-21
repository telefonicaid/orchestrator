from django.conf.urls import (url, include, patterns)
from django.contrib.auth.decorators import login_required

from orchestrator.api.views import (NewService_RESTView, \
    NewServiceUser_RESTView, \
    NewServiceRole_RESTView,
    AssignRoleServiceUser_RESTView,
    AssignRoleSubServiceUser_RESTView)

urlpatterns = patterns('',
     url(r'^service[/]?$', NewService_RESTView.as_view(), name='new_service_rest_view'),                       
#     # url(r'^subservice[/]?$', login_required(NewSubService_RESTView.as_view()), name='new_subservice_rest_view'),
     url(r'^user[/]?$', NewServiceUser_RESTView.as_view(), name='new_user_rest_view'),
     url(r'^role[/]?$', NewServiceRole_RESTView.as_view(), name='new_role_rest_view'),
     url(r'^assignRoleService[/]?$', AssignRoleServiceUser_RESTView.as_view(), name='assign_role_service_user_rest_view'),
     url(r'^assignRoleSubService[/]?$', AssignRoleSubServiceUser_RESTView.as_view(), name='assign_role_subservice_user_rest_view'),
)
