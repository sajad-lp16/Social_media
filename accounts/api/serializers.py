from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()


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
            data['token'] = request.user.oauth2_provider_accesstoken.get_queryset().last().token
        else:
            data.pop('phone_number')
            data.pop('email')
        return data
