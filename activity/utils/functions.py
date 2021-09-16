from uuid import uuid4


def comment_slug(instance):
    return f'{instance.user}-comment-{uuid4()}'
