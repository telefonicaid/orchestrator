from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, BrowsableAPIRenderer
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


from orchestrator.core.flow.createNewService import CreateNewService
from orchestrator.core.flow.createNewSubService import CreateNewSubService
from orchestrator.core.flow.createNewServiceUser import CreateNewServiceUser
from orchestrator.core.flow.createNewServiceRole import CreateNewServiceRole
from orchestrator.core.flow.assignRoleServiceUser import AssignRoleServiceUser
from orchestrator.core.flow.assignRoleSubServiceUser import AssignRoleSubServiceUser
from orchestrator.core.flow.removeUser import RemoveUser
from orchestrator.core.flow.updateUser import UpdateUser
from orchestrator.core.flow.Domains import Domains
from orchestrator.core.flow.Projects import Projects
from orchestrator.core.flow.Roles import Roles
from orchestrator.core.flow.Users import Users

from orchestrator.api.serializers import (ServiceSerializer, \
    SubServiceSerializer, \
    ServiceUserSerializer, \
    ServiceUserDeleteSerializer, \
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



class ServiceList_RESTView(APIView, IoTConf):
    """
    Lists of modifies and existent service

    """
    #renderer_classes = (JSONRenderer, ServiceBrowsableAPIRenderer)

    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id=None):
        # TODO: check params with a serializer?
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        flow = Domains(self.KEYSTONE_PROTOCOL,
                                self.KEYSTONE_HOST,
                                self.KEYSTONE_PORT)
        if not service_id:
            result = flow.domains(request.DATA.get("DOMAIN_NAME", None),
                                  request.DATA.get("SERVICE_ADMIN_USER", None),
                                  request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                  request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))
        else:
            # TODO: return detail of domain_id: name, etc
            result = flow.get_domain(request.DATA.get("DOMAIN_ID", service_id),
                                     request.DATA.get("SERVICE_ADMIN_USER", None),
                                     request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                     request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))

        if not 'error' in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            # TODO: return status from result error code
            #status=status.HTTP_404_NOT_FOUND)
            return Response(result['error'],
                            status=status.HTTP_400_BAD_REQUEST)


class ServiceCreate_RESTView(ServiceList_RESTView):
    """
    Creates a new service

    """
    serializer_class = ServiceSerializer

    def __init__(self):
        ServiceList_RESTView.__init__(self)

    def post(self, request, *args, **kw):
        serializer = ServiceSerializer(data=request.DATA)
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)

        if serializer.is_valid():

            cs = CreateNewService(self.KEYSTONE_PROTOCOL,
                                  self.KEYSTONE_HOST,
                                  self.KEYSTONE_PORT,
                                  self.KEYPASS_PROTOCOL,
                                  self.KEYPASS_HOST,
                                  self.KEYPASS_PORT)

            result = cs.createNewService(request.DATA.get("DOMAIN_NAME", None),
                                         request.DATA.get("DOMAIN_ADMIN_USER", None), 
                                         request.DATA.get("DOMAIN_ADMIN_PASSWORD", None),
                                         request.DATA.get("DOMAIN_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN), 
                                         request.DATA.get("NEW_SERVICE_NAME"),
                                         request.DATA.get("NEW_SERVICE_DESCRIPTION"),
                                         request.DATA.get("NEW_SERVICE_ADMIN_USER"),
                                         request.DATA.get("NEW_SERVICE_ADMIN_PASSWORD"))

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



class SubServiceList_RESTView(APIView, IoTConf):
    """
    Modifies a SubService
    """
    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id=None, subservice_id=None):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        # TODO: check params with a serializer?: service_id, subservice_id
        flow = Projects(self.KEYSTONE_PROTOCOL,
                        self.KEYSTONE_HOST,
                        self.KEYSTONE_PORT)
        if service_id:
            if not subservice_id:
                result = flow.projects(service_id,
                                   request.DATA.get("SERVICE_ADMIN_USER", None),
                                   request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                   request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))
            else:
                # TODO: get detail of subservice
                result = flow.get_project(
                                   request.DATA.get("SERVICE_ID", service_id),
                                   request.DATA.get("SUBSERVICE_ID", subservice_id),
                                   request.DATA.get("SERVICE_ADMIN_USER", None),
                                   request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                   request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))
        else:
            result['error'] = "ERROR not service_id provided"

        if not 'error' in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            # TODO: return status from result error code
            #status=status.HTTP_404_NOT_FOUND)
            return Response(result['error'],
                            status=status.HTTP_400_BAD_REQUEST)

