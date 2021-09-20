from rest_framework import generics

from .. import models
from . import serializers


class CommentPostListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(post__slug=self.request.data.get('post_slug'))
