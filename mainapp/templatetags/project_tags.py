import os

from django import template
from django.conf import settings

from intergalactic.settings import BASE_DIR

register = template.Library()


@register.filter(name='media_folder_users')
def media_folder_users(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    """
    if not string:
        return '/static/img/default_avatar.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_article')
def media_folder_article(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    """
    if not os.path.exists(f'{BASE_DIR}{settings.MEDIA_URL}{string}'):
        return "/media/1634827090.305732.png"
    elif not string:
        return "/media/1634827090.305732.png"
    return f'{settings.MEDIA_URL}{string}'