class SubServiceCreate_RESTView(SubServiceList_RESTView):
    """
    Creates a new SubService into a Service
    """
    serializer_class = SubServiceSerializer

    def __init__(self):
        SubServiceList_RESTView.__init__(self)

    def post(self, request, service_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        # TODO: check domain_id also!
        serializer = SubServiceSerializer(data=request.DATA)
        if serializer.is_valid():
            flow = CreateNewSubService(self.KEYSTONE_PROTOCOL,
                                       self.KEYSTONE_HOST,
                                       self.KEYSTONE_PORT)
            # service_id -> SERVICE_NAME
            result = flow.createNewSubService(request.DATA.get("SERVICE_NAME", None),
                                              request.DATA.get("SERVICE_ADMIN_USER", None),
                                              request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                              request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                                              request.DATA.get("NEW_SUBSERVICE_NAME", None),
                                              request.DATA.get("NEW_SUBSERVICE_DESCRIPTION",None))

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




class User_RESTView(APIView, IoTConf):
    """
    Modifies an Users of a Service

    """
    serializer_class = ServiceUserSerializer

    def __init__(self):
        IoTConf.__init__(self)

    def delete(self, request, service_id, user_id):
        #serializer = ServiceUserDeleteSerializer(data=request.DATA)
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        if True: #serializer.is_valid():
            flow = RemoveUser(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)
            result = flow.removeUser(
                                request.DATA.get("SERVICE_NAME", None),
                                request.DATA.get("SERVICE_ADMIN_USER", None),
                                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                                request.DATA.get("USER_NAME", None))

            return Response(result, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, service_id, user_id):
        # TODO: use a form to validate
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        if True:
            # TODO: el usuario se edita a si mismo? NO
            flow = UpdateUser(self.KEYSTONE_PROTOCOL,
                            self.KEYSTONE_HOST,
                            self.KEYSTONE_PORT)
            result = flow.updateUser(
                                request.DATA.get("SERVICE_NAME"), 
                                request.DATA.get("SERVICE_ID", service_id),
                                request.DATA.get("SERVICE_ADMIN_USER", None),
                                request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                                request.DATA.get("USER_NAME"),
                                request.DATA.get("USER_ID", user_id),
                                request.DATA.get("USER_DATA_VALUE"))
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(None,
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, service_id, user_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        flow = Users(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)

        result = flow.user( service_id,
                            user_id,
                            request.DATA.get("SERVICE_ADMIN_USER", None),
                            request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                            request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))
        print result
        if not 'error' in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            # TODO: return status from result error code
            #status=status.HTTP_404_NOT_FOUND)
            return Response(result['error'],
                            status=status.HTTP_400_BAD_REQUEST)


class UserList_RESTView(APIView, IoTConf):
    """
    Return a list of Users of a Service

    """
    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        flow = Users(self.KEYSTONE_PROTOCOL,
                              self.KEYSTONE_HOST,
                              self.KEYSTONE_PORT)

        result = flow.users(service_id,
                            request.DATA.get("SERVICE_ADMIN_USER", None),
                            request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                            request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))

        if not 'error' in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            # TODO: return status from result error code
            #status=status.HTTP_404_NOT_FOUND)
            return Response(result['error'],
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, service_id):
        serializer = ServiceUserSerializer(data=request.DATA)
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        if serializer.is_valid():
            flow = CreateNewServiceUser(self.KEYSTONE_PROTOCOL,
                                      self.KEYSTONE_HOST,
                                      self.KEYSTONE_PORT)
            result = flow.createNewServiceUser(request.DATA.get("SERVICE_NAME", None),
                                             request.DATA.get("SERVICE_ADMIN_USER", None),
                                             request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                             request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                                             request.DATA.get("NEW_SERVICE_USER_NAME", None),
                                             request.DATA.get("NEW_SERVICE_USER_PASSWORD", None))
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

            
class Role_RESTView(APIView, IoTConf):
    serializer_class = ServiceRoleSerializer

    def __init__(self):
        IoTConf.__init__(self)

    def post(self, request, service_id):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        serializer = ServiceRoleSerializer(data=request.DATA)
        if serializer.is_valid():
            flow = CreateNewServiceRole(self.KEYSTONE_PROTOCOL,
                                      self.KEYSTONE_HOST,
                                      self.KEYSTONE_PORT)
            result = flow.createNewServiceRole(
                                          request.DATA.get("SERVICE_NAME"),
                                          request.DATA.get("SERVICE_ADMIN_USER", None),
                                          request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                          request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                                          request.DATA.get("NEW_ROLE_NAME"))

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, service_id=None):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        # TODO: check params with a serializer
        flow = Roles(self.KEYSTONE_PROTOCOL,
                     self.KEYSTONE_HOST,
                     self.KEYSTONE_PORT)
        # get DOMAIN_ID from  url param

        result = flow.roles(service_id,
                            request.DATA.get("SERVICE_ADMIN_USER", None),
                            request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                            request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))

        if not 'error' in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            # TODO: return status from result error code
            #status=status.HTTP_404_NOT_FOUND)
            return Response(result['error'],
                            status=status.HTTP_400_BAD_REQUEST)

