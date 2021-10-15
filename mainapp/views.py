from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from mainapp.models import Article


class Main(ListView):
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        queryset = Article.objects.all()[:3]
        return queryset


class Articles(ListView):
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}

    def get_queryset(self):
        queryset = Article.objects.all()[:10]
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
    # allow_empty = False # Когда страница не найдена отдавать 404 ошибку

    def get_queryset(self):
        # Фильтр по категории и сортировка "сначала новые"
        return Article.objects.filter(hub__id=self.kwargs['hub_id']).order_by('-add_datatime')


