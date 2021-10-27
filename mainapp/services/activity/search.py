from django.shortcuts import render

from mainapp.services.activity.view import Activity

from ...models import Article
from ...search_filter import ArticleFilter


def search_pb(request):
    article = Article.objects.filter(article_status='PB')
    search_filter = ArticleFilter(request.GET, queryset=article)
    # article = search_filter.qs
    return search_filter

    # contex = {'page_title': 'Поиск', 'object_list': article, 'search_filter': search_filter}
    # return render(request, 'mainapp/articles.html', contex)