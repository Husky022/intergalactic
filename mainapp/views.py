from django.shortcuts import get_object_or_404, render
from django.views.generic import View, CreateView, ListView, DetailView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from authapp.models import NotificationModel
from mainapp.models import Article, ArticleStatus
from mainapp.services.activity.render_context import Activity, RenderArticle
from mainapp.forms import ArticleCreationForm, CommentForm, SubCommentForm
from .search_filter import ArticleFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Main(ListView):
    """ CBV Главной страницы """
    template_name = 'mainapp/index.html'
    paginate_by = 5
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        queryset = RenderArticle(self.kwargs).queryset_activity()
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        article = Article.objects.filter(article_status='PB')
        search_filter = ArticleFilter(request.GET, queryset=article)

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
        context['notifications_not_read'] = NotificationModel.objects.filter(is_read=0,
                                                                             recipient=self.request.user.id).count()
        context['search_filter'] = search_filter
        return self.render_to_response(context)


class Articles(ListView):
    """ CBV хабов страницы """
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}

    # paginate_by = 5

    def get_queryset(self):
        queryset = RenderArticle(self.kwargs).queryset_activity()
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        article = Article.objects.filter(article_status='PB')
        search_filter = ArticleFilter(request.GET, queryset=article)

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
        context['notifications_not_read'] = NotificationModel.objects.filter(is_read=0,
                                                                             recipient=self.request.user.id).count()
        context['search_filter'] = search_filter
        return self.render_to_response(context)


class ArticlePage(DetailView):
    """CBV одной статьи"""
    template_name = 'mainapp/article_page.html'
    model = Article
    extra_context = {
        'page_title': 'Статья',
        'CommentForm': CommentForm,
        'SubCommentForm': SubCommentForm
    }

    def get(self, request, *args, **kwargs):
        return Activity.create("get", self)

    def post(self):
        return Activity.create("post", self)


class ArticleCreationView(CreateView):
    """CBV для создание статьи"""
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('auth:profile')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.article_status_new = ArticleStatus.objects.get(name='Черновик')
        self.object.save()
        return super().form_valid(form)


class ArticleChangeActiveView(View):
    """CBV для активации статьи"""

    def post(self, request, article_pk):
        target_article = get_object_or_404(Article, pk=article_pk)
        target_article.is_active = False if target_article.is_active else True

        if target_article.article_status_new.name == 'В архиве':
            target_article.article_status_new = ArticleStatus.objects.get(name='Черновик')
        else:
            target_article.article_status_new = ArticleStatus.objects.get(name='В архиве')

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
                article.article_status_new = ArticleStatus.objects.get(name='На модерации')
                article.save()

        return HttpResponseRedirect(reverse(self.redirect_to))


class SendToModeration(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='На модерации')
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


class DraftArticle(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Черновик')
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


# def search(request):
#     article = Article.objects.filter(article_status='PB')
#     search_filter = ArticleFilter(request.GET, queryset=article)
#     article = search_filter.qs
#     paginator = Paginator(article, 2)
#     page = request.GET.get('page')
#
#     try:
#         article = paginator.page(page)
#     except PageNotAnInteger:
#         article = paginator.page(1)
#     except EmptyPage:
#         article = paginator.page(paginator.num_pages)
#
#     contex = {'page_title': 'Поиск',
#               'object_list': article,
#               'search_filter': search_filter,
#               'page_obj': article
#               }
#     return render(request, 'mainapp/articles.html', contex)

class Search(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    paginate_by = 5

    def get(self, request, page_num=1, *args, **kwargs):
        article = Article.objects.filter(article_status='PB')
        search_filter = ArticleFilter(request.GET, queryset=article)
        article = search_filter.qs

        # paginator = Paginator(article, 2)
        # page = request.GET.get('page')
        #
        # try:
        #     article = paginator.page(page)
        # except PageNotAnInteger:
        #     article = paginator.page(1)
        # except EmptyPage:
        #     article = paginator.page(paginator.num_pages)
        contex = {'page_title': 'Поиск',
                  'object_list': article,
                  'search_filter': search_filter,
                  # 'page_obj': article
                  }
        return render(request, 'mainapp/articles.html', contex)
