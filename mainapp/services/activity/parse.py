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
        if self.kwargs.get("pk", None) and len(self.kwargs.keys()) == 1:
            self.for_parse("filter")

        elif self.kwargs.get("by_date") == 'first_old':
            self.for_parse("sorting_by_date_first_old")
        elif self.kwargs.get("by_date") == 'first_new':
            self.for_parse("sorting_by_date_first_new")

        elif self.kwargs.get("by_like") == 'first_less':
            self.for_parse("sorting_by_like_first_less")
        elif self.kwargs.get("by_like") == 'first_more':
            self.for_parse("sorting_by_like_first_more")

        elif self.kwargs.get("by_comments") == 'first_less':
            self.for_parse("sorting_by_comment_first_less")
        elif self.kwargs.get("by_comments") == 'first_more':
            self.for_parse("sorting_by_comment_first_more")
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
        return Article.objects.filter(hub__id=self.kwargs.get("pk"), is_active=True,
                                      article_status_new=ArticleStatus.objects.get(name="Опубликована"))

    def parse_filter_by_hub(self, pk):
        return Article.objects.filter(hub__id=pk, is_active=True,
                                      article_status_new=ArticleStatus.objects.get(name="Опубликована"))

    def sorting_by_date_first_old(self):
        hub_pk = self.kwargs.get("pk")
        if hub_pk == 0:
            return self.parse_all().order_by('add_datetime')
        else:
            return self.parse_filter_by_hub(hub_pk).order_by('add_datetime')

    def sorting_by_date_first_new(self):
        hub_pk = self.kwargs.get("pk")
        if hub_pk == 0:
            return self.parse_all().order_by('-add_datetime')
        else:
            return self.parse_filter_by_hub(hub_pk).order_by('-add_datetime')

    def sorting_by_like_first_more(self, sort_order=True):
        hub_pk = self.kwargs.get("pk")
        likes_id = []
        result_list = []
        if hub_pk == 0:
            parse_func = self.parse_all()
        else:
            parse_func = self.parse_filter_by_hub(hub_pk)
        for item in parse_func:
            count_like = len(Likes.objects.filter(article_id=item.id, status='LK'))
            likes_id.append((count_like, item.name, item))
        sorted_list = sorted(likes_id, key=lambda count: count[0], reverse=sort_order)
        for i in sorted_list:
            result_list.append(i[2])
        return result_list

    def sorting_by_like_first_less(self, sort_order=False):
        hub_pk = self.kwargs.get("pk")
        likes_id = []
        result_list = []
        if hub_pk == 0:
            parse_func = self.parse_all()
        else:
            parse_func = self.parse_filter_by_hub(hub_pk)
        for item in parse_func:
            count_like = len(Likes.objects.filter(article_id=item.id, status='LK'))
            likes_id.append((count_like, item.name, item))
        sorted_list = sorted(likes_id, key=lambda count: count[0], reverse=sort_order)
        for i in sorted_list:
            result_list.append(i[2])
        return result_list

    def sorting_by_comment_first_more(self, sort_order=True):
        hub_pk = self.kwargs.get("pk")
        touple_list = []
        result_list = []
        if hub_pk == 0:
            parse_func = self.parse_all()
        else:
            parse_func = self.parse_filter_by_hub(hub_pk)
        for item in parse_func:
            count_comment = len(Comment.objects.filter(article_id=item.id))
            touple_list.append((count_comment, item.name, item))
        sorted_list = sorted(touple_list, key=lambda count: count[0], reverse=sort_order)
        for i in sorted_list:
            result_list.append(i[2])
        return result_list

    def sorting_by_comment_first_less(self, sort_order=False):
        hub_pk = self.kwargs.get("pk")
        touple_list = []
        result_list = []
        if hub_pk == 0:
            parse_func = self.parse_all()
        else:
            parse_func = self.parse_filter_by_hub(hub_pk)
        for item in parse_func:
            count_comment = len(Comment.objects.filter(article_id=item.id))
            touple_list.append((count_comment, item.name, item))
        sorted_list = sorted(touple_list, key=lambda count: count[0], reverse=sort_order)
        for i in sorted_list:
            result_list.append(i[2])
        return result_list


class Parse:
    """Фабрика для фильтров"""
    types = {
        'all': RenderArticle.parse_all,
        'filter': RenderArticle.parse_filter,

        'sorting_by_date_first_old': RenderArticle.sorting_by_date_first_old,
        'sorting_by_date_first_new': RenderArticle.sorting_by_date_first_new,

        'sorting_by_like_first_more': RenderArticle.sorting_by_like_first_more,
        'sorting_by_like_first_less': RenderArticle.sorting_by_like_first_less,

        'sorting_by_comment_first_more': RenderArticle.sorting_by_comment_first_more,
        'sorting_by_comment_first_less': RenderArticle.sorting_by_comment_first_less,
    }

    @classmethod
    def create(cls, type_, *args, **kwargs):
        return cls.types[type_](*args, **kwargs)


def get_sorted(kwargs, request):
    try:
        kwargs['pk'] = request.resolver_match.kwargs.get('pk')
    except:
        kwargs['pk'] = 0

    if request.GET.dict().get('by_date') == 'first_old':
        kwargs['by_date'] = 'first_old'
    elif request.GET.dict().get('by_date') == 'first_new':
        kwargs['by_date'] = 'first_new'

    if request.GET.dict().get('by_like') == 'first_less':
        kwargs['by_like'] = 'first_less'
    elif request.GET.dict().get('by_like') == 'first_more':
        kwargs['by_like'] = 'first_more'

    if request.GET.dict().get('by_comments') == 'first_less':
        kwargs['by_comments'] = 'first_less'
    elif request.GET.dict().get('by_comments') == 'first_more':
        kwargs['by_comments'] = 'first_more'
    return kwargs