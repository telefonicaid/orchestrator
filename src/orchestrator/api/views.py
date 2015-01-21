from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, BrowsableAPIRenderer
import logging


from orchestrator.core.flow.createNewService import createNewService
from orchestrator.core.flow.createNewServiceUser import createNewServiceUser
from orchestrator.core.flow.createNewServiceRole import createNewServiceRole
from orchestrator.core.flow.assignRoleServiceUser import assignRoleServiceUser
from orchestrator.core.flow.assignRoleServiceUser import assignRoleSubServiceUser
from orchestrator.api.serializers import (ServiceSerializer, \
    ServiceUserSerializer, \
    ServiceRoleSerializer, \
    RoleServiceUserSerializer, \
    RoleSubServiceUserSerializer) 

# class ServiceBrowsableAPIRenderer(BrowsableAPIRenderer):
#     def get_context(self, *args, **kwargs):
#         context = super(ServiceBrowsableAPIRenderer, self).get_context(*args, **kwargs)
#         context['display_edit_forms'] = True
#         context["post_form"] = ServiceForm
#         return context

#     def get_default_renderer(self, view):
#         return JSONRenderer()

logger = logging.getLogger('orchestrator_api')

class NewService_RESTView(APIView):
    serializer_class = ServiceSerializer
    #renderer_classes = (JSONRenderer, ServiceBrowsableAPIRenderer)

    def post(self, request, *args, **kw):
        serializer = ServiceSerializer(data=request.DATA)
        if serializer.is_valid():
            result = createNewService(request.DATA["KEYSTONE_PROTOCOL"],
                                      request.DATA["KEYSTONE_HOST"],
                                      request.DATA["KEYSTONE_PORT"],
                                      request.DATA["DOMAIN_NAME"],
                                      request.DATA["DOMAIN_ADMIN_USER"],
                                      request.DATA["DOMAIN_ADMIN_PASSWORD"],
                                      request.DATA["NEW_SERVICE_NAME"],
                                      request.DATA["NEW_SERVICE_DESCRIPTION"],
                                      request.DATA["NEW_SERVICE_ADMIN_USER"],
                                      request.DATA["NEW_SERVICE_ADMIN_PASSWORD"],
                                      request.DATA["KEYPASS_PROTOCOL"],
                                      request.DATA["KEYPASS_HOST"],
                                      request.DATA["KEYPASS_PORT"])

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class NewServiceUser_RESTView(APIView):
    serializer_class = ServiceUserSerializer

    def post(self, request, *args, **kw):
        serializer = ServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            result = createNewServiceUser(request.DATA["KEYSTONE_PROTOCOL"],
                                          request.DATA["KEYSTONE_HOST"],
                                          request.DATA["KEYSTONE_PORT"],
                                          request.DATA["SERVICE_NAME"],
                                          request.DATA["SERVICE_ADMIN_USER"],
                                          request.DATA["NEW_SERVICE_USER_NAME"],
                                          request.DATA["NEW_SERVICE_USER_PASSWORD"])

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class NewServiceRole_RESTView(APIView):
    serializer_class = ServiceRoleSerializer

    def post(self, request, *args, **kw):
        serializer = ServiceRoleSerializer(data=request.DATA)
        if serializer.is_valid():
            result = createNewServiceRole(request.DATA["KEYSTONE_PROTOCOL"],
                                          request.DATA["KEYSTONE_HOST"],
                                          request.DATA["KEYSTONE_PORT"],
                                          request.DATA["SERVICE_NAME"],
                                          request.DATA["SERVICE_ADMIN_USER"],
                                          request.DATA["SERVICE_ADMIN_PASSWORD"],
                                          request.DATA["NEW_ROLE_NAME"])

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class AssignRoleServiceUser_RESTView(APIView):
    serializer_class = RoleServiceUserSerializer

    def post(self, request, *args, **kw):
        serializer = RoleServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            result = assignRoleServiceUser(request.DATA["KEYSTONE_PROTOCOL"],
                                           request.DATA["KEYSTONE_HOST"],
                                           request.DATA["KEYSTONE_PORT"],
                                           request.DATA["SERVICE_NAME"],
                                           request.DATA["SERVICE_ADMIN_USER"],
                                           request.DATA["SERVICE_ADMIN_PASSWORD"],
                                           request.DATA["NEW_ROLE_NAME"],
                                           request.DATA["NEW_SERVICE_USER_NAME"])

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class AssignRoleSubServiceUser_RESTView(APIView):
    serializer_class = assignRoleSubServiceUser

    def post(self, request, *args, **kw):
        serializer = RoleSubServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            result = assignRoleSubServiceUser(request.DATA["KEYSTONE_PROTOCOL"],
                                              request.DATA["KEYSTONE_HOST"],
                                              request.DATA["KEYSTONE_PORT"],
                                              request.DATA["SERVICE_NAME"],
                                              request.DATA["SUBSERVICE_NAME"],
                                              request.DATA["SERVICE_ADMIN_USER"],
                                              request.DATA["SERVICE_ADMIN_PASSWORD"],
                                              request.DATA["NEW_ROLE_NAME"],
                                              request.DATA["NEW_SERVICE_USER_NAME"])

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
