from django.db import models

# Create your models here.
from authapp.models import IntergalacticUser


class UserBalance(models.Model):
    user = models.ForeignKey(IntergalacticUser, related_name='Пользователь', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    amount = models.DecimalField(verbose_name='Баланс', default=0, max_digits=18, decimal_places=2)
    update_datetime = models.DateTimeField('Время обновления баланса', auto_now=True)


class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('DONE', 'Выполнена'),
        ('CANCELLED', 'Отменена'),
    ]
    TRANSACTION_DEFAULT_STATUS = 'REG'

    to_user = models.ForeignKey(IntergalacticUser, related_name='Получатель', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус лайка статьи', max_length=9,
                              choices=TRANSACTION_STATUS_CHOICES, default=TRANSACTION_DEFAULT_STATUS)
    sender = models.TextField(verbose_name='Отправитель')
    message = models.TextField(verbose_name='Сопроводительное сообщение', blank=True, null=True)
    coins = models.DecimalField(verbose_name='Монеты', default=0, max_digits=18, decimal_places=2)
    is_read = models.BooleanField(default=False, db_index=True, verbose_name='Статус прочтения')
    datetime = models.DateTimeField('Время транзакции', auto_now_add=True)
