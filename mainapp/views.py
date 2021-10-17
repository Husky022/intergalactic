from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from authapp.models import IntergalacticUser
from mainapp.forms import ArticleCreationForm
from mainapp.models import Article, Hub


class Main(ListView):
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'Главная'}
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.objects.filter(is_active=True)
        return queryset


class Articles(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.objects.filter(is_active=True)
        return queryset


def article_page(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'page_title': 'Статья',
        'article': article,
        'article_pk': article.hub_id,
    }
    return render(request, 'mainapp/article_page.html', context)


class Hub_category(ListView):
    model = Article
    template_name = 'mainapp/hub_category.html'
    context_object_name = 'hub'
    paginate_by = 5
    # allow_empty = False # Когда страница не найдена отдавать 404 ошибку

    def get_queryset(self):
        # Фильтр по категории и сортировка "сначала новые"
        return Article.objects.filter(
            is_active=True,
            hub__id=self.kwargs['hub_id']
        ).order_by('-add_datetime')


class ArticleCreationView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('auth:profile')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleChangeActiveView(View):
    def post(self, request, article_pk):
        target_article = get_object_or_404(Article, pk=article_pk)
        target_article.is_active = False if target_article.is_active else True
        # Пока сделал, что все статьи из архива - попадают на модерацию
        # Надо будет обдумать более гибкую логику
        target_article.article_status = 'AR' if target_article.article_status != 'AR' else 'PB'
        target_article.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ArticleEditView(UpdateView):
    """Контроллер для изменения товара"""
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('auth:profile')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
