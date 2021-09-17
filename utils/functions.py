import os


def get_format(filename):
    _, ext = os.path.splitext(filename)
    return ext
