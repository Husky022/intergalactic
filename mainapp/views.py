from django.shortcuts import render, get_object_or_404
from datetime import datetime
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from mainapp.models import ArticlesCategory, Article


def get_category_menu():
    return ArticlesCategory.objects.all()


def get_articles():
    return Article.objects.all()

# Create your views here.
def base(request):
    context = {
        'now': datetime.now().year
    }
    return render(request, 'mainapp/base.html', context)


def main(request):
    context = {}
    return render(request, 'mainapp/index.html', context)


def articles(request):
    context = {
        'page_title': 'статьи',
        'category_menu': get_category_menu(),
        'articles': get_articles(),
    }
    return render(request, 'mainapp/articles.html', context)


def article_page(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'page_title': 'продукт',
        'article': article,
        'category_menu': get_category_menu(),
        'category_pk': article.category_id,
    }
    return render(request, 'mainapp/article_page.html', context)


def article_category(request, category_pk):
    article = get_object_or_404(Article, pk=category_pk)
    context = {
        'article': article,
        'category_pk': article.category_pk,
        'category_menu': get_category_menu(),
    }
    return render(request, context)


def programming(request):
    context = {
        'title': 'Программирование'
    }
    return render(request, 'mainapp/category_base.html', context)


def web_design_page(request):
    context = {
        'title': 'Веб-Дизайн'
    }
    return render(request, 'mainapp/category_base.html', context)


def html_css_page(request):
    context = {
        'title': 'HTML/CSS'
    }
    return render(request, 'mainapp/category_base.html', context)

