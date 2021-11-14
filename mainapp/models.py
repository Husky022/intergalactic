from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from authapp.models import IntergalacticUser

from userprofile.models import ButtonsInProfile
from .utilities import get_timestamp_path


class Hub(models.Model):
    class Meta:
        verbose_name = 'хаб'
        verbose_name_plural = 'хабы'

    name = models.CharField(max_length=20, db_index=True, verbose_name='Название хаба')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок вывода')
    is_active = models.BooleanField('активность', default=True)

    def __str__(self):
        return f'{self.name}'


class ArticleStatus(models.Model):
    short_name = models.CharField(verbose_name='Краткое название', max_length=2)
    name = models.CharField(verbose_name='Название статуса', max_length=50)
    name_plural = models.CharField(verbose_name='Название раздела в ЛК (мн.число)', max_length=50)
    buttons = models.ManyToManyField(ButtonsInProfile, verbose_name='Кнопки для этого статуса в ЛК',
                                     related_name='кнопки')


class Article(models.Model):
    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['-add_datetime']

    ARTICLE_STATUS_CHOICES = [
        ('DR', 'Черновик'),
        ('MD', 'На модерации'),
        ('RC', 'Требует исправления'),
        ('PB', 'Опубликована'),
        ('AR', 'В архиве'),
        ('AB', 'Заблокированна')
    ]

    # Пока модерация не включена в настройках - публиковать сразу все написанные статьи
    ARTICLE_DEFAULT_STATUS = 'DR' if settings.MODERATION_STATUS else 'PB'

    name = models.CharField(verbose_name='Название статьи', max_length=168)
    image = models.ImageField(verbose_name='Изображение для статьи', blank=True, upload_to=get_timestamp_path)
    preview = models.TextField(verbose_name='Предпросмотр', max_length=250)
    text = models.TextField(verbose_name='Текст статьи')

    tag = models.CharField(verbose_name='Тэг статьи', max_length=64, blank=True)
    hub = models.ForeignKey(Hub, verbose_name='Хаб', on_delete=models.PROTECT, blank=True)
    author = models.ForeignKey(IntergalacticUser, verbose_name='Автор статьи',
                               on_delete=models.CASCADE, null=True, blank=True, )
    is_active = models.BooleanField(verbose_name='Актуальность статьи', default=True, db_index=True)
    add_datetime = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    article_status_new = models.ForeignKey(ArticleStatus, verbose_name='Статус публикации (новый)',
                                           null=True, on_delete=models.SET_NULL, )

    # Activity block
    count_like = models.IntegerField(default=0, verbose_name='количество лайков')
    count_dislike = models.IntegerField(default=0, verbose_name='количество дизлайков')
    status_like_dislike = models.CharField(max_length=8, default="UND", verbose_name='рейтинг')
    count_comment = models.IntegerField(default=0, verbose_name='количество комментариев')
    views = models.IntegerField(default=0, verbose_name='количество просмотров')
    rating = models.IntegerField(default=0, verbose_name='рейтинг')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_pk = None

    def __str__(self):
        return f'{self.name} - ({self.hub.name})'


class Comment(MPTTModel):
    text = models.TextField(verbose_name='Текст комментария')
    parent = TreeForeignKey("self", on_delete=CASCADE, blank=True, null=True, related_name='children')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path)
    article = models.ForeignKey(Article, on_delete=models.PROTECT,
                                verbose_name='Статья')
    author = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                               verbose_name='Автор комментария')
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Активация комментария')
    add_datetime = models.DateTimeField(
        'Время добавления комментария', auto_now_add=True)

    def __str__(self):
        return f'{self.article.name}: {self.text}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class Likes(models.Model):
    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'

    LIKE_STATUS_CHOICES = [
        ('DZ', 'Дизлайк'),
        ('UND', 'Не установлено'),
        ('LK', 'Лайк'),
    ]
    LIKE_DEFAULT_STATUS = 'UND'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус лайка статьи', max_length=3,
                              choices=LIKE_STATUS_CHOICES, default=LIKE_DEFAULT_STATUS)

    def __str__(self):
        data_str = f'Пользователь {self.user.last_name} {self.user.first_name} '
        if self.status:
            data_str += f'установил лайк к статье - \"{self.article.name}\"'
        else:
            data_str += f'снял лайк к статье - \"{self.article.name}\"'
        return data_str


class Visits(models.Model):
    """Визиты пользователей для просмотра"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.CharField(max_length=32, verbose_name='Имя посетителя')
    host = models.CharField(max_length=32, verbose_name='IP посетителя')


class VoiceArticle(models.Model):
    """Аудио текст"""
    audio_file = models.FileField(upload_to="audio")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Sorting(models.Model):
    SORTING_TYPE_CHOICES = [
        ('NEWEST', 'По дате сначала новые'),
        ('ELDEST', 'По дате сначала старые'),
        ('LK_MORE', 'По лайкам сначала больше'),
        ('LK_LESS', 'По лайкам сначала меньше'),
        ('COM_MORE', 'По комментариям сначала больше'),
        ('COM_LESS', 'По комментариям сначала меньше'),
    ]

    user = models.OneToOneField(IntergalacticUser, on_delete=models.CASCADE, unique=True)
    sorting_type = models.CharField(verbose_name='Тип сортировки статей', max_length=8,
                                    choices=SORTING_TYPE_CHOICES, default='NEWEST')

    def __str__(self):
        return f'{self.user} - {self.sorting_type}'


class Recommendations(models.Model):
    """Рекомендации статей для просмотра"""
    user = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров статей')

    def __str__(self):
        return f'статья: {self.article.id}, хаб: {self.article.hub}, просмотры: {self.view_count}'

