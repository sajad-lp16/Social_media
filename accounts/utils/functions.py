from utils.functions import get_format


def rename_file(instance, file_name):
    ext = get_format(file_name)
    return f'profiles/{instance.username}{ext}'
