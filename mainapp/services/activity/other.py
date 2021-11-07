from mainapp.models import Visits, Likes, Comment, SubComment


def total_rating(self):
    """Подсчет рейтинга"""
    _article = self.article
    _likes = Likes.objects.filter(article=_article, status="LK").count()
    _dislikes = Likes.objects.filter(article=_article, status="DZ").count()
    _comment = Comment.objects.filter(article=_article, is_active=True).count()
    _sub_comment = SubComment.objects.filter(article=_article, is_active=True).count()
    _total_rating = (int(_article.views) * 2) + (_likes * 3) + _dislikes + (_comment * 4) + (_sub_comment * 5)
    return _total_rating

# def rating(article):
#     """Показывает рейтинг"""
#     Rating.objects.get_or_create(article=article)
#     rating = Rating.objects.get(article=article)
#     return rating.total_rating


def view_views(self):
    """Показывает просмотры"""
    user_ip = self.request.get_host()
    if self.request.user.is_authenticated:
        user_name = self.request.user.username
    else:
        user_name = "Anon"
    self.object = self.get_object()
    if Visits.objects.filter(article=self.object,host=user_ip, user=user_name):
        return None
    else:
        self.object.views += 1
        Visits.objects.create(article=self.object, user=user_name, host=user_ip)
        self.object.save()
