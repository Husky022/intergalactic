from django.db import models

from authapp.models import IntergalacticUser
from mainapp.models import Article


class ArticleMessage(models.Model):
    article = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE)
    message_from = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Сообщение от',
        null=True,
        on_delete=models.SET_NULL
    )
    text = models.TextField(verbose_name='Текст сообщения')
    moderator = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Модератор',
        null=True,
        on_delete=models.SET_NULL,
        related_name='moderator'
    )
    datetime = models.DateTimeField(verbose_name='Дата и время сообщения', auto_now_add=True)
