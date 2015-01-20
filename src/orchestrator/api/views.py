from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, BrowsableAPIRenderer

from orchestrator.core.flow.createNewService import createNewServiceKeystone
from orchestrator.api.serializers import ServiceSerializer

# class ServiceBrowsableAPIRenderer(BrowsableAPIRenderer):
#     def get_context(self, *args, **kwargs):
#         context = super(ServiceBrowsableAPIRenderer, self).get_context(*args, **kwargs)
#         context['display_edit_forms'] = True
#         context["post_form"] = ServiceForm
#         return context

#     def get_default_renderer(self, view):
#         return JSONRenderer()


class NewService_RESTView(APIView):
    serializer_class = ServiceSerializer
    #renderer_classes = (JSONRenderer, ServiceBrowsableAPIRenderer)
 
    def post(self, request, *args, **kw):
        serializer = ServiceSerializer(data=request.DATA)
        if serializer.is_valid():
            result = createNewServiceKeystone(request.DATA["KEYSTONE_PROTOCOL"],
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
