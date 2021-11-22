from django.db import models

from authapp.models import IntergalacticUser
from mainapp.models import Article, Comment


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
    moderator = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Модератор',
        null=True,
        on_delete=models.SET_NULL,
        related_name='moderator'
    )
    datetime = models.DateTimeField(
        verbose_name='Дата и время сообщения', auto_now_add=True)


class BlockedUser(models.Model):
    user = models.OneToOneField(
        IntergalacticUser, verbose_name='Пользователь', related_name='blusers', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Причина блокировки', blank=True)
    datetime = models.DateTimeField(verbose_name='Дата и время блокировки', auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class Complaint(models.Model):
    article = models.ForeignKey(
        Article, verbose_name='Статья', null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, null=True, verbose_name='Комментарий', on_delete=models.CASCADE)
    complainant = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Жалоба от',
        null=True,
        on_delete=models.SET_NULL
    )
    text = models.TextField(verbose_name='Текст жалобы')
    datetime = models.DateTimeField(
        verbose_name='Дата и время жалобы', auto_now_add=True)
    is_active = models.BooleanField(
        verbose_name='Актуальность жалобы',
        default=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'жалоба'
        verbose_name_plural = 'жалобы'
        ordering = ['-datetime']


class ComplaintMessage(models.Model):
    complaint = models.ForeignKey(
        Complaint, verbose_name='Жалоба', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, verbose_name='Статья', null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, verbose_name='Комментарий', null=True, on_delete=models.CASCADE)
    message_from = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Сообщение от',
        null=True,
        on_delete=models.SET_NULL
    )
    text = models.TextField(verbose_name='Текст сообщения')
    datetime = models.DateTimeField(
        verbose_name='Дата и время сообщения', auto_now_add=True)
