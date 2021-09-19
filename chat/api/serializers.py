from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .. import models

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    conversation = serializers.SerializerMethodField(read_only=True)
    conversation_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = models.Message
        fields = (
            'user',
            'content',
            'media',
            'conversation',
            'conversation_slug',
        )

    def get_conversation(self, obj):
        return obj.__str__()

    def create(self, validated_data):
        slug = validated_data.pop('conversation_slug')
        user = self.context['request'].user
        conversation = get_object_or_404(models.Conversation, slug=slug)
        instance = models.Message.objects.create(
            conversation=conversation, user=user, **validated_data
        )
        return instance


class ConversationSerializer(serializers.ModelSerializer):
    start_user = serializers.StringRelatedField()
    end_user = serializers.StringRelatedField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = models.Conversation
        fields = (
            'start_user',
            'end_user',
            'messages'
        )

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('-create_time')
        return MessageSerializer(messages, many=True).data


class ConversationListSerializer(serializers.ModelSerializer):
    contact = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Conversation
        fields = (
            'contact',
            'slug'
        )

    def get_contact(self, obj):
        request = self.context['request']
        if request.user == obj.start_user:
            return obj.end_user.__str__()
        return obj.start_user.__str__()
