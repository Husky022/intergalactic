from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from mainapp.models import Article


class Main(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'Главная'}


class Articles(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}


def article_page(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'page_title': 'продукт',
        'article': article,
        'category_pk': article.category_id,
    }
    return render(request, 'mainapp/article_page.html', context)


def article_category(request, category_pk):
    article = get_object_or_404(Article, pk=category_pk)
    context = {
        'article': article,
        'category_pk': article.category_pk,
    }
    return render(request, context)

