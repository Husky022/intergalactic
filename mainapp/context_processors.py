from authapp.models import NotificationModel
from mainapp.models import Hub, Article, ArticleStatus, Sorting
from .services.search_filter import ArticleFilter
from moneyapp.models import Transaction

def category(request):
    return {"category_menu": Hub.objects.all()}


def search_filter(request):
    article = Article.objects.all()
    search_filter = ArticleFilter(request.GET, queryset=article)
    return {'search_filter': search_filter}


def notification(request):
    if request.user.is_authenticated:
        notifications_not_read = NotificationModel.objects.filter(is_read=0, recipient=request.user).count()
        return {'notifications_not_read': notifications_not_read}
    else:
        return {'notifications_not_read': NotificationModel}

def transactions_not_read(request):
    if request.user.is_authenticated:
        transactions_not_read = Transaction.objects.filter(is_read=False, status='CREATED'),
        transactions_not_read_count = Transaction.objects.filter(is_read=False, status='CREATED').count()
        return {'transactions_not_read': transactions_not_read,
                'transactions_not_read_count': transactions_not_read_count,
                }
    else:
        return {'transactions_not_read': Transaction}


def get_sorted_type(request):
    if request.user.is_anonymous:
        try:
            sorting_type = request.session['sorting']
        except:
            sorting_type = 'NEWEST'
    else:
        try:
            sorting_type = Sorting.objects.filter(user=request.user.id)[0].sorting_type
        except:
            sorting_type = 'NEWEST'
    return {'sorting_type': sorting_type}