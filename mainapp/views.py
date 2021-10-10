from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from mainapp.models import Article, Hub


class Main(TemplateView):
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'Главная'}


class Articles(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}



def index(request):
    recent_articles = Articles.objects.filter(is_active=True)[:10]
    context = {'articles': recent_articles, 'title': 'Главная'}
    return render(request, 'mainapp/index1.html', context)



def article_page(request, hub_pk):
    article = get_object_or_404(Article, pk=hub_pk)
    context = {
        'page_title': 'продукт',
        'article': article,
        'hub_pk': article.hub_id,
    }
    return render(request, 'mainapp/article_page.html', context)


def hub(request, hub_pk):
    article = get_object_or_404(Article, pk=hub_pk)
    context = {
        'article': article,
        'hub_pk': article.hub_id,
    }
    return render(request, context)
