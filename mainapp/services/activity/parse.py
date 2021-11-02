from mainapp.models import Article, Comment, Likes, SubComment, ArticleStatus

# Article View
from mainapp.services.activity.other import rating


class RenderArticle:
    """Рендер контекста Article и Activity в множественном количестве"""

    def __init__(self, kwargs=None):
        """Инициализируем рендер"""
        self.kwargs = kwargs
        self.comment_list = []

    def queryset_activity(self):
        """Возвращает queryset """
        self.if_article()
        return self.comment_list

    def if_article(self):
        """Определяет фильтр по которому будет готов queryset"""
        if self.kwargs.get("pk", None):
            self.for_parse("filter")
        else:
            self.for_parse("all")

    def for_parse(self, type_):
        """Берет функцию указанную в фильтре из класса Parse"""
        for item in Parse.create(type_, self):
            self.add_item(item)

    def add_item(self, item):
        """Добавляет в каждый item количество like, dislike, comment, subcomment"""
        item.rating = rating(article=item)
        item.item_comment = Comment.objects.filter(article=item, is_active=True).count() + SubComment.objects.filter(
            article=item, is_active=True).count()
        item.like_count = Likes.objects.filter(article=item, status="LK").count()
        item.dislike_count = Likes.objects.filter(article=item, status="DZ").count()
        self.comment_list.append(item)

    def parse_all(self):
        return Article.objects.filter(is_active=True, article_status_new=ArticleStatus.objects.get(name="Опубликована"))

    def parse_filter(self):
        return Article.objects.filter(hub__id=self.kwargs['pk'], is_active=True,
                                      article_status_new=ArticleStatus.objects.get(name="Опубликована"))


class Parse:
    """Фабрика для фильтров"""
    types = {
        'all': RenderArticle.parse_all,
        'filter': RenderArticle.parse_filter
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)

# ArticlePage View
