from compat import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from moneyapp.services.moneys import make_donations

from mainapp.models import Article, ArticleStatus, Sorting
from mainapp.forms import ArticleCreationForm, CommentForm
from mainapp.models import Comment
from mainapp.services.activity.likes import LikeDislike

from .services.search_filter import ArticleFilter
from .services.articlepage.get import get_article_page, if_get_ajax
from .services.articlepage.post import post_article_page
from .services.audio import play_text
from .services.sorting import get_sorted_queryset
#from moneyapp.models import Transaction # конфликт при слиянии ie-173, на всякий случай пока просто закомментил
from .services.activity.comment import add_comment_complaint
from .services.mainpage.get_context import get_context_main_page



class Main(ListView):
    """ CBV Главной страницы """
    model = Article
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return get_context_main_page(self, context)


class Articles(ListView):
    """ CBV хабов страницы """
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        status = ArticleStatus.objects.get(name='Опубликована')
        if self.kwargs["pk"] == 0:
            article = Article.objects.filter(article_status_new=status)
        else:
            article = Article.objects.filter(
                article_status_new=status, hub=self.kwargs["pk"])

        return get_sorted_queryset(self, article)


class ArticlePage(DetailView):
    """CBV одной статьи"""
    template_name = 'mainapp/article_page.html'
    model = Article
    extra_context = {
        'page_title': 'Статья',
        'CommentForm': CommentForm,
    }

    def get(self, request, *args, **kwargs):
        # Сбор контекста и взаимодействие активити
        context = get_article_page(self)

        # Проверка на аякс
        if self.request.is_ajax():
            return if_get_ajax(self, context)

        # Рендер обычного гет запроса
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        # Взаимодействие активити
        post_article_page(self)

        # Рендер обычного гет запроса

        if 'donation' in self.request.POST.dict():
            make_donations(self, self.request.POST)
        if 'comment_complaint' in self.request.POST.dict():
            add_comment_complaint(
                self.request.user.id, self.request.POST['comment_complaint'], self.request.POST['text_complaint'])
            # print(self.request.POST.dict())
            print(self.request)
            # print(user.id)
            # make_donations(self, self.request.POST)
        return HttpResponseRedirect(reverse_lazy('article_page', args=(int(self.kwargs["pk"]),)))


class ArticleCreationView(CreateView):
    """CBV для создание статьи"""
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('auth:profile')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.article_status_new = ArticleStatus.objects.get(
            name='Черновик')
        self.object.save()
        return super().form_valid(form)


class ArticleChangeActiveView(View):
    """CBV для активации статьи"""

    def post(self, request, article_pk):
        target_article = get_object_or_404(Article, pk=article_pk)
        target_article.is_active = False if target_article.is_active else True

        if target_article.article_status_new.name == 'В архиве':
            target_article.article_status_new = ArticleStatus.objects.get(
                name='Черновик')
        else:
            target_article.article_status_new = ArticleStatus.objects.get(
                name='В архиве')

        target_article.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ArticleEditView(View):
    """Контроллер для изменения статьи"""
    title = 'Редактирование статьи'
    template_name = 'mainapp/edit_article.html'
    form_class = ArticleCreationForm
    redirect_to = 'auth:profile'

    def get(self, request, pk):
        context = {
            'form': self.form_class(instance=Article.objects.get(pk=pk)),
            'article': Article.objects.get(pk=pk)
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article_form = ArticleCreationForm(
            data=request.POST, files=request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            if article.article_status_new == ArticleStatus.objects.get(name='Опубликована'):
                article.article_status_new = ArticleStatus.objects.get(
                    name='На модерации')
                article.save()

        return HttpResponseRedirect(reverse(self.redirect_to))


class SendToModeration(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(
            name='На модерации')
        play_text(pk)
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


class DraftArticle(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Черновик')
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


class Search(ListView):
    # model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Поиск'}
    paginate_by = 5

    def get_queryset(self, article):
        return get_sorted_queryset(self, article)

    def get(self, request, page_num=1, *args, **kwargs):
        article = Article.objects.filter(
            article_status_new=ArticleStatus.objects.get(name='Опубликована'))
        search_filter = ArticleFilter(request.GET, queryset=article)
        article = search_filter.qs
        self.object_list = self.get_queryset(article)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context['search_filter'] = search_filter
        context['filter'] = request.GET.dict()
        return render(request, 'mainapp/articles.html', context)


def set_sorted_type(request, sorting_type):
    sorting = Sorting.objects.all()
    if request.user.is_anonymous:
        request.session['sorting'] = sorting_type
    else:
        sorting_by_user = sorting.filter(user=request.user.id)
        sorting_by_user.update(sorting_type=sorting_type)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def like_dislike_comment(request, pk):
    get_dict = request.GET.dict()
    comment = Comment.objects.get(pk=pk)
    like_dislike = LikeDislike(comment.author, comment.article, get_dict.get('status'), comment=comment)
    like_dislike.status_like()
    like_dislike.define_count_like()
    return JsonResponse({"count_like": comment.count_like,
                         "count_dislike": comment.count_dislike,
                         "status": like_dislike.like.status})
