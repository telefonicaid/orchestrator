from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, BrowsableAPIRenderer
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


from orchestrator.core.flow.createNewService import createNewService
from orchestrator.core.flow.createNewServiceUser import createNewServiceUser
from orchestrator.core.flow.createNewServiceRole import createNewServiceRole
from orchestrator.core.flow.assignRoleServiceUser import assignRoleServiceUser
from orchestrator.core.flow.assignRoleSubServiceUser import assignRoleSubServiceUser
from orchestrator.core.flow.removeUser import removeUser
from orchestrator.core.flow.updateUser import updateUser

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

# TOOD: extract Keystone/Keypass from django settings instead of API

class IoTConf(object):

    def __init__(self):
        try:
            self.KEYSTONE_PROTOCOL = settings.KEYSTONE['protocol']
            self.KEYSTONE_HOST = settings.KEYSTONE['host']
            self.KEYSTONE_PORT = settings.KEYSTONE['port']

            self.KEYPASS_PROTOCOL = settings.KEYPASS['protocol']
            self.KEYPASS_HOST = settings.KEYPASS['host']
            self.KEYPASS_PORT = settings.KEYPASS['port']
            
        except KeyError:
            raise ImproperlyConfigured("keystone or keypass conf")
            



class NewService_RESTView(APIView, IoTConf):
    serializer_class = ServiceSerializer
    #renderer_classes = (JSONRenderer, ServiceBrowsableAPIRenderer)

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, *args, **kw):
        serializer = ServiceSerializer(data=request.DATA)
        if serializer.is_valid():
            result = createNewService(self.KEYSTONE_PROTOCOL,
                                      self.KEYSTONE_HOST,
                                      self.KEYSTONE_PORT,
                                      request.data["DOMAIN_NAME"],
                                      request.DATA["DOMAIN_ADMIN_USER"],
                                      request.DATA["DOMAIN_ADMIN_PASSWORD"],
                                      request.DATA["NEW_SERVICE_NAME"],
                                      request.DATA["NEW_SERVICE_DESCRIPTION"],
                                      request.DATA["NEW_SERVICE_ADMIN_USER"],
                                      request.DATA["NEW_SERVICE_ADMIN_PASSWORD"],
                                      self.KEYPASS_PROTOCOL,
                                      self.KEYPASS_HOST,
                                      self.KEYPASS_PORT)

            if 'token' in result:
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                # TODO: return status from result error code
                #status=status.HTTP_404_NOT_FOUND)
                return Response(result['error'],
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class NewServiceUser_RESTView(APIView, IoTConf):
    serializer_class = ServiceUserSerializer

    def __init__(self):
        IoTConf.__init__(self)
    
    def post(self, request, *args, **kw):
        serializer = ServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            result = createNewServiceUser(self.KEYSTONE_PROTOCOL,
                                          self.KEYSTONE_HOST,
                                          self.KEYSTONE_PORT,
                                          request.DATA["SERVICE_NAME"],
                                          request.DATA["SERVICE_ADMIN_USER"],
                                          request.DATA["SERVICE_ADMIN_PASSWORD"],
                                          request.DATA["NEW_SERVICE_USER_NAME"],
                                          request.DATA["NEW_SERVICE_USER_PASSWORD"])
            if 'id' in result:
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                # TODO: return status from result error code
                #status=status.HTTP_404_NOT_FOUND)
                return Response(result['error'],
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kw):
        # TODO:
        import ipdb
        ipdb.set_trace()
        if True:
            result = removeUser(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                request.DATA["SERVICE_NAME"],
                                request.DATA["SERVICE_ADMIN_USER"],
                                request.DATA["SERVICE_ADMIN_PASSWORD"],
                                request.DATA["USER_NAME"])
            
            return Response(result, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kw):
        # TODO: use a form to validate
        import ipdb
        ipdb.set_trace()
        if True:
            result = updateUser(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT,
                                request.DATA["SERVICE_NAME"],
                                request.DATA["SERVICE_ADMIN_USER"],
                                request.DATA["SERVICE_ADMIN_PASSWORD"],
                                request.DATA["USER_NAME"],
                                request.DATA["USER_DATA_VALUE"],)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(None,
                        status=status.HTTP_400_BAD_REQUEST)
            
class NewServiceRole_RESTView(APIView, IoTConf):
    serializer_class = ServiceRoleSerializer

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, *args, **kw):
        serializer = ServiceRoleSerializer(data=request.DATA)
        if serializer.is_valid():
            result = createNewServiceRole(self.KEYSTONE_PROTOCOL,
                                          self.KEYSTONE_HOST,
                                          self.KEYSTONE_PORT,
                                          request.DATA["SERVICE_NAME"],
                                          request.DATA["SERVICE_ADMIN_USER"],
                                          request.DATA["SERVICE_ADMIN_PASSWORD"],
                                          request.DATA["NEW_ROLE_NAME"])

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class AssignRoleServiceUser_RESTView(APIView, IoTConf):
    serializer_class = RoleServiceUserSerializer

    def __init__(self):
        IoTConf.__init__(self)
        
    def post(self, request, *args, **kw):
        serializer = RoleServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            result = assignRoleServiceUser(self.KEYSTONE_PROTOCOL,
                                           self.KEYSTONE_HOST,
                                           self.KEYSTONE_PORT,
                                           request.DATA["SERVICE_NAME"],
                                           request.DATA["SERVICE_ADMIN_USER"],
                                           request.DATA["SERVICE_ADMIN_PASSWORD"],
                                           request.DATA["NEW_ROLE_NAME"],
                                           request.DATA["NEW_SERVICE_USER_NAME"])

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class AssignRoleSubServiceUser_RESTView(APIView, IoTConf):
    serializer_class = assignRoleSubServiceUser

    def __init__(self):
        IoTConf.__init__(self)
    
    def post(self, request, *args, **kw):
        serializer = RoleSubServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            result = assignRoleSubServiceUser(self.KEYSTONE_PROTOCOL,
                                              self.KEYSTONE_HOST,
                                              self.KEYSTONE_PORT,
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
