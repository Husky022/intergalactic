from django.db import models
from django.contrib.auth.models import AbstractUser


class IntergalacticUser(AbstractUser):
    sex_male = 'male'
    sex_female = 'female'
    sex_not_selected = 'not selected'
    sex_choices = (
        (sex_male, 'мужской'),
        (sex_female, 'женский'),
        (sex_not_selected, 'не выбран'),
    )
    avatar = models.ImageField(
        verbose_name='Аватарка',
        upload_to='avatars',
        blank=True
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='возраст',
        blank=True,
        null=True
    )
    sex = models.CharField(
        verbose_name='пол',
        max_length=12,
        choices=sex_choices,
        default=sex_not_selected
    )
    send_messages = models.BooleanField(
        default=True,
        verbose_name='Оповещать о новых комментариях'
    )
    about_me = models.TextField(verbose_name='О себе', blank=True, null=True)

    def __str__(self):
        return f'{self.username}'


class Notification(models.Model):
    recipient = models.ForeignKey(IntergalacticUser, on_delete=models.PROTECT,
                                verbose_name='Получатель')
    is_read = models.BooleanField(
        default=False, db_index=True, verbose_name='Активация комментария')
    text = models.TextField(verbose_name='Текст уведомления')
    add_datetime = models.DateTimeField('Время уведомления', auto_now_add=True)

    def __str__(self):
        return f'Уведомление: {self.text}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'