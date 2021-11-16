"""Модуль лайки и дизлайки"""
from authapp.models import NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import Likes
from authapp.services.debugger import timing


class LikeDislike(object):
    """Лайки и дизлайки"""

    def __init__(self, user, article, status=None):
        """Инициализация лайка для usera, прием реквеста и кваргс"""
        self.user = user
        self.article = article
        self.status = status
        self.like = self.change_like()

    def change_like(self):
        """Выбор состояние лайка по отношению зарегистрирован или нет и нахождения usera в этот момент"""
        if self.user.is_anonymous:
            self.like = Likes
        else:
            if Likes.objects.filter(article=self.article, user=self.user):
                self.like = Likes.objects.get(article=self.article, user=self.user)
            else:
                self.like = Likes.objects.create(article=self.article, user=self.user)
        return self.like

    def define_count_like(self):
        """Сохранение в статье статуса лайков и дизлайков и их количества для рендера"""
        likes = Likes.objects.filter(article=self.article)
        self.article.count_like = len(likes.filter(status="LK"))
        self.article.count_dislike = len(likes.filter(status="DZ"))
        if self.status:
            self.article.status_like_dislike = self.like.status
        self.article.save()


    @timing
    def status_like(self):
        """Сохранение статуса лайка и дизлайка"""
        if self.like.status == self.status.get("status"):
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = "UND"
        else:
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = self.status.get("status")
            notification = Notification(self.like)
            notification.send()
        self.like.save()

    def render_like_and_dislike(self, context):
        """Рендер количества лайков и дизлайков"""
        self.define_count_like()
        context["article"] = self.article
        return context
