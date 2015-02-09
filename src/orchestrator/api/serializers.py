from rest_framework import serializers

class ServiceSerializer(serializers.Serializer):
    DOMAIN_NAME=serializers.CharField(max_length=25, required=False)
    DOMAIN_ADMIN_USER=serializers.CharField(max_length=25, required=False)
    DOMAIN_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=False)
    DOMAIN_ADMIN_TOKEN=serializers.CharField(max_length=100, required=False)
    NEW_SERVICE_NAME=serializers.CharField(max_length=25, required=True)
    NEW_SERVICE_DESCRIPTION=serializers.CharField(max_length=250, required=False)
    NEW_SERVICE_ADMIN_USER=serializers.CharField(max_length=25, required=True)
    NEW_SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=True)

class SubServiceSerializer(serializers.Serializer):
    SERVICE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_TOKEN=serializers.CharField(max_length=100, required=False)
    NEW_SUBSERVICE_NAME=serializers.CharField(max_length=25, required=True)
    NEW_SUBSERVICE_DESCRIPTION=serializers.CharField(max_length=250, required=False)
    
class ServiceUserSerializer(serializers.Serializer):
    SERVICE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_TOKEN=serializers.CharField(max_length=100, required=False)
    NEW_SERVICE_USER_NAME=serializers.CharField(max_length=25, required=True)
    NEW_SERVICE_USER_PASSWORD=serializers.CharField(max_length=25, required=True)
    NEW_SERICE_USER_EMAIL=serializers.EmailField(required=False)

class ServiceUserDeleteSerializer(serializers.Serializer):
    SERVICE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_TOKEN=serializers.CharField(max_length=100, required=False)
    NEW_SERVICE_USER_NAME=serializers.CharField(max_length=25, required=True)

class ServiceRoleSerializer(serializers.Serializer):
    SERVICE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_TOKEN=serializers.CharField(max_length=100, required=False)
    NEW_ROLE_NAME=serializers.CharField(max_length=25, required=True)

class RoleServiceUserSerializer(serializers.Serializer):
    SERVICE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_TOKEN=serializers.CharField(max_length=100, required=False)
    ROLE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_USER_NAME=serializers.CharField(max_length=25, required=True)

class RoleSubServiceUserSerializer(serializers.Serializer):
    SERVICE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=25, required=False)
    SERVICE_ADMIN_TOKEN=serializers.CharField(max_length=100, required=False)
    SUBSERVICE_NAME=serializers.CharField(max_length=25, required=True)    
    ROLE_NAME=serializers.CharField(max_length=25, required=True)
    SERVICE_USER_NAME=serializers.CharField(max_length=25, required=True)    
    

# TODO: passwrod should be strong
# import cracklib
# cracklib.VeryFascistCheck(password)
