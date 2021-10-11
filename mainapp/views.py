from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from mainapp.models import Article


class Main(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'Главная'}


class Articles(ListView):
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}

    def get_queryset(self):
        queryset = Article.objects.all()[:10]
        return queryset


def article_page(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'page_title': 'продукт',
        'article': article,
        'article_pk': article.hub_id,
    }
    return render(request, 'mainapp/article_page.html', context)


def hub(request, hub_pk):
    article = get_object_or_404(Article, pk=hub_pk)
    context = {
        'article': article,
        'hub_pk': article.hub_id,
    }
    return render(request, context)
