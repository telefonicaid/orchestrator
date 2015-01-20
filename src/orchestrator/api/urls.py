from django.conf.urls import (url, include, patterns)
from django.contrib.auth.decorators import login_required

from orchestrator.api.views import NewService_RESTView 

urlpatterns = patterns('',
     url(r'^service[/]?$', NewService_RESTView.as_view(), name='new_service_rest_view'),                       
#     # url(r'^subservice[/]?$', login_required(NewSubService_RESTView.as_view()), name='new_subservice_rest_view'),
#     # url(r'^user[/]?$', login_required(NewUser_RESTView.as_view()), name='new_user_rest_view'),
#     # url(r'^role[/]?$', login_required(NewRole_RESTView.as_view()), name='new_role_rest_view'),
)
