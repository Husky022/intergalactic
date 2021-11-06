from django.db import models

# Create your models here.
from authapp.models import IntergalacticUser


class UserBalance(models.Model):
    user = models.ForeignKey(IntergalacticUser, related_name='balance_changes')
    amount = models.DecimalField(verbose_name='Баланс', default=0, max_digits=18, decimal_places=6)
    update_datetime = models.DateTimeField('Время обновления баланса', auto_now=True)


class Transaction(models.Model):
    user = models.ForeignKey('User', related_name='balance_changes')
    sender = models.TextField(verbose_name='Отправитель')
    message = models.TextField(verbose_name='Сопроводительное сообщение', blank=True, null=True)
    coins = models.DecimalField(verbose_name='Монеты', default=0, max_digits=18, decimal_places=6)
    datetime = models.DateTimeField('Время транзакции', auto_now_add=True)
