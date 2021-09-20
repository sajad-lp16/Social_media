from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .. import models


class MediaSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post_slug = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = models.Media
        fields = (
            'user',
            'post_slug',
            'media',
            'slug'
        )

    def get_post_slug(self, obj):
        return obj.post.slug

    def create(self, validated_data):
        post = get_object_or_404(models.Post, slug=validated_data.pop('slug'))
        instance = models.Media.objects.create(post=post, **validated_data)
        return instance


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = (
            'user',
            'caption',
            'slug',
            'media'
        )

        extra_kwargs = {
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        instance = models.Post.objects.create(user=request.user, **validated_data)
        return instance
