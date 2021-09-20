from uuid import uuid4

from rest_framework import status
from rest_framework.response import Response


def comment_slug(instance):
    return f'{instance.user}-comment-{uuid4()}'


def handle_like(obj, serializer, instance, target, action):
    if instance is None:
        action(serializer, target)
        headers = obj.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    instance.delete()
    return Response({'message': 'like has been deleted!'}, status=status.HTTP_204_NO_CONTENT)


def handle_serializer(obj, request):
    serializer = obj.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer
