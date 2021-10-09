from django.db import models


class ArticlesCategory(models.Model):
    name = models.CharField('категория статьи', max_length=64)
    is_active = models.BooleanField('активность', default=True)

    class Meta:
        verbose_name = 'категория статьи'
        verbose_name_plural = 'категории статей'

    def __str__(self):
        return f'Категория {self.name}'

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
        return 1, {}


class Article(models.Model):
    category = models.ForeignKey(ArticlesCategory, on_delete=models.CASCADE)
    name = models.CharField('имя', max_length=64)
    image = models.ImageField(upload_to='articles_images', blank=True)
    text = models.TextField('Текст статьи')
    tag = models.CharField('тэг статьи', max_length=64, blank=True)
    hub = models.CharField('хаб статьи', max_length=64, blank=True)
    add_datatime = models.DateField('время добавления', auto_now_add=True)
    is_active = models.BooleanField('активность', default=True)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_pk = None

    def __str__(self):
        return f'Категория {self.name} ({self.category.name})'

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
        return 1, {}