class AssignRoleUser_RESTView(APIView, IoTConf):
    def __init__(self):
        IoTConf.__init__(self)

    def get(self, request, service_id):
        user_id = request.GET.get('user_id', None)
        project_id = request.GET.get('project_id', None)
        role_id = request.GET.get('role_id', None)

        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        flow = Roles(self.KEYSTONE_PROTOCOL,
                     self.KEYSTONE_HOST,
                     self.KEYSTONE_PORT)
        # get DOMAIN_ID from  url param

        result = flow.roles_assignments(
                            request.DATA.get("SERVICE_ID", service_id),
                            request.DATA.get("SUBSERVICE_ID", project_id),
                            request.DATA.get("ROLE_ID", role_id),
                            request.DATA.get("USER_ID", user_id),
                            request.DATA.get("SERVICE_ADMIN_USER", None),
                            request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                            request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN))

        if not 'error' in result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            # TODO: return status from result error code
            #status=status.HTTP_404_NOT_FOUND)
            return Response(result['error'],
                            status=status.HTTP_400_BAD_REQUEST)

class AssignRoleServiceUser_RESTView(AssignRoleUser_RESTView):
    serializer_class = RoleServiceUserSerializer

    def __init__(self):
        AssignRoleUser_RESTView.__init__(self)

    def post(self, request, *args, **kw):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        serializer = RoleServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            flow = AssignRoleServiceUser(self.KEYSTONE_PROTOCOL,
                                       self.KEYSTONE_HOST,
                                       self.KEYSTONE_PORT)
            result = flow.assignRoleServiceUser(
                                           request.DATA.get("SERVICE_NAME"),
                                           request.DATA.get("SERVICE_ADMIN_USER", None),
                                           request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                           request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                                           request.DATA.get("NEW_ROLE_NAME"),
                                           request.DATA.get("NEW_SERVICE_USER_NAME"))

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class AssignRoleSubServiceUser_RESTView(AssignRoleUser_RESTView):
    serializer_class = RoleSubServiceUserSerializer

    def __init__(self):
        AssignRoleUser_RESTView.__init__(self)

    def post(self, request, *args, **kw):
        HTTP_X_AUTH_TOKEN = request.META.get('HTTP_X_AUTH_TOKEN', None)
        serializer = RoleSubServiceUserSerializer(data=request.DATA)
        if serializer.is_valid():
            flow = AssignRoleSubServiceUser(self.KEYSTONE_PROTOCOL,
                                          self.KEYSTONE_HOST,
                                          self.KEYSTONE_PORT)
            result = flow.assignRoleSubServiceUser(
                                              request.DATA.get("SERVICE_NAME"),
                                              request.DATA.get("SUBSERVICE_NAME"),
                                              request.DATA.get("SERVICE_ADMIN_USER", None),
                                              request.DATA.get("SERVICE_ADMIN_PASSWORD", None),
                                              request.DATA.get("SERVICE_ADMIN_TOKEN", HTTP_X_AUTH_TOKEN),
                                              request.DATA.get("NEW_ROLE_NAME"),
                                              request.DATA.get("NEW_SERVICE_USER_NAME"))

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


