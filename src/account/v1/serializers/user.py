from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=64, allow_null=True, allow_blank=True)
    phone = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(max_length=64, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=64, allow_null=True, allow_blank=True)
    email = serializers.EmailField(required=True, max_length=65)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance
