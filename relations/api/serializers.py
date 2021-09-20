from django.contrib.auth import get_user_model

from rest_framework import serializers
from accounts.api.serializers import UserSerializer

User = get_user_model()

from .. import models


class RelationSerializer(serializers.ModelSerializer):
    start_user = serializers.StringRelatedField(read_only=True)
    end_user = serializers.StringRelatedField(read_only=True)
    target = serializers.CharField(write_only=True)

    class Meta:
        model = models.Relation
        fields = (
            'start_user',
            'end_user',
            'target'
        )
