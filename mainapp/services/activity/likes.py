from django.template.loader import render_to_string
from mainapp.models import Likes, Article

from authapp.models import IntergalacticUser
from mainapp.models import Likes, Article
from authapp.services.notifications import Notification

class LikeDislike(object):
    """Лайки и дизлайки"""

    def __init__(self, request, kwargs):
        """Инициализация лайка для usera, прием реквеста и кваргс"""
        self.request = request
        self.kwargs = kwargs
        self.like = self.change_like()

    def change_like(self):
        """Выбор состояние лайка по отношению зарегистрирован или нет и нахождения usera в этот момент"""
        if self.request.user.is_anonymous:
            self.like = Likes
        elif "article_page" in self.request.META["PATH_INFO"]:
            if Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk):
                self.like = Likes.objects.filter(article=self.kwargs["pk"], user=self.request.user).first()
            elif not Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk):
                self.like = Likes.objects.create(article_id=self.kwargs["pk"], user_id=self.request.user.pk)
        else:
            self.like = Likes.objects.filter(user=self.request.user)
        print(self.like)
        return self.like

    def render_like_and_dislike(self):
        """Рендер количества лайков и дизлайков"""
        like_count = self.define_count_like("LK")
        dislike_count = self.define_count_like("DZ")
        return like_count, dislike_count

    def define_count_like(self, status):
        """Выбор статуса лайков и дизлайков для рендера"""
        return len(Likes.objects.filter(article_id=int(self.kwargs["pk"]), status=status))

    def status_like(self, status):
        """Сохранение статуса лайка и дизлайка"""
        if self.like.status == status:
            self.like.status = "UND"
        else:
            article = Article.objects.filter(id=int(self.kwargs["pk"])).first()
            recipient = IntergalacticUser.objects.filter(id=article.author_id).first()
            Notification.create('like_article', recipient, self.request.user, None, article.name,
                                int(self.kwargs["pk"]), None, None)
            self.like.status = status
        self.like.save()

    def view_like(self):
        """Показ лайков и дизлайков на страничке"""
        self.like.like_count, self.like.dislike_count = self.render_like_and_dislike()
        return self.like

    def set_like(self, context):
        """Добавление и удаление лайка и дизлайка"""
        self.status_like(self.request.GET.dict()["status"])
        self.like.like_count, self.like.dislike_count = self.render_like_and_dislike()
        context["likes"] = self.like
        result = render_to_string('mainapp/includes/inc__activity.html', context=context, request=self.request)
        return result

# def new_like(self):
#     if not Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk):
#         Likes.objects.create(article_id=self.kwargs["pk"], user_id=self.request.user.pk)
#
#
# def change_like(self):
#     if not self.request.user.is_anonymous:
#         like = Likes.objects.filter(article_id=int(self.kwargs["pk"]), user_id=self.request.user.pk).first()
#     else:
#         if Likes.objects.filter(article_id=int(self.kwargs["pk"])):
#             like = Likes.objects.filter(article_id=int(self.kwargs["pk"])).first()
#         else:
#             return None
#     return like
#
#
# def define_count_like(self, status):
#     return len(Likes.objects.filter(article_id=int(self.kwargs["pk"]), status=status))
#
#
# def view_like(self):
#     like = change_like(self)
#     if like:
#         like.like_count = define_count_like(self, "LK")
#         like.dislike_count = define_count_like(self, "DZ")
#         return like
#     return None
#
#
# def set_like(self, context):
#     new_like(self)
#     like = change_like(self)
#     like = status_like(like, self.request.GET.dict()["status"])
#     like.like_count = define_count_like(self, "LK")
#     like.dislike_count = define_count_like(self, "DZ")
#     context["likes"] = like
#     result = render_to_string('mainapp/includes/inc__activity.html', context=context, request=self.request)
#     return result

# def set_like(self, context):
#     new_like(self)
#     like = change_like(self)
#     like = status_like(self, like, self.request.GET.dict()["status"])
#     like.like_count = define_count_like(self, "LK")
#     like.dislike_count = define_count_like(self, "DZ")
#     context["likes"] = like
#     result = render_to_string('mainapp/includes/inc__icon.html', context=context, request=self.request)
#     return result
