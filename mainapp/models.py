from os import name
from django.db import models
from authapp.models import IntergalacticUser
from django.utils import timezone


from .utilities import get_timestamp_path


class Hub(models.Model):
    name = models.CharField(max_length=20, db_index=True,
                            verbose_name='Название хаба')
    order = models.SmallIntegerField(
        default=0, db_index=True, verbose_name='Порядок вывода')
    is_active = models.BooleanField('активность', default=True)

    class Meta:
        verbose_name = 'хаб'
        verbose_name_plural = 'хабы'

    def __str__(self):
        return f'{self.name}'


class Article(models.Model):
    name = models.CharField('имя', max_length=64)
    image = models.ImageField(blank=True, upload_to=get_timestamp_path)
    text = models.TextField(verbose_name='Текст статьи')
    tag = models.CharField('тэг статьи', max_length=64, blank=True)
    hub = models.ForeignKey(Hub, on_delete=models.PROTECT,
                            verbose_name='Хаб', blank=True)
    author = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                               verbose_name='Автор статьи')
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Актуальность статьи')
    add_datetime = models.DateTimeField('время добавления', auto_now_add=True)
    from_summernote = models.BooleanField('Самописная статья', blank=True, null=True)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['-add_datetime']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_pk = None

    def __str__(self):
        return f'{self.name} - ({self.hub.name})'
