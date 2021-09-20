from rest_framework import generics
from rest_framework.generics import get_object_or_404

from . import serializers
from .. import models
from ..utils.functions import handle_like, handle_serializer


class CommentPostListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(post__slug=self.request.data.get('post_slug'))


class CommentLikeListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.LikeCommentSerializer

    def get_queryset(self):
        return models.LikeComment.objects.filter(comment__slug=self.request.data.get('comment_slug'))

    def action(self, serializer, comment):
        serializer.save(user=self.request.user, comment=comment)

    def create(self, request, *args, **kwargs):
        serializer = handle_serializer(self, request)
        comment = get_object_or_404(models.Comment, slug=serializer.validated_data.pop('comment_slug', None))
        instance = models.LikeComment.objects.filter(user=request.user, comment=comment).first()
        return handle_like(self, serializer, instance, comment, self.action)


class PostLikesListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.LikePostSerializer

    def get_queryset(self):
        return models.LikePost.objects.filter(post__slug=self.request.data.get('post_slug'))

    def action(self, serializer, post):
        serializer.save(user=self.request.user, post=post)

    def create(self, request, *args, **kwargs):
        serializer = handle_serializer(self, request)
        post = get_object_or_404(models.Post, slug=serializer.validated_data.pop('post_slug', None))
        instance = models.LikePost.objects.filter(user=request.user, post=post).first()
        return handle_like(self, serializer, instance, post, self.action)


class MessageLikeListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.LikeMessageSerializer

    def get_queryset(self):
        return models.LikeMessage.objects.filter(message__id=self.request.data.pop('message_id', None))

    def action(self, serializer, message):
        serializer.save(user=self.request.user, message=message)

    def create(self, request, *args, **kwargs):
        serializer = handle_serializer(self, request)
        message = get_object_or_404(models.Message, id=serializer.validated_data.get('message_id'))
        instance = models.LikeMessage.objects.filter(user=request.user, message=message).first()
        return handle_like(self, serializer, instance, message, self.action)
