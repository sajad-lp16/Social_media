import os
from uuid import uuid4


def post_slug(instance):
    return f'{instance.user}-post-{uuid4()}'


def get_format(filename):
    _, ext = os.path.splitext(filename)
    return ext


def rename_file(instance, file_name):
    ext = get_format(file_name)
    return f'media/{instance.user}/{instance.user}{ext}'
