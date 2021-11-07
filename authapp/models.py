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
    send_to_email = models.BooleanField(
        default=True,
        verbose_name='Уведомления на почту'
    )
    about_me = models.TextField(verbose_name='О себе', blank=True, null=True)

    def __str__(self):
        return f'{self.username}'


class NotificationModel(models.Model):
    recipient = models.ForeignKey(IntergalacticUser, on_delete=models.PROTECT,
                                  verbose_name='Получатель', related_name='recipient')
    sender = models.ForeignKey(IntergalacticUser, on_delete=models.PROTECT,
                               verbose_name='Отправитель', related_name='sender', null=True)
    is_read = models.BooleanField(default=False, db_index=True,
                                  verbose_name='Статус прочтения')
    action = models.TextField(verbose_name='Текст')
    text = models.TextField(verbose_name='Текст', blank=True, null=True)
    target = models.TextField(verbose_name='Цель')
    article_id = models.PositiveIntegerField(
        verbose_name='ID статьи', null=True)
    comment_id = models.PositiveIntegerField(
        verbose_name='ID комментария', null=True)
    subcomment_id = models.PositiveIntegerField(
        verbose_name='ID подкомментария', null=True)
    like_id = models.PositiveIntegerField(verbose_name='ID лайка', null=True)
    complaint_id = models.PositiveIntegerField(
        verbose_name='ID жалобы', null=True)
    add_datetime = models.DateTimeField('Время уведомления', auto_now_add=True)

    def __str__(self):
        return f'Уведомление: {self.text}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
