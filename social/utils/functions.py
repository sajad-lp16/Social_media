from uuid import uuid4

from utils.functions import get_format


def post_slug(instance):
    return f'{instance.user}-post-{uuid4()}'


def rename_file(instance, file_name):
    ext = get_format(file_name)
    return f'media/{instance.user}/{instance.user}{ext}'
