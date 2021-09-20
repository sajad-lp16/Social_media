from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .. import models
from chat.api.serializers import MessageSerializer
from social.api.serializers import PostSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = PostSerializer(read_only=True)

    post_slug = serializers.SlugField(write_only=True)

    reply_to = serializers.SerializerMethodField(read_only=True)
    reply_to_slug = serializers.SlugField(write_only=True, required=False)

    class Meta:
        model = models.Comment
        fields = (
            'user',
            'content',
            'slug',
            'post_slug',
            'post',
            'reply_to',
            'reply_to_slug',
        )

    def create(self, validated_data):
        request = self.context['request']
        reply_to = validated_data.pop('reply_to_slug', None)
        post = get_object_or_404(models.Post, slug=validated_data.pop('post_slug'))

        if reply_to is None:
            return models.Comment.objects.create(user=request.user, post=post, **validated_data)
        reply_to_comment = get_object_or_404(models.Comment, slug=reply_to)
        return models.Comment.objects.create(user=request.user, post=post, reply_to=reply_to_comment, **validated_data)

    def get_reply_to(self, obj):
        if obj.reply_to is not None:
            return obj.reply_to.slug


class LikeCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comment = CommentSerializer(read_only=True)

    comment_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = models.LikeComment
        fields = (
            'user',
            'comment',
            'comment_slug'
        )


class LikeMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    message = serializers.StringRelatedField(read_only=True)

    message_id = serializers.CharField(write_only=True)

    class Meta:
        model = models.LikeMessage
        fields = (
            'user',
            'message',
            'message_id',
        )


class LikePostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = PostSerializer(read_only=True)

    post_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = models.LikePost
        fields = (
            'user',
            'post',
            'post_slug',
        )
