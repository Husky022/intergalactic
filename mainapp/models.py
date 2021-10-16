from django.conf import settings
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
    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['-add_datetime']

    ARTICLE_STATUS_CHOICES = [
        ('DR', 'Черновик'),
        ('MD', 'На модерации'),
        ('PB', 'Опубликована'),
    ]

    # Пока модерация не включена в настройках - публиковать сразу все написанные статьи
    ARTICLE_DEFAULT_STATUS = 'MD' if settings.MODERATION_STATUS else ARTICLE_DEFAULT_STATUS = 'PB'

    name = models.CharField(verbose_name='Название статьи', max_length=168)
    image = models.ImageField(verbose_name='Изображение для статьи', blank=True, upload_to=get_timestamp_path)
    preview = models.TextField(verbose_name='Предпросмотр', max_length=200)
    text = models.TextField(verbose_name='Текст статьи')
    tag = models.CharField(verbose_name='Тэг статьи', max_length=64, blank=True)
    hub = models.ForeignKey(
        Hub,
        verbose_name='Хаб',
        on_delete=models.PROTECT,
        blank=True
    )
    author = models.ForeignKey(
        IntergalacticUser,
        verbose_name='Автор статьи',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(
        verbose_name='Актуальность статьи',
        default=True,
        db_index=True,
    )
    add_datetime = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True
    )
    article_status = models.CharField(
        verbose_name='Статус публикации',
        choices=ARTICLE_STATUS_CHOICES,
        default=ARTICLE_DEFAULT_STATUS
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_pk = None

    def __str__(self):
        return f'{self.name} - ({self.hub.name})'
