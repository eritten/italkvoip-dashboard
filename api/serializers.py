from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CredentialSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    domain = serializers.CharField()
    display_name = serializers.CharField()
