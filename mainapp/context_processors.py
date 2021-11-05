from mainapp.models import Hub, Article, ArticleStatus
from mainapp.search_filter import ArticleFilter


def category(request):
    return {"category_menu": Hub.objects.all()}


def search_filter(request):
    article = Article.objects.filter(article_status_new=ArticleStatus.objects.get(name='Опубликована'))
    search_filter = ArticleFilter(request.GET, queryset=article)
    return {'search_filter': search_filter}

