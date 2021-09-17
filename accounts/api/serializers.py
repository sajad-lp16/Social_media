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
            'avatar',
        )

        extra_kwargs = {
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
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
