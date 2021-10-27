from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from mainapp.services.activity.likes import LikeDislike
from mainapp.services.activity.comment import CommentSubcomment

from mainapp.models import Article, Comment, Likes, SubComment


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
        self.comment_list.append(item)

    def parse_all(self):
        return Article.objects.filter(is_active=True)

    def parse_filter(self):
        return Article.objects.filter(hub__id=self.kwargs['pk'], is_active=True)


class Parse:
    types = {
        'all': RenderArticle.parse_all,
        'filter': RenderArticle.parse_filter
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)


# def parse_all():
#     return Article.objects.filter(is_active=True)
#
#
# def parse_filter(self):
#     return Article.objects.filter(hub__id=self.kwargs['pk'], is_active=True)
#
#
# def add_item(item, comment_list):
#     item.item_comment = Comment.objects.filter(article=item, is_active=True).count() + SubComment.objects.filter(
#         article=item, is_active=True).count()
#     item.like_count = Likes.objects.filter(article=item, status="LK").count()
#     item.dislike_count = Likes.objects.filter(article=item, status="DZ").count()
#     comment_list.append(item)
#
#
# def for_parse(type_, comment_list, *args):
#     for item in Parse.create(type_, *args):
#         add_item(item, comment_list)
#
#
# def if_article(comment_list, self):
#     if self.kwargs.get("pk", None):
#         for_parse("filter", comment_list, self)
#     else:
#         for_parse("all", comment_list)
#
#
# def queryset_activity(self):
#     comment_list = []
#     if_article(comment_list, self)
#     return comment_list


def fill_context(self):
    """Рендер контекста"""
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())
    context = CommentSubcomment(self.request, self.kwargs).render_context(context)
    context['likes'] = LikeDislike(self.request, self.kwargs).view_like()
    return context


def article_page_get(self):
    """Get запрос для article_page"""
    context = fill_context(self)
    if self.request.is_ajax():
        if self.request.GET.dict().get("text_comment") or self.request.GET.dict().get("text_subcomment"):
            context = CommentSubcomment(self.request, self.kwargs, self.request.GET.dict()).set(context)
        elif self.request.GET.dict().get("com_delete") or self.request.GET.dict().get("sub_com_delete"):
            context = CommentSubcomment(self.request, self.kwargs, self.request.GET.dict()).delete(context)
        else:
            context = LikeDislike(self.request, self.kwargs, ).set_like(context)
        result = render_to_string('mainapp/includes/inc__activity.html', context, request=self.request)
        return JsonResponse({"result": result})
    return self.render_to_response(context)


def article_page_post(self):
    """Post запрос для article page"""
    CommentSubcomment(self.request, self.kwargs, self.request.POST.dict()).add_get_or_post()
    CommentSubcomment(self.request, self.kwargs, self.request.POST.dict()).delete_get_or_post()
    return HttpResponseRedirect(reverse_lazy('article_page', args=(int(self.kwargs["pk"]),)))


class Activity:
    types = {
        'get': article_page_get,
        'post': article_page_post,
    }

    @classmethod
    def create(cls, type_, *args, **kwargs):
        return cls.types[type_](*args, **kwargs)
