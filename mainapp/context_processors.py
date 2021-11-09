from authapp.models import NotificationModel
from mainapp.models import Hub, Article, ArticleStatus
from mainapp.search_filter import ArticleFilter


def category(request):
    return {"category_menu": Hub.objects.all()}


def search_filter(request):
    article = Article.objects.filter(article_status_new=ArticleStatus.objects.get(name='Опубликована'))
    search_filter = ArticleFilter(request.GET, queryset=article)
    return {'search_filter': search_filter}


def notification(request):
    if request.user.is_authenticated:
        notifications_not_read = NotificationModel.objects.filter(is_read=0, recipient=request.user).count()
        return {'notifications_not_read': notifications_not_read}
    else:
        return  {'notifications_not_read': NotificationModel}
