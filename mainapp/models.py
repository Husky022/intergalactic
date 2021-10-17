from django.db import models
from authapp.models import IntergalacticUser

from .utilities import get_timestamp_path


class Hub(models.Model):
    class Meta:
        verbose_name = 'хаб'
        verbose_name_plural = 'хабы'

    name = models.CharField(max_length=20, db_index=True,
                            verbose_name='Название хаба')
    order = models.SmallIntegerField(
        default=0, db_index=True, verbose_name='Порядок вывода')
    is_active = models.BooleanField('активность', default=True)

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

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['-add_datetime']

    ARTICLE_STATUS_CHOICES = [
        ('DR', 'Черновик'),
        ('MD', 'На модерации'),
        ('PB', 'Опубликована'),
    ]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path)
    article = models.ForeignKey(Article, on_delete=models.PROTECT,
                                verbose_name='Статья')
    author = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                               verbose_name='Автор комментария')
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Активация комментария')
    add_datetime = models.DateTimeField('Время добавления комментария', auto_now_add=True)

    def __str__(self):
        return f'{self.article.name}: {self.text}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
