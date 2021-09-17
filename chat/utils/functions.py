from utils.functions import get_format


def chat_room_slug(instance):
    return f'chat-room-{instance.start_user}-{instance.end_user}'


def rename_file(instance, file_name):
    ext = get_format(file_name)
    return f'messages/{instance.user}-{instance.chat_room.end_user}/{instance.user}{ext}'
