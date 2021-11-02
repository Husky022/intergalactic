from django.conf import settings
from django.contrib.auth import get_user_model
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


class ButtonsInProfile(models.Model):
    name = models.CharField(verbose_name='название кнопки', max_length=20)
    include_html_file_name = models.CharField(verbose_name='html файл', max_length=100)


class ArticleStatus(models.Model):
    short_name = models.CharField(verbose_name='Краткое название', max_length=2)
    name = models.CharField(verbose_name='Название статуса', max_length=50)
    name_plural = models.CharField(verbose_name='Название раздела в ЛК (мн.число)', max_length=50)
    buttons = models.ManyToManyField(ButtonsInProfile, verbose_name='Кнопки для этого статуса в ЛК')


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
    ]

    # Пока модерация не включена в настройках - публиковать сразу все написанные статьи
    ARTICLE_DEFAULT_STATUS = 'DR' if settings.MODERATION_STATUS else 'PB'

    name = models.CharField(verbose_name='Название статьи', max_length=168)
    image = models.ImageField(
        verbose_name='Изображение для статьи', blank=True, upload_to=get_timestamp_path)
    preview = models.TextField(verbose_name='Предпросмотр', max_length=250)
    text = models.TextField(verbose_name='Текст статьи')
    text_audio = models.TextField(blank=True, verbose_name='Текст аудио')
    tag = models.CharField(verbose_name='Тэг статьи',
                           max_length=64, blank=True)
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
        null=True,
        blank=True,
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
        max_length=2,
        choices=ARTICLE_STATUS_CHOICES,
        default=ARTICLE_DEFAULT_STATUS
    )
    article_status_new = models.ForeignKey(
        ArticleStatus,
        verbose_name='Статус публикации (новый)',
        null=True,
        on_delete=models.SET_NULL,
    )
    views = models.IntegerField(default=0, verbose_name='просмотры')
    article_status_new = models.ForeignKey(
        ArticleStatus,
        verbose_name='Статус публикации (новый)',
        null=True,
        on_delete=models.SET_NULL,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_pk = None

    def __str__(self):
        return f'{self.name} - ({self.hub.name})'


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
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


class SubComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.PROTECT,
                                verbose_name='Статья')
    text = models.TextField(verbose_name='Текст подкомментария')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                verbose_name='Комментарий')
    author = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                               verbose_name='Автор подкомментария')
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Активация комментария')
    add_datetime = models.DateTimeField(
        'Время добавления ответа', auto_now_add=True)

    def __str__(self):
        return f'Комментарий к сообщению: {self.comment.text} - {self.text}'

    class Meta:
        verbose_name = 'Подкомментарий'
        verbose_name_plural = 'Подкомментарии'


class Visits(models.Model):
    """Визиты пользователей для просмотра"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.CharField(max_length=32, verbose_name='Имя посетителя')
    host = models.CharField(max_length=32, verbose_name='IP посетителя')


class VoiceArticle(models.Model):
    """Аудио текст"""
    audio_file = models.FileField(upload_to="audio")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Rating(models.Model):
    """Рейтинг"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    @property
    def total_rating(self):
        """Подсчет рейтинга"""
        _article = self.article
        _likes = Likes.objects.filter(article=_article, status="LK").count()
        _dislikes = Likes.objects.filter(article=_article, status="DZ").count()
        _comment = Comment.objects.filter(article=_article, is_active=True).count()
        _sub_comment = SubComment.objects.filter(article=_article, is_active=True).count()
        total_rating = (int(_article.views) * 2) + (_likes * 3) + _dislikes + (_comment * 4) + (_sub_comment * 5)
        return total_rating
