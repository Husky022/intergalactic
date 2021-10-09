from os import name
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import IntegerField

from .utilities import get_timestamp_path

# Create your models here.


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(
        default=True, verbose_name='Слать оповещения о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass


class Hab(models.Model):
    name = models.CharField(max_length=20, db_index=True,
                            ValueError='Название хаба')
    order = models.SmallIntegerField(
        default=0, db_index=True, verbose_name='Порядок вывода')


class Article(models.Model):
    hab = models.ForeignKey(Hab, on_delete=models.PROTECT, verbose_name='Хаб')
    title = models.CharField(max_length=99, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Текст статьи')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name='Автор статьи')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path)
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Актуальность статьи')
