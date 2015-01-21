from rest_framework import serializers

class ServiceSerializer(serializers.Serializer):
    KEYSTONE_PROTOCOL=serializers.CharField(max_length=5, required=True)
    KEYSTONE_HOST=serializers.CharField(max_length=20, required=True)
    KEYSTONE_PORT=serializers.IntegerField(required=True)
    DOMAIN_NAME=serializers.CharField(max_length=20, required=True)
    DOMAIN_ADMIN_USER=serializers.CharField(max_length=20, required=True)
    DOMAIN_ADMIN_PASSWORD=serializers.CharField(max_length=20, required=True)
    NEW_SERVICE_NAME=serializers.CharField(max_length=20, required=True)
    NEW_SERVICE_DESCRIPTION=serializers.CharField(max_length=200, required=True)
    NEW_SERVICE_ADMIN_USER=serializers.CharField(max_length=20, required=True)
    NEW_SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=20, required=True)
    KEYPASS_PROTOCOL=serializers.CharField(max_length=5, required=True)
    KEYPASS_HOST=serializers.CharField(max_length=20, required=True)
    KEYPASS_PORT=serializers.IntegerField(required=True)

class ServiceUserSerializer(serializers.Serializer):
    KEYSTONE_PROTOCOL=serializers.CharField(max_length=5, required=True)
    KEYSTONE_HOST=serializers.CharField(max_length=20, required=True)
    KEYSTONE_PORT=serializers.IntegerField(required=True)
    SERVICE_NAME=serializers.CharField(max_length=20, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=20, required=True)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=20, required=True)
    NEW_SERVICE_USER_NAME=serializers.CharField(max_length=20, required=True)
    NEW_SERVICE_USER_PASSWORD=serializers.CharField(max_length=20, required=True)

class ServiceRoleSerializer(serializers.Serializer):
    KEYSTONE_PROTOCOL=serializers.CharField(max_length=5, required=True)
    KEYSTONE_HOST=serializers.CharField(max_length=20, required=True)
    KEYSTONE_PORT=serializers.IntegerField(required=True)
    SERVICE_NAME=serializers.CharField(max_length=20, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=20, required=True)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=20, required=True)
    NEW_ROLE_NAME=serializers.CharField(max_length=20, required=True)

class RoleServiceUserSerializer(serializers.Serializer):
    KEYSTONE_PROTOCOL=serializers.CharField(max_length=5, required=True)
    KEYSTONE_HOST=serializers.CharField(max_length=20, required=True)
    KEYSTONE_PORT=serializers.IntegerField(required=True)
    SERVICE_NAME=serializers.CharField(max_length=20, required=True)
    SERVICE_ADMIN_USER=serializers.CharField(max_length=20, required=True)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=20, required=True)
    ROLE_NAME=serializers.CharField(max_length=20, required=True)
    SERVICE_USER_NAME=serializers.CharField(max_length=20, required=True)

class RoleSubServiceUserSerializer(serializers.Serializer):
    KEYSTONE_PROTOCOL=serializers.CharField(max_length=5, required=True)
    KEYSTONE_HOST=serializers.CharField(max_length=20, required=True)
    KEYSTONE_PORT=serializers.IntegerField(required=True)
    SERVICE_NAME=serializers.CharField(max_length=20, required=True)
    SUBSERVICE_NAME=serializers.CharField(max_length=20, required=True)    
    SERVICE_ADMIN_USER=serializers.CharField(max_length=20, required=True)
    SERVICE_ADMIN_PASSWORD=serializers.CharField(max_length=20, required=True)
    ROLE_NAME=serializers.CharField(max_length=20, required=True)
    SERVICE_USER_NAME=serializers.CharField(max_length=20, required=True)    
    
