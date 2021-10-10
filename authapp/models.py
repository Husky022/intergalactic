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
        blank=True
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

    # class Meta(AbstractUser.Meta):
    #     pass

    def __str__(self):
        return f'{self.username}'
