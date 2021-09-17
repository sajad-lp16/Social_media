import json
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()

CLIENT_ID = '03pUssR1v7l5BdTcDQkgmN9jVs70nMU5AO7c2AGE'
GRANT_TYPE = 'password'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'phone_number',
            'bio',
            'is_active',
            'is_staff',
            'is_private',
            'is_verified',
            'avatar',
        )

        extra_kwargs = {
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'is_verified': {'read_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        data = {
            'username': validated_data['username'],
            'password': password,
            'client_id': CLIENT_ID,
            'grant_type': GRANT_TYPE
        }
        requests.post('http://localhost:8000/oauth/token/', data=json.dumps(data))
        return instance

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password is not None:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context['request']
        data = super().to_representation(instance)
        if request.user == instance or request.user.is_superuser:
            data['token'] = instance.oauth2_provider_accesstoken.get_queryset()[0].token
        else:
            data.pop('phone_number')
            data.pop('email')
        return data
