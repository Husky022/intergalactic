"""Модуль лайки и дизлайки"""
from authapp.models import IntergalacticUser, NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import Likes, Article


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
        return self.like

    def render_like_and_dislike(self):
        """Рендер количества лайков и дизлайков"""
        like_count = self.define_count_like("LK")
        dislike_count = self.define_count_like("DZ")
        return like_count, dislike_count

    def define_count_like(self, status):
        """Выбор статуса лайков и дизлайков для рендера"""
        return len(Likes.objects.filter(article_id=int(self.kwargs["pk"]), status=status))

    def status_like(self):
        """Сохранение статуса лайка и дизлайка"""
        status=self.request.GET.get("status")
        if self.like.status == status:
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = "UND"
        else:
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = status
            notification = Notification(self.like)
            notification.send()
        return self.like.save()

    def view_like(self):
        """Показ лайков и дизлайков на страничке"""
        self.like.like_count, self.like.dislike_count = self.render_like_and_dislike()
        return self.like
