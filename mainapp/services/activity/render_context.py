
from authapp.models import NotificationModel
from mainapp.services.activity.likes import LikeDislike
from mainapp.services.activity.comment import CommentSubcomment

from mainapp.models import Article, Comment, Likes, SubComment, Hosts, Art_Visits, ArticleStatus, VoiceArticle


# Article View

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
        item.item_comment = Comment.objects.filter(article=item, is_active=True).count() + SubComment.objects.filter(
            article=item, is_active=True).count()
        item.like_count = Likes.objects.filter(article=item, status="LK").count()
        item.dislike_count = Likes.objects.filter(article=item, status="DZ").count()
        item.rating = item.dislike_count + item.views * 2 + item.like_count * 3 + Comment.objects.filter(
            article=item, is_active=True).count() * 4 + SubComment.objects.filter(article=item,
                                                                                  is_active=True).count() * 5
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


def article_views(self):
    """Увеличение просмотров"""
    # article = Article.objects.filter(id=self.kwargs["pk"]).first()
    # article.views += 1
    # article.save()
    visitor_IP = self.request.get_host()
    print(f'int(kwargs["pk"] = {int(self.kwargs["pk"])}')
    Hosts.objects.get_or_create(host=visitor_IP)
    self.object = self.get_object()
    for v in Art_Visits.objects.filter(host=Hosts.objects.get(host=visitor_IP).pk):
        if v.article_id == int(self.kwargs["pk"]):
            break
    else:
        self.object.views += 1
        v = Art_Visits(article=self.object,
                       host=Hosts.objects.get(host=visitor_IP))
        v.save()
    self.object.save()


def fill_context(self):
    """Рендер контекста"""
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())

    context = CommentSubcomment(self.request, self.kwargs).render_context(context)
    context['likes'] = LikeDislike(self.request, self.kwargs).view_like()
    context["rating"] = context["likes"].dislike_count + self.object.views * 2 + \
                        context["likes"].like_count * 3 + len(context['comments']) * 4 + len(
        SubComment.objects.filter(article_id=self.kwargs["pk"], is_active=True)) * 5
    context['notifications_not_read'] = NotificationModel.objects.filter(is_read=0,
                                                                         recipient=self.request.user.id).count()
    article = Article.objects.filter(id=self.kwargs["pk"]).first()
    context['audio'] = VoiceArticle.objects.filter(article=article).first()
    return context
