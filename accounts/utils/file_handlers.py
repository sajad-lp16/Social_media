import os


def get_format(filename):
    _, ext = os.path.splitext(filename)
    return ext


def rename_file(instance, file_name):
    ext = get_format(file_name)
    return f'profiles/{instance.username}{ext}'
