from django.db import models

from authapp.models import IntergalacticUser


class ButtonsInProfile(models.Model):
    name = models.CharField(verbose_name='название кнопки', max_length=20)
    include_html_file_name = models.CharField(verbose_name='html файл', max_length=100)


class Chat(models.Model):
    user = models.ManyToManyField(IntergalacticUser)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='Чат')
    author = models.ForeignKey(
        IntergalacticUser,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='от пользователя'
    )
    text = models.TextField(verbose_name='Текст сообщения')
    datetime = models.DateTimeField(verbose_name='дата сообщения', auto_now_add=True)
    read = models.BooleanField(verbose_name='Прочитано', default=False)
    was_call = models.BooleanField(default=False)  # Если сообщение отображалось где-либо хотя-бы раз, то True


class NewMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    to_user = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE)
