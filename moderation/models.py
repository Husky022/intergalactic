from django.db import models

from authapp.models import IntergalacticUser
from mainapp.models import Article


class ArticleMessage(models.Model):
    article = models.ForeignKey(
        Article, verbose_name='Статья', on_delete=models.CASCADE)
    message_from = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Сообщение от',
        null=True,
        on_delete=models.SET_NULL
    )
    text = models.TextField(verbose_name='Текст сообщения')
    datetime = models.DateTimeField(
        verbose_name='Дата и время сообщения', auto_now_add=True)


class Complaint(models.Model):
    article = models.ForeignKey(
        Article, verbose_name='Статья', on_delete=models.CASCADE)
    complainant = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Жалоба от',
        null=True,
        on_delete=models.SET_NULL
    )
    text = models.TextField(verbose_name='Текст жалобы')
    datetime = models.DateTimeField(
        verbose_name='Дата и время жалобы')
    is_active = models.BooleanField(
        verbose_name='Актуальность жалобы',
        default=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'жалоба'
        verbose_name_plural = 'жалобы'
