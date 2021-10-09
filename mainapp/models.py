from os import name
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import IntegerField

from .utilities import get_timestamp_path


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(
        default=True, verbose_name='Слать оповещения о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return f'{self.username}'


class Hab(models.Model):
    name = models.CharField(max_length=20, db_index=True,
                            verbose_name='Название хаба')
    order = models.SmallIntegerField(
        default=0, db_index=True, verbose_name='Порядок вывода')

    class Meta:
        verbose_name = 'хаб'
        verbose_name_plural = 'хабы'

    def __str__(self):
        return f'{self.name}'


class ArticlesCategory(models.Model):
    name = models.CharField('категория статьи', max_length=64)
    is_active = models.BooleanField('активность', default=True)

    class Meta:
        verbose_name = 'категория статьи'
        verbose_name_plural = 'категории статей'

    def __str__(self):
        return f'Категория {self.name}'

    def delete(self, using=None, keep_parents=False):

        self.is_active = False
        self.save()
        return 1, {}


class Article(models.Model):
    category = models.ForeignKey(ArticlesCategory, on_delete=models.CASCADE)
    name = models.CharField('имя', max_length=64)
    image = models.ImageField(blank=True, upload_to=get_timestamp_path)
    text = models.TextField(verbose_name='Текст статьи')
    tag = models.CharField('тэг статьи', max_length=64, blank=True)
    hab = models.ForeignKey(Hab, on_delete=models.PROTECT, verbose_name='Хаб', blank=True)
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name='Автор статьи')
    add_datatime = models.DateField('время добавления', auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Актуальность статьи')

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_pk = None

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
        return 1, {}
